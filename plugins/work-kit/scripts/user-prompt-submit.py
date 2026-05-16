#!/usr/bin/env python3
"""
UserPromptSubmit hook: inject current PR task status into Claude's context.
- In a PR worktree: injects the task checklist from the PR doc.
- On main branch: reminds to create a worktree for new work.
Silently exits on any error.
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


def extract_task_section(pr_doc: str) -> str:
    m = re.search(
        r"(## 作業内容\n(?:(?!^## ).)*)",
        pr_doc,
        re.MULTILINE | re.DOTALL,
    )
    return m.group(1).strip() if m else pr_doc.strip()


def output(context: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))


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
        output("[work-kit] On main branch. If starting new work, create a worktree with /wt:wt.")
        sys.exit(0)

    pr_num = m.group(1)
    matches = list(Path.cwd().glob(f"docs/tasks/**/PR{pr_num}.md"))
    if not matches:
        sys.exit(0)

    pr_doc = matches[0].read_text(encoding="utf-8")
    tasks = extract_task_section(pr_doc)
    output(f"[PR{pr_num} task status]\n{tasks}")


if __name__ == "__main__":
    main()
