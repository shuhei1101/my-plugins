"""PostToolUse フック: git push origin master 後に tools/reload_plugins.py を実行する。

責務:
  - post-merge-upgrade.py … git merge 完了後に reload_plugins を実行
  - このフック          … git push origin master 完了後に reload_plugins を実行

pr-review スキルは git merge → worktree_remove → git push origin master の順で動く。
push 完了のタイミングでプラグインキャッシュを更新することで、
gh CLI 経由マージ後も確実に reload_plugins が走るようにする。
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

# git push origin master / git push origin main のみ対象
if not re.search(r"\bgit\s+push\s+(?:origin\s+)?(?:master|main)\b", cmd):
    sys.exit(0)

# push 失敗時はスキップ
response = str(d.get("tool_response") or "")
if d.get("exit_code", 0) != 0:
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

# reload_plugins.py を直接呼び出す
result = subprocess.run(
    [sys.executable, f"{REPO_ROOT}/tools/reload_plugins.py"],
    cwd=REPO_ROOT, capture_output=True, text=True, check=False,
)

report_parts: list[str] = []
if result.stdout.strip():
    report_parts.append(result.stdout.strip())
if result.stderr.strip():
    report_parts.append(f"### reload_plugins.py stderr\n\n```\n{result.stderr.strip()}\n```")
if result.returncode != 0:
    report_parts.append(f"### reload_plugins.py exited with rc={result.returncode}")

if not report_parts:
    sys.exit(0)

output = {
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "\n\n".join(report_parts),
    },
}
sys.stdout.buffer.write(json.dumps(output, ensure_ascii=False).encode("utf-8"))
