#!/usr/bin/env python3
"""
setup-task.py -- Initialize task folder and document for a new branch.

Usage (new task folder):
    python setup-task.py <worktree_path> \\
        --branch <{type}/{title}> \\
        --ja-title <日本語タイトル> \\
        --date <YYMMDD> \\
        --plugin-root <plugin_root_path> \\
        [--title <kebab-case-title>] \\
        [--id <N>]

Usage (existing task folder):
    python setup-task.py <worktree_path> \\
        --branch <{type}/{title}> \\
        --ja-title <日本語タイトル> \\
        --task-dir <YYMMDD_existing-title> \\
        --plugin-root <plugin_root_path> \\
        [--id <N>]

Creates:
    <worktree>/.work/tasks/<task_dir>/<YYMMDD>-<日本語タイトル>.md

When --ja-title is provided, the file name uses the Japanese title.
When --ja-title is omitted, the branch name is hyphenated and used as a fallback
(e.g. refactor/rename-pr-to-branch -> YYMMDD-refactor-rename-pr-to-branch.md).
The date prefix is taken from --date, or extracted from --task-dir (the 6-digit YYMMDD prefix).

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
             "Used in the document header. When --ja-title is omitted, slashes are converted "
             "to hyphens to form the file name.",
    )
    parser.add_argument(
        "--ja-title",
        default="",
        dest="ja_title",
        help="Japanese title used as the file name stem (e.g. ブランチ文書ファイル名変更). "
             "When provided, the file is named <YYMMDD>-<ja-title>.md.",
    )
    parser.add_argument("--title", default="", help="Task title (kebab-case); used in the folder name when creating a new folder")
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

    # Determine date prefix: from --date, or extract from task folder name (YYMMDD_xxx format).
    date_prefix = args.date
    if not date_prefix and task_folder_name:
        prefix = task_folder_name.split("_")[0]
        if len(prefix) == 6 and prefix.isdigit():
            date_prefix = prefix

    # Determine file name stem: Japanese title takes priority; fall back to hyphenated branch name.
    if args.ja_title:
        name_stem = args.ja_title
    else:
        name_stem = args.branch.replace("/", "-")
    file_stem = f"{date_prefix}-{name_stem}" if date_prefix else name_stem
    dest_path = task_dir / f"{file_stem}.md"

    template_path = (
        plugin_root / "templates" / ".work" / "tasks" / "yymmdd_xxx" / "yymmdd-日本語タイトル.md"
    )
    if not template_path.exists():
        # Back-compat: fall back to legacy template names.
        template_path = (
            plugin_root / "templates" / ".work" / "tasks" / "yymmdd_xxx" / "yymmdd-branch-name.md"
        )
    if not template_path.exists():
        template_path = (
            plugin_root / "templates" / ".work" / "tasks" / "yymmdd_xxx" / "type-title.md"
        )
    if not template_path.exists():
        template_path = (
            plugin_root / "templates" / ".work" / "tasks" / "yymmdd_xxx" / "PRNNN-type-title.md"
        )
    id_for_heading = str(args.id) if args.id is not None else ""
    _create_from_template(
        template_path,
        dest_path,
        {
            "{N}": id_for_heading,
            "{日本語タイトル}": args.ja_title or title_for_heading,
            "{branch-name}": args.branch,
            "{タイトル}": title_for_heading,
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
