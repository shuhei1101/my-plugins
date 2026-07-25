"""`main.py` の単体テスト。"""
from __future__ import annotations

import io
import json
import threading
import time
import urllib.error
from pathlib import Path

from inject_rules.features.rules.types import RuleDefinition
from inject_rules.features.session.store import load_state, save_state
from inject_rules.features.session.types import SessionState
from inject_rules.main import _build_blocks, _read_input, clear, inject_conventions, main

SESSION = "9f2c1b"
INDEX_URL = "https://example.com/rules.yaml"
A = "https://example.com/a.md"
B = "https://example.com/b.md"
C = "https://example.com/c.md"
FILE_PATH = "/repo/src/a.py"
CWD = "/repo"


def _payload(
    *,
    tool_name: str = "Read",
    file_path: str | None = FILE_PATH,
    session_id: str | None = SESSION,
    cwd: str | None = CWD,
) -> str:
    """フックのペイロード JSON を組み立てる。"""
    body: dict[str, object] = {"tool_name": tool_name}
    if session_id is not None:
        body["session_id"] = session_id
    if cwd is not None:
        body["cwd"] = cwd
    body["tool_input"] = {"file_path": file_path} if file_path is not None else {}
    return json.dumps(body)


def _stdin(monkeypatch, text: str) -> None:
    """標準入力を差し替える。"""
    monkeypatch.setattr("sys.stdin", io.StringIO(text))


def _stdout_json(capsys) -> dict | None:
    """標準出力の JSON を返す（空なら None）。"""
    out = capsys.readouterr().out.strip()
    return json.loads(out) if out else None


# =========================
# _read_input
# =========================


def test_read_input():
    """全フィールドの変換（正常系）。"""
    # 実行
    hook_input = _read_input(_payload())
    # 検証
    assert hook_input.session_id == SESSION
    assert hook_input.tool_name == "Read"
    assert hook_input.file_path == FILE_PATH
    assert hook_input.cwd == Path(CWD)


def test_read_input_when_session_id_missing():
    """セッション ID 既定値（正常系）。"""
    # 実行
    hook_input = _read_input(_payload(session_id=None))
    # 検証
    assert hook_input.session_id == "default"


def test_read_input_when_file_path_missing():
    """対象パスなし（正常系）。"""
    # 実行・検証
    assert _read_input(_payload(file_path=None)) is None


def test_read_input_when_broken_json():
    """壊れた JSON（正常系）。"""
    # 実行・検証: 例外を投げない
    assert _read_input("{壊れている") is None


# =========================
# _build_blocks
# =========================


def test_build_blocks(fetch_stub):
    """全件の組み立て（正常系）。"""
    # 準備
    rules = [
        RuleDefinition(url=A, patterns=("**/*.py",)),
        RuleDefinition(url=B, patterns=("**/*.md",)),
    ]
    fetch = fetch_stub({A: "本文 A", B: "本文 B"})
    # 実行
    blocks = _build_blocks(rules, state=SessionState(), fetch=fetch)
    # 検証: 並列取得でも順序が入れ替わらない
    assert [b.url for b in blocks] == [A, B]
    assert [b.body for b in blocks] == ["本文 A", "本文 B"]


def test_build_blocks_when_offset(fetch_stub):
    """続き位置の反映（正常系）。"""
    # 準備: 続き位置 100 を記録した状態
    rules = [RuleDefinition(url=A, patterns=("**/*.py",))]
    state = SessionState()
    state.mark_partial(A, 100)
    fetch = fetch_stub({A: "あ" * 300})
    # 実行
    blocks = _build_blocks(rules, state=state, fetch=fetch)
    # 検証: 本文が 100 文字目以降になる
    assert blocks[0].body == "あ" * 200
    assert blocks[0].offset == 100


def test_build_blocks_when_fetch_failed(fetch_stub):
    """取得失敗の除外（正常系）。"""
    # 準備: 2 件中 1 件が例外
    rules = [
        RuleDefinition(url=A, patterns=("**/*.py",)),
        RuleDefinition(url=B, patterns=("**/*.py",)),
    ]
    fetch = fetch_stub({B: "本文 B"}, errors={A: urllib.error.URLError("接続できません")})
    # 実行
    blocks = _build_blocks(rules, state=SessionState(), fetch=fetch)
    # 検証: 次回再試行のため注入済みにしない
    assert [b.url for b in blocks] == [B]


def test_build_blocks_when_parallel():
    """並列取得（正常系）。"""
    # 準備: 待機する取得関数を 3 件分（呼び出し時刻を記録する）
    rules = [RuleDefinition(url=url, patterns=("**/*.py",)) for url in (A, B, C)]
    lock = threading.Lock()
    started: list[float] = []
    finished: list[float] = []

    def _slow_fetch(url: str) -> str:
        with lock:
            started.append(time.monotonic())
        time.sleep(0.1)
        with lock:
            finished.append(time.monotonic())
        return f"本文 {url}"

    # 実行
    _build_blocks(rules, state=SessionState(), fetch=_slow_fetch)
    # 検証: 直列だと件数分の待ち時間になるため、3 件の取得が重なって実行される
    assert max(started) < min(finished)


# =========================
# main
# =========================


def test_main(monkeypatch, capsys, tmp_dirs, rule_index, fetch_stub):
    """1 回で収まる注入（正常系）。"""
    # 準備: マッチするルール 1 件
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    fetch = fetch_stub({INDEX_URL: rule_index([(A, ["**/*.py"])]), A: "命名規約の本文"})
    monkeypatch.setattr("inject_rules.main.fetch_text", fetch)
    _stdin(monkeypatch, _payload())
    # 実行
    code = main()
    # 検証
    assert code == 0
    response = _stdout_json(capsys)
    assert response["hookSpecificOutput"]["permissionDecision"] == "allow"


def test_main_when_not_target_tool(monkeypatch, capsys, tmp_dirs, rule_index, fetch_stub):
    """対象外ツールの無処理（正常系）。"""
    # 準備
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    fetch = fetch_stub({INDEX_URL: rule_index([(A, ["**/*.py"])]), A: "命名規約の本文"})
    monkeypatch.setattr("inject_rules.main.fetch_text", fetch)
    _stdin(monkeypatch, _payload(tool_name="Edit"))
    # 実行
    main()
    # 検証: 取得が発生しない
    assert _stdout_json(capsys) is None
    assert fetch.calls == []


def test_main_when_indexes_unset(monkeypatch, capsys, tmp_dirs):
    """注入元未設定（正常系）。"""
    # 準備: 環境変数を削除し、ログ送出を記録する
    monkeypatch.delenv("INJECT_RULES_INDEXES", raising=False)
    logs: list[tuple] = []
    monkeypatch.setattr("inject_rules.main.emit_log", lambda *a, **kw: logs.append((a, kw)))
    _stdin(monkeypatch, _payload())
    # 実行
    main()
    # 検証
    assert _stdout_json(capsys) is None
    assert len(logs) == 1


def test_main_when_indexes_unset_twice(monkeypatch, capsys, tmp_dirs):
    """通知の抑制（正常系）。"""
    # 準備: 同一セッション ID で 2 回実行する
    monkeypatch.delenv("INJECT_RULES_INDEXES", raising=False)
    logs: list[tuple] = []
    monkeypatch.setattr("inject_rules.main.emit_log", lambda *a, **kw: logs.append((a, kw)))
    # 実行
    _stdin(monkeypatch, _payload())
    main()
    _stdin(monkeypatch, _payload())
    main()
    # 検証: ログ送出が 1 回だけ
    assert len(logs) == 1


def test_main_when_index_missing(monkeypatch, capsys, tmp_dirs, fetch_stub):
    """索引が取得できない（正常系）。"""
    # 準備: 取得関数が URLError を投げる
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    fetch = fetch_stub({}, errors={INDEX_URL: urllib.error.URLError("見つかりません")})
    monkeypatch.setattr("inject_rules.main.fetch_text", fetch)
    logs: list[tuple] = []
    monkeypatch.setattr("inject_rules.main.emit_log", lambda *a, **kw: logs.append((a, kw)))
    _stdin(monkeypatch, _payload())
    # 実行
    main()
    # 検証
    assert _stdout_json(capsys) is None
    assert len(logs) == 1


def test_main_when_no_match(monkeypatch, capsys, tmp_dirs, rule_index, fetch_stub):
    """マッチなし（正常系）。"""
    # 準備: 編集対象にマッチしない glob だけの索引
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    fetch = fetch_stub({INDEX_URL: rule_index([(A, ["**/*.md"])]), A: "命名規約の本文"})
    monkeypatch.setattr("inject_rules.main.fetch_text", fetch)
    _stdin(monkeypatch, _payload())
    # 実行
    main()
    # 検証
    assert _stdout_json(capsys) is None


def test_main_when_already_injected(monkeypatch, capsys, tmp_dirs, rule_index, fetch_stub):
    """注入済みの無処理（正常系）。"""
    # 準備: セッションに注入済み記録を持たせる
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    state = SessionState()
    state.mark_injected(A)
    save_state(SESSION, state, base_dir=tmp_dirs.session)
    fetch = fetch_stub({INDEX_URL: rule_index([(A, ["**/*.py"])]), A: "命名規約の本文"})
    monkeypatch.setattr("inject_rules.main.fetch_text", fetch)
    _stdin(monkeypatch, _payload())
    # 実行
    main()
    # 検証: 再注入を抑止する
    assert _stdout_json(capsys) is None


def test_main_when_over_limit(monkeypatch, capsys, tmp_dirs, rule_index, fetch_stub):
    """上限超過の差し戻し（正常系）。"""
    # 準備: 上限を超える本文
    monkeypatch.setenv("INJECT_RULES_INDEXES", INDEX_URL)
    fetch = fetch_stub({INDEX_URL: rule_index([(A, ["**/*.py"])]), A: "あ" * 20000})
    monkeypatch.setattr("inject_rules.main.fetch_text", fetch)
    _stdin(monkeypatch, _payload())
    # 実行
    main()
    # 検証: 続き位置が保存される
    response = _stdout_json(capsys)
    assert response["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert load_state(SESSION, base_dir=tmp_dirs.session).offset_of(A) > 0


def test_main_when_broken_stdin(monkeypatch, capsys, tmp_dirs):
    """壊れた入力（正常系）。"""
    # 準備
    _stdin(monkeypatch, "{壊れている")
    # 実行
    code = main()
    # 検証
    assert code == 0
    assert _stdout_json(capsys) is None


# =========================
# clear
# =========================


def test_clear(monkeypatch, tmp_dirs):
    """注入済み記録の破棄（正常系）。"""
    # 準備: 保存済みのセッション
    state = SessionState()
    state.mark_injected(A)
    save_state(SESSION, state, base_dir=tmp_dirs.session)
    _stdin(monkeypatch, json.dumps({"session_id": SESSION}))
    # 実行
    code = clear()
    # 検証
    assert code == 0
    assert load_state(SESSION, base_dir=tmp_dirs.session).injected == set()


def test_clear_when_broken_stdin(monkeypatch, tmp_dirs):
    """壊れた入力（正常系）。"""
    # 準備
    _stdin(monkeypatch, "{壊れている")
    # 実行・検証: 例外を投げない
    assert clear() == 0


# =========================
# inject_conventions
# =========================


def test_inject_conventions(capsys):
    """作業規約の出力（正常系）。"""
    # 実行
    code = inject_conventions()
    # 検証
    assert code == 0
    output = _stdout_json(capsys)["hookSpecificOutput"]
    assert output["hookEventName"] == "SessionStart"
    assert "新規ファイルの作成手順" in output["additionalContext"]
