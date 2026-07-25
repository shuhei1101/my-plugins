"""E2E テスト共通の fixture（実 Claude Code + 実 HTTP 配信 + 実観測基盤・--run-e2e ガード）。

前提:
- `claude` CLI が PATH にあること
- ログ検証を含むシナリオでは docker が使えて、observability リポジトリが本リポジトリと同階層にあること
  （観測基盤はテスト側で起動する）
"""
from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from base64 import b64encode
from dataclasses import dataclass
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK_DIR = REPO_ROOT / "plugins" / "inject-rules" / "hooks"
HOOK_SCRIPT = HOOK_DIR / "pre_tool_use.py"
SESSION_START_SCRIPT = HOOK_DIR / "session_start.py"
COMPOSE_FILE = REPO_ROOT.parent / "observability" / "observability.yaml"
OTLP_ENDPOINT = "http://localhost:4317"
GRAFANA_URL = "http://localhost:3000"
GRAFANA_AUTH = b64encode(b"admin:admin").decode()
CLAUDE_TIMEOUT_SEC = 600
STACK_READY_TIMEOUT_SEC = 180
# 会話ログのうち、フックがコンテキストへ渡した内容を表すレコード種別
HOOK_CONTEXT_TYPE = "hook_additional_context"
HOOK_EVENT = "PreToolUse"


def pytest_addoption(parser):
    """誤実行防止の --run-e2e フラグを定義する。"""
    parser.addoption(
        "--run-e2e",
        action="store_true",
        default=False,
        help="実 Claude Code + 実 HTTP 配信でシナリオ E2E テストを実行する",
    )


def pytest_collection_modifyitems(config, items):
    """--run-e2e なしでは E2E テスト（本フォルダ配下）を全 skip する。"""
    if config.getoption("--run-e2e"):
        return
    skip_marker = pytest.mark.skip(reason="--run-e2e なしのため skip")
    e2e_dir = Path(__file__).resolve().parent
    for item in items:
        if item.path.resolve().is_relative_to(e2e_dir):
            item.add_marker(skip_marker)


class _QuietHandler(SimpleHTTPRequestHandler):
    """アクセスログを標準エラーへ出さない配信ハンドラ。"""

    def log_message(self, format: str, *args: object) -> None:
        pass


@dataclass(frozen=True, slots=True, kw_only=True)
class WikiServer:
    """プロジェクト Wiki を模した HTTP 配信。"""

    base_url: str
    root: Path

    def put(self, name: str, text: str) -> str:
        """ファイルを配置してその URL を返す。"""
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return self.url_for(name)

    def url_for(self, name: str) -> str:
        """配置していない名前も含めて URL を組み立てる。"""
        return f"{self.base_url}/{name}"


@dataclass(frozen=True, slots=True, kw_only=True)
class ClaudeResult:
    """Claude Code の実行結果。"""

    session_id: str
    transcript: str
    injections: list[str]  # 1 要素 = フックが 1 回コンテキストへ渡した注入テキスト
    tool_calls: list[tuple[str, dict]]  # 発生順の（ツール名, 入力）

    @property
    def injected_text(self) -> str:
        """注入テキストをすべて連結して返す。"""
        return "\n".join(self.injections)


def _read_injections(transcript: str) -> list[str]:
    """会話ログから、フックがコンテキストへ渡した注入テキストを発生順に取り出す。"""
    injections: list[str] = []
    for line in transcript.splitlines():
        try:
            record = json.loads(line)
        except ValueError:
            continue
        attachment = record.get("attachment")
        if not isinstance(attachment, dict) or attachment.get("type") != HOOK_CONTEXT_TYPE:
            continue
        # 他のフック（UserPromptSubmit 等）が渡した内容と混ざらないようにする
        if attachment.get("hookEvent") != HOOK_EVENT:
            continue
        content = attachment.get("content")
        injections.append("".join(content) if isinstance(content, list) else str(content))
    return injections


def _read_tool_calls(transcript: str) -> list[tuple[str, dict]]:
    """会話ログから、ツール呼び出しを発生順に取り出す。"""
    calls: list[tuple[str, dict]] = []
    for line in transcript.splitlines():
        try:
            record = json.loads(line)
        except ValueError:
            continue
        message = record.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                calls.append((block.get("name", ""), block.get("input") or {}))
    return calls


@pytest.fixture(autouse=True)
def claude_cli() -> str:
    """`claude` CLI の実体パスを返す（未導入なら skip）。"""
    path = shutil.which("claude")
    if path is None:
        pytest.skip("claude CLI が PATH にない")
    return path


@pytest.fixture
def wiki_server(tmp_path: Path):
    """ルール索引とルール本文を配信する HTTP サーバを立てる。"""
    root = tmp_path / "wiki"
    root.mkdir()
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(_QuietHandler, directory=str(root)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield WikiServer(base_url=f"http://127.0.0.1:{server.server_port}", root=root)
    server.shutdown()
    server.server_close()


@pytest.fixture
def unreachable_url() -> str:
    """誰も待ち受けていないポートの索引 URL を返す。"""
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    return f"http://127.0.0.1:{port}/rules.yaml"


@pytest.fixture
def cache_dir(tmp_path: Path) -> Path:
    """取得済み本文のキャッシュ置き場を返す。"""
    return tmp_path / "cache"


@pytest.fixture
def session_dir(tmp_path: Path) -> Path:
    """セッション状態の保存先を返す。"""
    return tmp_path / "session"


@pytest.fixture
def claude_project(tmp_path: Path) -> Path:
    """ルール注入フックを登録した一時プロジェクトを作る。"""
    project = tmp_path / "project"
    (project / ".claude").mkdir(parents=True)
    settings = {
        "hooks": {
            "SessionStart": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python3",
                            "args": [str(SESSION_START_SCRIPT)],
                            "timeout": 10,
                        }
                    ],
                }
            ],
            "PreToolUse": [
                {
                    "matcher": "Read|Write",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python3",
                            "args": [str(HOOK_SCRIPT)],
                            "timeout": 60,
                        }
                    ],
                }
            ],
        }
    }
    (project / ".claude" / "settings.json").write_text(
        json.dumps(settings, ensure_ascii=False), encoding="utf-8"
    )
    return project


@pytest.fixture
def run_claude(claude_cli, claude_project: Path, cache_dir: Path, session_dir: Path):
    """索引 URL を環境変数へ渡して Claude Code を 1 セッション実行する factory。"""

    def _run(prompt: str, *, indexes: str | None) -> ClaudeResult:
        env = os.environ.copy()
        env["INJECT_RULES_CACHE_DIR"] = str(cache_dir)
        env["INJECT_RULES_SESSION_DIR"] = str(session_dir)
        env["INJECT_RULES_OTLP_ENDPOINT"] = OTLP_ENDPOINT
        if indexes is None:
            env.pop("INJECT_RULES_INDEXES", None)
        else:
            env["INJECT_RULES_INDEXES"] = indexes
        completed = subprocess.run(
            [claude_cli, "-p", prompt, "--output-format", "json", "--permission-mode", "acceptEdits"],
            cwd=claude_project,
            env=env,
            capture_output=True,
            text=True,
            timeout=CLAUDE_TIMEOUT_SEC,
            check=False,
        )
        if completed.returncode != 0:
            pytest.fail(f"claude の実行に失敗:\n{completed.stdout[-2000:]}\n{completed.stderr[-2000:]}")
        session_id = json.loads(completed.stdout)["session_id"]
        matches = sorted(Path.home().glob(f".claude/projects/*/{session_id}.jsonl"))
        if not matches:
            pytest.fail(f"セッション {session_id} の会話ログが見つからない")
        transcript = matches[0].read_text(encoding="utf-8")
        return ClaudeResult(
            session_id=session_id,
            transcript=transcript,
            injections=_read_injections(transcript),
            tool_calls=_read_tool_calls(transcript),
        )

    return _run


def _grafana(path: str) -> object:
    """Grafana の API を管理者認証で叩いて JSON を返す。"""
    request = urllib.request.Request(
        f"{GRAFANA_URL}{path}", headers={"Authorization": f"Basic {GRAFANA_AUTH}"}
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read())


@pytest.fixture(scope="session")
def observability_stack() -> None:
    """観測基盤（Collector + Loki + Grafana）を起動して受付開始まで待つ。"""
    if shutil.which("docker") is None:
        pytest.skip("docker が PATH にない")
    if not COMPOSE_FILE.exists():
        pytest.skip(f"{COMPOSE_FILE} が無い（observability リポジトリを同階層にクローンする）")
    completed = subprocess.run(
        ["docker", "compose", "-f", str(COMPOSE_FILE), "up", "-d"],
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    if completed.returncode != 0:
        pytest.skip(f"観測基盤を起動できない:\n{completed.stderr[-2000:]}")
    # 起動直後は Grafana がまだ受け付けないので、認証付きの API が通るまで待つ
    deadline = time.time() + STACK_READY_TIMEOUT_SEC
    while time.time() < deadline:
        try:
            _grafana("/api/datasources")
            return
        except urllib.error.HTTPError as error:
            # 既存ボリュームが残っていると compose の管理者パスワードは反映されない
            if error.code == 401:
                pytest.fail(
                    "Grafana の管理者認証に失敗した。"
                    " docker exec observability-grafana grafana cli"
                    " --homepath /usr/share/grafana admin reset-admin-password admin"
                    " で既定に戻す"
                )
            time.sleep(2)
        except (urllib.error.URLError, TimeoutError):
            time.sleep(2)
    pytest.fail(f"Grafana が {STACK_READY_TIMEOUT_SEC} 秒以内に応答しない")


@pytest.fixture(scope="session")
def datasource_uid(observability_stack) -> str:
    """Grafana にプロビジョニングされた Loki datasource の UID を返す。"""
    datasources = _grafana("/api/datasources")
    loki = next((d for d in datasources if d["type"] == "loki"), None)
    if loki is None:
        pytest.fail("Loki datasource がプロビジョニングされていない")
    return loki["uid"]


@pytest.fixture
def query_logs(datasource_uid):
    """Grafana 経由で LogQL を投げ、指定時刻以降のログ行を返す factory。"""

    def _query(logql: str, *, since: float, timeout_sec: int = 60) -> list[str]:
        deadline = time.time() + timeout_sec
        while True:
            params = urllib.parse.urlencode(
                {
                    "query": logql,
                    "start": int(since * 1_000_000_000),
                    "end": int(time.time() * 1_000_000_000),
                    "limit": 100,
                }
            )
            result = _grafana(
                f"/api/datasources/proxy/uid/{datasource_uid}/loki/api/v1/query_range?{params}"
            )
            streams = result["data"]["result"]
            lines = [value[1] for stream in streams for value in stream["values"]]
            if lines or time.time() >= deadline:
                return lines
            time.sleep(2)

    return _query
