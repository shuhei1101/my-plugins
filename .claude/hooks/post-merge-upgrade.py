"""PostToolUse フック: master マージ後に tools/post_merge_upgrade.py を実行する。

サブステップの結果（push / marketplace upgrade / reload-plugins）は post_merge_upgrade.py が
stdout にレポートとして出力する。それを `hookSpecificOutput.additionalContext` で会話に注入し、
silent fail を防ぐ。
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

# サブステップを実行し、stdout を取得して会話に注入する
result = subprocess.run(
    [sys.executable, str(REPO_ROOT / "tools" / "post_merge_upgrade.py")],
    cwd=REPO_ROOT, capture_output=True, text=True, check=False,
)

report_parts: list[str] = []
if result.stdout.strip():
    report_parts.append(result.stdout.strip())
if result.stderr.strip():
    report_parts.append(f"### post_merge_upgrade.py stderr\n\n```\n{result.stderr.strip()}\n```")
if result.returncode != 0:
    report_parts.append(f"### post_merge_upgrade.py exited with rc={result.returncode}")

if not report_parts:
    sys.exit(0)

# フックとして呼ばれた場合は PostToolUse の additionalContext、直接実行時はそのまま print
if d:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": "\n\n".join(report_parts),
        },
    }
    sys.stdout.buffer.write(json.dumps(output, ensure_ascii=False).encode("utf-8"))
else:
    print("\n\n".join(report_parts))
