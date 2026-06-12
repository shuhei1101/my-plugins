"""起動中の tmux セッション (ait-0〜10 / plg-1〜10) に /reload-plugins を送信する。

# 実行方法
python tools/reload_plugins.py
"""
from __future__ import annotations

import subprocess
import sys

SESSIONS = [f"ait-{i}" for i in range(0, 11)] + [f"plg-{i}" for i in range(1, 11)]


def reload_plugins() -> None:
    """起動中のセッションを検出し、/reload-plugins コマンドを送信する。"""
    ls = subprocess.run(
        ["tmux", "ls", "-F", "#{session_name}"],
        capture_output=True,
        text=True,
    )
    # tmux が起動していない場合はスキップ
    if ls.returncode != 0:
        return

    active = set(ls.stdout.strip().splitlines())
    for session in SESSIONS:
        # 対象セッションが起動中であれば送信
        if session in active:
            subprocess.run(
                ["tmux", "send-keys", "-t", session, "/reload-plugins", "Enter"],
                check=False,
            )


def main() -> int:
    """エントリポイント。"""
    reload_plugins()
    return 0


if __name__ == "__main__":
    sys.exit(main())
