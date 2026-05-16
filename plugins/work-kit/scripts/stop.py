#!/usr/bin/env python3
"""
Stop hook: remind Claude to update completed tasks in the PR doc.
Injects a reminder into context when unchecked tasks exist in the current PR.
Does not block (no decision: block) to avoid infinite loops on partial work.
"""
import json
import re
import subprocess
import sys
from pathlib import Path


def get_git_branch() -> str:
    return subprocess.check_output(
        ["git", "branch", "--show-current"],
        text=True,
        stderr=subprocess.DEVNULL,
        timeout=5,
    ).strip()


def main():
    try:
        json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    try:
        branch = get_git_branch()
    except Exception:
        sys.exit(0)

    m = re.match(r"PR(\d+)/", branch)
    if not m:
        sys.exit(0)

    pr_num = m.group(1)
    matches = list(Path.cwd().glob(f"docs/tasks/**/PR{pr_num}.md"))
    if not matches:
        sys.exit(0)

    pr_doc = matches[0].read_text(encoding="utf-8")
    unchecked = re.findall(r"^- \[ \] .+", pr_doc, re.MULTILINE)
    if not unchecked:
        sys.exit(0)

    items = "\n".join(unchecked)
    context = (
        f"[work-kit] PR{pr_num} has {len(unchecked)} unchecked task(s). "
        f"Mark completed ones as `- [x]` in the PR doc before finishing.\n{items}"
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "additionalContext": context,
        }
    }))


if __name__ == "__main__":
    main()
