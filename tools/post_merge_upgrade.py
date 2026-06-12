"""マージ後アップグレード: push + marketplace upgrade + reload-plugins を実行する。

# 使い方
python tools/post_merge_upgrade.py
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_post_merge_upgrade() -> None:
    """push + marketplace upgrade + reload-plugins を順に実行する。"""
    # WSL から HTTPS push は認証できないため Windows 側の git.exe を使う
    git_cmd = ["git.exe", "push", "origin", "master"] if sys.platform != "win32" else ["git", "push", "origin", "master"]
    subprocess.run(git_cmd, cwd=REPO_ROOT, check=False)

    # push が GitHub に反映されるまで待機
    time.sleep(2)

    # marketplace upgrade
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "marketplace.py"), "upgrade"],
        cwd=REPO_ROOT, check=False,
    )

    # 起動中の tmux セッションに /reload-plugins を送信
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "reload_plugins.py")],
        cwd=REPO_ROOT, check=False,
    )


def main() -> int:
    """エントリポイント。"""
    run_post_merge_upgrade()
    return 0


if __name__ == "__main__":
    sys.exit(main())
