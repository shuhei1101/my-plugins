#!/usr/bin/env python3
"""
setup-task.py -- Initialize task folder and document for a new branch.

Usage (new task folder):
    python setup-task.py <worktree_path> \\
        --branch <{type}/{title}> \\
        --ja-title <日本語タイトル> \\
        --date <YYMMDD> \\
        [--title <kebab-case-title>] \\
        [--id <N>]

Usage (existing task folder):
    python setup-task.py <worktree_path> \\
        --branch <{type}/{title}> \\
        --ja-title <日本語タイトル> \\
        --task-dir <YYMMDD_existing-title> \\
        [--id <N>]

Creates:
    <worktree>/.work/tasks/<task_dir>/<YYMMDD>-<日本語タイトル>.md

When --ja-title is provided, the file name uses the Japanese title.
When --ja-title is omitted, the branch name is hyphenated and used as a fallback
(e.g. refactor/rename-pr-to-branch -> YYMMDD-refactor-rename-pr-to-branch.md).
The date prefix is taken from --date, or extracted from --task-dir (the 6-digit YYMMDD prefix).

When --task-dir is omitted, the folder name is built from --date and --title.
When --task-dir is provided, --date and --title are optional (used only in the document heading).

--id is the internal numeric ID tracked in index.yaml (archive cross-reference). It is accepted for
interface compatibility but is NOT written into the document or the file name. Legacy invocations
with --pr are accepted as an alias for --id.
--plugin-root is accepted for backward compatibility but is no longer used.
"""

import argparse
import pathlib
import sys

# ── ブランチドキュメントテンプレート ────────────────────────
_BRANCH_DOC_TEMPLATE = """\
# {日本語タイトル}

> ブランチ: `{branch-name}`

## 概要

{このブランチの目的・背景を書く}

### 実施条件

{例: 即時実施可 / 「{他ブランチ名}」が完了してから}

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | {何をするか（サンプル行 — 実際の作業に書き換える）} |
| 2 | - | {何をするか} |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `{file/path}` | 新規 | {このファイルで何を実装したか} | {補足あれば} |
| 2 | `{file/path2}` | 編集 | {何を変更したか} | - |

## テスト

手動テスト・動作確認の実施記録。

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | {確認内容} | (未実施) | - |

## QA

このブランチのスコープの未決定事項を QA-XXX として記録する。決定後は本文の該当箇所に反映する。

### QA-001: {タイトル}

**背景**: {なぜこれを判断する必要があるか}

| # | 案 | 内容 |
|---|---|---|
| 1 | A | {案 A の説明} |
| 2 | B | {案 B の説明} |

**推奨方式**: {A/B のどちらか + 理由を 1〜2 行。「後で決める」は禁止}

**状態**: 未解決

**決定したら反映先**: {ドキュメントの該当セクション}

## 参考ドキュメント

- `{path/to/spec.md}`: {何の資料か}

## 関連イシュー

このブランチが解決する `.work/issues/` のイシュー一覧。merge 実行時に自動でクローズされる。
イシューがない場合は表ごと削除してよい。

| # | ID | 概要 | resolution |
|---|---|---|---|
| 1 | ISSUE-{N} | {イシューのタイトル} | resolved |

## 関連ブランチ

直接関連するブランチ（先行・分割兄弟・後続）を列挙する。

| # | ブランチ | 概要 |
|---|---|---|
| 1 | {type/title} | {概要} |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | {次にやること} | {背景・目的} | {例: 即時実施可 / 「{他候補タイトル}」が完了したら} |
"""


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
        help="Internal numeric ID tracked in index.yaml (accepted for interface compatibility; "
             "not written into the document). --pr is accepted as an alias for back-compat.",
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
    parser.add_argument("--plugin-root", default="", help="Accepted for backward compatibility; no longer used.")
    args = parser.parse_args()

    worktree = pathlib.Path(args.worktree)

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

    _create_from_template(
        dest_path,
        {
            "{日本語タイトル}": args.ja_title or title_for_heading,
            "{branch-name}": args.branch,
            "{タイトル}": title_for_heading,
        },
    )

    print(f"Task folder : {task_dir}")
    print(f"Created     : {dest_path}")


def _create_from_template(
    dest_path: pathlib.Path,
    replacements: dict[str, str],
) -> None:
    content = _BRANCH_DOC_TEMPLATE
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    dest_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
