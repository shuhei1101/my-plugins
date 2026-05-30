#!/usr/bin/env python3
"""
setup-task.py -- Initialize task folder and document for a new branch.

Usage (new task folder):
    python setup-task.py <worktree_path> \\
        --branch <{type}/{title}> \\
        --title <kebab-case-title> \\
        --date <YYMMDD> \\
        --plugin-root <plugin_root_path> \\
        [--id <N>]

Usage (existing task folder):
    python setup-task.py <worktree_path> \\
        --branch <{type}/{title}> \\
        --task-dir <YYMMDD_existing-title> \\
        --plugin-root <plugin_root_path> \\
        [--id <N>]

Creates:
    <worktree>/.work/tasks/<task_dir>/<branch-hyphenated>.md

The branch name is hyphenated by replacing every slash with a hyphen
(e.g. refactor/rename-pr-to-branch -> refactor-rename-pr-to-branch).

When --task-dir is omitted, the folder name is built from --date and --title.
When --task-dir is provided, --date and --title are optional (used only in the document heading).

--id is the internal numeric ID tracked in index.yaml. It is recorded in the document heading for
cross-reference with commits and archive metadata; it is NOT embedded in the branch / worktree /
filename. Legacy invocations with --pr are accepted as an alias for --id.
"""

import argparse
import pathlib
import sys


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a branch task folder and initial document from template."
    )
    parser.add_argument("worktree", help="Path to the git worktree")
    parser.add_argument(
        "--id",
        "--pr",
        dest="id",
        default=None,
        type=int,
        help="Internal numeric ID tracked in index.yaml (used in the document heading only). "
             "--pr is accepted as an alias for back-compat.",
    )
    parser.add_argument(
        "--branch",
        required=True,
        help="Full branch name (e.g. refactor/rename-pr-to-branch). "
             "Slashes are converted to hyphens to form the file name.",
    )
    parser.add_argument("--title", default="", help="Task title (kebab-case); used in the document heading")
    parser.add_argument("--date", default="", help="Date in YYMMDD format")
    parser.add_argument(
        "--task-dir",
        default="",
        help="Existing task folder name (e.g. 260515_my-task). "
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

    task_dir.mkdir(parents=True, exist_ok=True)

    file_stem = args.branch.replace("/", "-")
    dest_path = task_dir / f"{file_stem}.md"

    template_path = (
        plugin_root / "templates" / ".work" / "tasks" / "yymmdd_xxx" / "type-title.md"
    )
    if not template_path.exists():
        # Back-compat: fall back to the legacy template name if the new one is not yet deployed.
        template_path = (
            plugin_root / "templates" / ".work" / "tasks" / "yymmdd_xxx" / "PRNNN-type-title.md"
        )
    id_for_heading = str(args.id) if args.id is not None else ""
    _create_from_template(
        template_path,
        dest_path,
        {
            "{N}": id_for_heading,
            "{タイトル}": title_for_heading,
            "{ブランチ名}": args.branch,
        },
    )

    print(f"Task folder : {task_dir}")
    print(f"Created     : {dest_path}")


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
