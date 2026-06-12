"""
PostToolUse フック: master へのマージ後に push + marketplace upgrade + reload-plugins を実行。

処理の流れ:
  1. git push origin master
  2. python tools/marketplace.py upgrade
  3. ait-1〜10 / plg-1〜10 の起動中 tmux セッションに /reload-plugins を送信
"""
import sys
import json
import re
import subprocess
import pathlib
import time

REPO_ROOT = pathlib.Path(__file__).parent.parent.parent

# TTY から直接実行された場合は空の入力として扱う（stdin 待ちで固まるのを防ぐ）
raw = "" if sys.stdin.isatty() else sys.stdin.read()
d = json.loads(raw) if raw.strip() else {}

direct_run = not d  # stdin なし（TTY 直接実行）の場合は True

if not direct_run:
    # フックとして起動された場合のみ以下のチェックを行う
    if d.get("tool_name") != "Bash":
        sys.exit(0)

    cmd = (d.get("tool_input") or {}).get("command", "") or ""

    if not re.search(r"\bgit\s+merge\b", cmd):
        sys.exit(0)

    # master/main を取り込む操作（git merge origin/master など）はスキップ
    if re.search(r"\bgit\s+merge\s+(origin/)?(master|main)\b", cmd):
        sys.exit(0)

    # 現在のブランチが master でなければスキップ
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    ).stdout.strip()
    if branch != "master":
        sys.exit(0)

    # コンフリクトがあればスキップ
    if "CONFLICT" in str(d.get("tool_response") or ""):
        sys.exit(0)

# 1. master を push
# WSL から HTTPS push は認証できないため Windows 側の git.exe を使う
_git_cmd = ["git.exe", "push", "origin", "master"] if sys.platform != "win32" else ["git", "push", "origin", "master"]
subprocess.run(_git_cmd, cwd=REPO_ROOT, check=False)

# push が GitHub に反映されるまで待機
time.sleep(2)

# 2. marketplace upgrade
subprocess.run(
    [sys.executable, str(REPO_ROOT / "tools" / "marketplace.py"), "upgrade"],
    cwd=REPO_ROOT, check=False,
)

# 3. 起動中の tmux セッションに /reload-plugins を送信
subprocess.run(
    [sys.executable, str(REPO_ROOT / "tools" / "reload_plugins.py")],
    cwd=REPO_ROOT,
    check=False,
)
