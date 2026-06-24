#!/usr/bin/env python3
"""issue-review-daemon.py

「確認:issue-reviewer」ラベル付き Issue を claude -p で直列処理するデーモン。

使い方:
    ./issue-review-daemon.py

環境変数（オプション、上書き用）:
    POLL_INTERVAL       ポーリング間隔（秒）[デフォルト: 30]
    LOCK_FILE           flock に使うロックファイルパス [デフォルト: $TMPDIR/gh-kit-issue-review.lock]
    TMPDIR              一時ディレクトリ（POSIX 標準）。LOCK_FILE のデフォルトパス算出に使用。
                        未設定なら Python の tempfile.gettempdir() が /tmp 等を返す。

    constants.sh から動的注入される定数: _load_constants_sh() 参照
"""

from __future__ import annotations

import fcntl
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

# plugins/gh-kit/scripts/monitor/issue-review-daemon.py から見て親の親の親が gh-kit プラグインルート
GH_KIT_PLUGIN_DIR = str(Path(__file__).resolve().parent.parent.parent)


def _load_env_file(path: Path) -> None:
    """gh_monitor.env が存在すれば os.environ に読み込む（外部 export 済みを優先）。"""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip()


def _load_constants_sh(target: dict[str, object]) -> None:
    """hooks/session-start/constants.sh の export 行を target 名前空間に注入する。

    target には通常 globals() を渡し、constants.sh の定数名（GH_KIT_LABEL_*）
    がそのままモジュールトップレベル変数として参照可能になる。
    定数の再定義（Python 側で名前を付け直す）を不要にし、constants.sh を SoT に統一する。
    既に os.environ に値があれば（外部 export 済み）そちらを優先。
    """
    constants_path = Path(GH_KIT_PLUGIN_DIR) / "hooks" / "session-start" / "constants.sh"
    if not constants_path.is_file():
        # フォールバックは設けない: 必須ファイルが無ければ起動を中止
        raise FileNotFoundError(f"constants.sh が見つかりません: {constants_path}")
    for raw in constants_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        # export VAR=VALUE 形式のみ取り込む（コメント・空行・shebang・その他は無視）
        if not line.startswith("export "):
            continue
        body = line[len("export ") :]
        if "=" not in body:
            continue
        key, value = body.split("=", 1)
        # 外部 env を優先し、無ければ constants.sh の値を採用
        target[key] = os.environ.get(key, value)


# カレントディレクトリの gh_monitor.env を優先して読み込む（外部 export 済みを優先）。
_load_env_file(Path.cwd() / "gh_monitor.env")

# constants.sh の定数を本モジュールのトップレベルに注入。
# これにより GH_KIT_LABEL_CONFIRM_ISSUE_REVIEW などが定数名そのままで使える。
_load_constants_sh(globals())

POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "30"))
LOCK_FILE = os.environ.get(
    "LOCK_FILE",
    str(Path(os.environ.get("TMPDIR", tempfile.gettempdir())) / "gh-kit-issue-review.lock"),
)

# 優先度ソート時のランク（数値が小さいほど先に処理）
PRIORITY_RANK_URGENT = 0
PRIORITY_RANK_LOW = 1
PRIORITY_RANK_NORMAL = 2

def log(msg: str) -> None:
    """タイムスタンプ付きで stderr にログ 1 行を出力する。"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr, flush=True)


def die(msg: str) -> None:
    """エラーログを出力して exit code 1 で終了する。"""
    log(f"ERROR: {msg}")
    sys.exit(1)


def preflight() -> None:
    """起動前に外部コマンド（claude / gh）の存在を検証する。"""
    for tool in ("claude", "gh"):
        if shutil.which(tool) is None:
            die(f"{tool!r} が見つかりません。インストールされているか確認してください。")


def find_next_issue() -> int | None:
    """確認:issue-reviewer ラベル付きで処理中ではない次の Issue 番号を返す（なければ None）。"""
    result = subprocess.run(
        [
            "gh", "issue", "list",
            "--state", "open",
            "--label", GH_KIT_LABEL_CONFIRM_ISSUE_REVIEW,  # noqa: F821 — constants.sh から動的注入
            "--json", "number,labels",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        log(f"WARN: gh issue list が失敗しました (exit={result.returncode}): {result.stderr.strip()}")
        log("  git リポジトリ内で実行してください")
        return None
    issues = json.loads(result.stdout)

    def is_not_processing(issue: dict) -> bool:
        """Issue に 処理中:* ラベルが付いていないかを判定する。"""
        return not any(
            lbl["name"].startswith(GH_KIT_LABEL_PROCESSING_PREFIX) for lbl in issue.get("labels", [])
        )

    def priority_key(issue: dict) -> tuple[int, int]:
        """ソート用キー（優先度ランク, Issue 番号）を返す。同ランクは古い番号順。"""
        names = [lbl["name"] for lbl in issue.get("labels", [])]
        # 急ぎラベルあり: 最優先で処理
        if GH_KIT_LABEL_PRIORITY_URGENT in names:  # noqa: F821 — constants.sh から動的注入
            rank = PRIORITY_RANK_URGENT
        # いつでもラベルあり: 最劣後（他にネタが無いときだけ処理）
        elif GH_KIT_LABEL_PRIORITY_LOW in names:  # noqa: F821 — constants.sh から動的注入
            rank = PRIORITY_RANK_LOW
        # 優先度ラベルなし: 通常扱い
        else:
            rank = PRIORITY_RANK_NORMAL
        return (rank, issue["number"])

    candidates = [i for i in issues if is_not_processing(i)]
    if not candidates:
        return None
    candidates.sort(key=priority_key)
    return candidates[0]["number"]


def add_label(issue_number: int, label: str) -> bool:
    """Issue にラベルを付与し、gh の exit code が 0 なら True を返す。"""
    return subprocess.run(
        ["gh", "issue", "edit", str(issue_number), "--add-label", label],
        capture_output=True,
    ).returncode == 0


def remove_label(issue_number: int, label: str) -> None:
    """Issue からラベルを除去する（失敗しても戻り値で通知しない）。"""
    subprocess.run(
        ["gh", "issue", "edit", str(issue_number), "--remove-label", label],
        capture_output=True,
    )


def run_ai_review(issue_number: int) -> int:
    """AI CLI に /gh-kit:issue-review を投げ、出力を stderr にミラーして exit code を返す。"""
    cmd = [
        "claude", "-p", f"/gh-kit:issue-review {issue_number}",
        "--plugin-dir", GH_KIT_PLUGIN_DIR,
        "--permission-mode", "dontAsk",
        "--allowedTools", "Bash,Read,Edit,Write,WebFetch",
        "--output-format", "json",
        "--no-session-persistence",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    assert proc.stdout is not None
    for line in proc.stdout:
        sys.stderr.write(line)
        sys.stderr.flush()
    return proc.wait()


def review_issue(issue_number: int) -> None:
    """1 件の Issue に対し、処理中ラベル付与・flock 取得・AI レビューを実行する。"""
    log(f"Issue #{issue_number} のレビューを開始します")

    # noqa: F821 — GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER は constants.sh から動的注入
    if not add_label(issue_number, GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER):  # noqa: F821
        log(f"WARN: 処理中ラベルの付与に失敗しました（Issue #{issue_number}）")

    try:
        lock_fd = os.open(LOCK_FILE, os.O_CREAT | os.O_WRONLY, 0o644)
        try:
            # 別インスタンスの並走を防ぐため非ブロッキングで排他ロックを取る
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                # 別インスタンスがロックを保持中: 今回はスキップして次回ポーリングに任せる
                log(f"SKIP: ロック取得失敗 — 別インスタンスが実行中です（Issue #{issue_number}）")
                return

            exit_code = run_ai_review(issue_number)

            if exit_code != 0:
                # AI CLI が異常終了: ラベルを戻してキュー再投入させる
                log(
                    f"ERROR: claude -p が異常終了しました"
                    f"（Issue #{issue_number}, exit_code={exit_code}）"
                )
                log("  処理中ラベルを除去してキューに戻します")
                return

            log(f"Issue #{issue_number} のレビューが完了しました（exit_code={exit_code}）")
        finally:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            except OSError:
                pass
            os.close(lock_fd)
    finally:
        remove_label(issue_number, GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER)  # noqa: F821


def main() -> int:
    """デーモン本体: ポーリング → 次 Issue 取得 → レビュー実行を繰り返す。"""
    preflight()

    log("issue-review-daemon 起動")
    log(f"  GH_KIT_PLUGIN_DIR={GH_KIT_PLUGIN_DIR}")
    log(f"  POLL_INTERVAL={POLL_INTERVAL}s")
    log(f"  LOCK_FILE={LOCK_FILE}")
    log(f"ポーリング開始（間隔: {POLL_INTERVAL}s）")

    while True:
        try:
            issue_number = find_next_issue()
            if issue_number is not None:
                review_issue(issue_number)
            else:
                log(f"対象 Issue なし — {POLL_INTERVAL}s 待機")
        except Exception as exc:
            log(f"ERROR: ポーリング中に例外が発生しました: {exc}")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("SIGINT を受信しました。終了します。")
        sys.exit(130)
