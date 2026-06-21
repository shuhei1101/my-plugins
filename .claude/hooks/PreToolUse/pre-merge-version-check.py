"""PreToolUse フック: master マージ前バージョンチェックのシン・ラッパー。

ビジネスロジックは tools/pre_merge_check.py に委譲する。
"""
import sys
import json
import re
import subprocess

raw = "" if sys.stdin.isatty() else sys.stdin.read()
d = json.loads(raw) if raw.strip() else {}

if d.get("tool_name") != "Bash":
    sys.exit(0)

cmd = (d.get("tool_input") or {}).get("command", "") or ""

if not re.search(r"\bgit\s+merge\b", cmd):
    sys.exit(0)

# master/main を取り込む操作はスキップ
if re.search(r"\bgit\s+merge\s+(origin/)?(master|main)\b", cmd):
    sys.exit(0)

# REPO_ROOT を git rev-parse で動的解決（worktree 対応）
repo_root_result = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"],
    capture_output=True, text=True,
)
if repo_root_result.returncode != 0:
    sys.exit(0)
REPO_ROOT = repo_root_result.stdout.strip()

# master ブランチ上でなければスキップ
branch = subprocess.run(
    ["git", "branch", "--show-current"],
    capture_output=True, text=True, cwd=REPO_ROOT,
).stdout.strip()
if branch != "master":
    sys.exit(0)

m = re.search(r"\bgit\s+merge\s+([^\s;|&]+)", cmd)
if not m:
    sys.exit(0)

# ビジネスロジックを tools/pre_merge_check.py に委譲
result = subprocess.run(
    [sys.executable, f"{REPO_ROOT}/tools/pre_merge_check.py", m.group(1)],
    capture_output=True, text=True, cwd=REPO_ROOT,
)

if not result.stdout.strip():
    sys.exit(0)

output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "additionalContext": result.stdout,
    },
}
sys.stdout.buffer.write(json.dumps(output, ensure_ascii=False).encode("utf-8"))
