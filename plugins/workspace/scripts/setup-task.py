#!/usr/bin/env python3
"""
setup-task.py -- Initialize task folder and documents for a new PR.

Usage (new task folder):
    python setup-task.py <worktree_path> \\
        --pr <N> \\
        --title <kebab-case-title> \\
        --date <YYYYMMDD> \\
        --plugin-root <plugin_root_path>

Usage (existing task folder):
    python setup-task.py <worktree_path> \\
        --pr <N> \\
        --task-dir <YYYYMMDD_existing-title> \\
        --plugin-root <plugin_root_path>

Creates:
    <worktree>/.work/tasks/<task_dir>/PR<N>/TODO.md
    <worktree>/.work/tasks/<task_dir>/PR<N>/QA.md

When --task-dir is omitted, the folder name is built from --date and --title.
When --task-dir is provided, --date and --title are optional (used only in TODO.md title).
"""

import argparse
import pathlib
import sys


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create PR folder and initial documents from templates."
    )
    parser.add_argument("worktree", help="Path to the git worktree")
    parser.add_argument("--pr", required=True, type=int, help="PR number")
    parser.add_argument("--title", default="", help="Task title (kebab-case); used in TODO.md heading")
    parser.add_argument("--date", default="", help="Date in YYYYMMDD format")
    parser.add_argument(
        "--task-dir",
        default="",
        help="Existing task folder name (e.g. 20260515_my-task). "
             "When omitted, a new folder is created from --date and --title.",
    )
    parser.add_argument("--plugin-root", required=True, help="Plugin root path")
    args = parser.parse_args()

    worktree = pathlib.Path(args.worktree)
    plugin_root = pathlib.Path(args.plugin_root)

    if args.task_dir:
        task_folder_name = args.task_dir
        title_for_heading = args.title or args.task_dir
    else:
        if not args.date or not args.title:
            print(
                "ERROR: --date and --title are required when --task-dir is not specified.",
                file=sys.stderr,
            )
            sys.exit(1)
        task_folder_name = f"{args.date}_{args.title}"
        title_for_heading = args.title

    tasks_root = worktree / ".work" / "tasks"
    task_dir = tasks_root / task_folder_name

    if args.task_dir and not task_dir.exists():
        existing = sorted(
            p.name for p in tasks_root.iterdir() if p.is_dir() and p.name != ".gitignore"
        ) if tasks_root.exists() else []
        print(
            f"ERROR: task folder '{task_folder_name}' does not exist.\n"
            f"Existing folders: {existing or '(none)'}",
            file=sys.stderr,
        )
        sys.exit(1)

    pr_dir = task_dir / f"PR{args.pr}"
    pr_dir.mkdir(parents=True, exist_ok=True)

    _create_from_template(
        plugin_root / "templates" / "TODO.md",
        pr_dir / "TODO.md",
        {"{N}": str(args.pr), "{タイトル}": title_for_heading},
    )

    _create_from_template(
        plugin_root / "templates" / "QA.md",
        pr_dir / "QA.md",
        {"{N}": str(args.pr)},
    )

    print(f"Task folder : {task_dir}")
    print(f"Created     : {pr_dir / 'TODO.md'}")
    print(f"Created     : {pr_dir / 'QA.md'}")


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
