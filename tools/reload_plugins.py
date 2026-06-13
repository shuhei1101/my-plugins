"""起動中の tmux セッション (ait-0〜10 / plg-1〜10) に /reload-plugins を送信する。

送信前に marketplace.py upgrade を実行してキャッシュを最新に更新する。
自分自身が動いているセッションはターン処理中で入力を取りこぼすため、
即時送信せず保留トークンを書く。Stop フック（reload_deferred.py）が
ターン終了時にトークンを消費して遅延送信する。

# 実行方法
python tools/reload_plugins.py
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SESSIONS = [f"ait-{i}" for i in range(0, 11)] + [f"plg-{i}" for i in range(1, 11)]
PENDING_DIR = Path.home() / ".claude" / "tokens" / "work" / "reload-pending"


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
    """起動中のセッションに /reload-plugins を送信する（自セッションは保留トークン化）。"""
    ls = subprocess.run(
        ["tmux", "ls", "-F", "#{session_name}"],
        capture_output=True,
        text=True,
    )
    # tmux が起動していない場合はスキップ
    if ls.returncode != 0:
        return

    active = set(ls.stdout.strip().splitlines())
    own = _own_session()
    for session in SESSIONS:
        if session not in active:
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
