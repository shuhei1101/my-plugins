"""PostToolUse フック: master マージ後アップグレードのシン・ラッパー。

ビジネスロジックは tools/post_merge_upgrade.py に委譲する。
"""
import sys
import json
import re
import subprocess
import pathlib

REPO_ROOT = pathlib.Path(__file__).parent.parent.parent

raw = "" if sys.stdin.isatty() else sys.stdin.read()
d = json.loads(raw) if raw.strip() else {}

# フックとして起動された場合のみ条件チェックする
if d:
    if d.get("tool_name") != "Bash":
        sys.exit(0)

    cmd = (d.get("tool_input") or {}).get("command", "") or ""

    if not re.search(r"\bgit\s+merge\b", cmd):
        sys.exit(0)

    # master/main を取り込む操作はスキップ
    if re.search(r"\bgit\s+merge\s+(origin/)?(master|main)\b", cmd):
        sys.exit(0)

    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    ).stdout.strip()
    if branch != "master":
        sys.exit(0)

    # コンフリクトがあればスキップ
    if "CONFLICT" in str(d.get("tool_response") or ""):
        sys.exit(0)

# ビジネスロジックを tools/post_merge_upgrade.py に委譲
subprocess.run(
    [sys.executable, str(REPO_ROOT / "tools" / "post_merge_upgrade.py")],
    cwd=REPO_ROOT, check=False,
)
