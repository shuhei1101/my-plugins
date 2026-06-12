"""Stop フック: 保留中の /reload-plugins を自セッションへ遅延送信する。

reload_plugins.py が自セッション宛に書いた保留トークン
（~/.claude/tokens/work/reload-pending/<tmux_session>）を消費し、
ターン終了後に入力が空くタイミングを狙ってバックグラウンドで send-keys する。
トークンがなければ何もしない。
"""
from __future__ import annotations

import os
import pathlib
import subprocess

PENDING_DIR = pathlib.Path.home() / ".claude" / "tokens" / "work" / "reload-pending"

# Stop フック完了 → 入力欄がアイドルに戻るまでの猶予秒数
SEND_DELAY_SECONDS = 3


def main() -> None:
    """保留トークンがあれば消費し、遅延 send-keys をバックグラウンドで仕込む。"""
    # tmux 外では何もしない
    if not os.environ.get("TMUX"):
        return

    result = subprocess.run(
        ["tmux", "display-message", "-p", "#{session_name}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return
    session = result.stdout.strip()

    token = PENDING_DIR / session
    if not token.is_file():
        return
    token.unlink()

    # Stop フックをブロックしないよう、デタッチしたバックグラウンドプロセスで遅延送信する
    subprocess.Popen(
        ["bash", "-c", f"sleep {SEND_DELAY_SECONDS}; tmux send-keys -t {session} /reload-plugins Enter"],
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


if __name__ == "__main__":
    main()
