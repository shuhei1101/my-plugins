#!/usr/bin/env python3
"""
setup-task.py -- Initialize task folder and documents for a new PR.

Usage:
    python setup-task.py <worktree_path> \\
        --pr <N> \\
        --title <kebab-case-title> \\
        --date <YYYYMMDD> \\
        --plugin-root <plugin_root_path>

Creates:
    <worktree>/.work/tasks/<YYYYMMDD>_<title>/PR<N>/TODO.md
    <worktree>/.work/tasks/<YYYYMMDD>_<title>/PR<N>/QA.md
"""

import argparse
import pathlib
import sys


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create task folder and initial documents from templates."
    )
    parser.add_argument("worktree", help="Path to the git worktree")
    parser.add_argument("--pr", required=True, type=int, help="PR number")
    parser.add_argument("--title", required=True, help="Task title (kebab-case)")
    parser.add_argument("--date", required=True, help="Date in YYYYMMDD format")
    parser.add_argument("--plugin-root", required=True, help="Plugin root path")
    args = parser.parse_args()

    worktree = pathlib.Path(args.worktree)
    plugin_root = pathlib.Path(args.plugin_root)

    task_dir = (
        worktree
        / ".work"
        / "tasks"
        / f"{args.date}_{args.title}"
        / f"PR{args.pr}"
    )
    task_dir.mkdir(parents=True, exist_ok=True)

    _create_from_template(
        plugin_root / "templates" / "TODO.md",
        task_dir / "TODO.md",
        {"{N}": str(args.pr), "{タイトル}": args.title},
    )

    _create_from_template(
        plugin_root / "templates" / "QA.md",
        task_dir / "QA.md",
        {"{N}": str(args.pr)},
    )

    print(f"Created: {task_dir / 'TODO.md'}")
    print(f"Created: {task_dir / 'QA.md'}")


def _create_from_template(
    template_path: pathlib.Path,
    dest_path: pathlib.Path,
    replacements: dict[str, str],
) -> None:
    if not template_path.exists():
        print(f"ERROR: template not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    content = template_path.read_text(encoding="utf-8")
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    dest_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
