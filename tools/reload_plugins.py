"""起動中の全 tmux セッションに /reload-plugins を送信する。

送信前に marketplace.py upgrade を実行してキャッシュを最新に更新する。
自分自身が動いているセッションはターン処理中で入力を取りこぼすため、
即時送信せず保留トークンを書く。Stop フック（reload_deferred.py）が
ターン終了時にトークンを消費して遅延送信する。

BLACKLIST_KEYWORDS のいずれかに glob パターンマッチするセッション名は除外する。
例: ["*server*"] → "test-server-1" のようなセッションをスキップ

# 実行方法
python tools/reload_plugins.py
"""
from __future__ import annotations

import fnmatch
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ブラックリスト: glob パターンにマッチするセッション名は /reload-plugins を送信しない
# 例: "*server*" → セッション名に "server" を含むものを除外
BLACKLIST_KEYWORDS: list[str] = [
    "*server*",
]

PENDING_DIR = Path.home() / ".claude" / "tokens" / "work" / "reload-pending"


def _is_blacklisted(session: str) -> bool:
    """セッション名がブラックリストの glob パターンにマッチするか判定する。"""
    return any(fnmatch.fnmatch(session, pattern) for pattern in BLACKLIST_KEYWORDS)


def _own_session() -> str | None:
    """自分が動いている tmux セッション名を返す（tmux 外なら None）。"""
    if not os.environ.get("TMUX"):
        return None
    result = subprocess.run(
        ["tmux", "display-message", "-p", "#{session_name}"],
        capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def upgrade() -> None:
    """marketplace.py upgrade を実行してキャッシュを最新バージョンに更新する。"""
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "marketplace.py"), "upgrade"],
        cwd=REPO_ROOT, check=False,
    )


def reload_plugins() -> None:
    """起動中の全セッションに /reload-plugins を送信する（自セッションは保留トークン化）。"""
    ls = subprocess.run(
        ["tmux", "ls", "-F", "#{session_name}"],
        capture_output=True,
        text=True,
    )
    # tmux が起動していない場合はスキップ
    if ls.returncode != 0:
        return

    active = ls.stdout.strip().splitlines()
    own = _own_session()
    for session in active:
        # ブラックリストにマッチするセッションはスキップ
        if _is_blacklisted(session):
            print(f"スキップ（ブラックリスト）: {session}")
            continue
        # 自セッションはターン処理中のため即時送信せず、Stop フックに委ねる
        if session == own:
            PENDING_DIR.mkdir(parents=True, exist_ok=True)
            (PENDING_DIR / session).touch()
            print(f"自セッション {session} は保留 — ターン終了時に /reload-plugins を遅延実行します")
            continue
        subprocess.run(
            ["tmux", "send-keys", "-t", session, "/reload-plugins", "Enter"],
            check=False,
        )


def main() -> int:
    """エントリポイント。"""
    upgrade()
    reload_plugins()
    return 0


if __name__ == "__main__":
    sys.exit(main())
