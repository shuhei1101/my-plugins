#!/usr/bin/env python3
"""
setup-task.py — 新しいブランチのタスクフォルダとブランチドキュメントを初期化する。

使い方（新規タスクフォルダ）:
    python setup-task.py <worktree_path> \\
        --branch <{type}/{title}> \\
        --ja-title <日本語タイトル> \\
        --date <YYMMDD> \\
        --plugin-root <plugin_root_path> \\
        [--title <kebab-case-title>] \\
        [--id <N>]

使い方（既存タスクフォルダへ追加）:
    python setup-task.py <worktree_path> \\
        --branch <{type}/{title}> \\
        --ja-title <日本語タイトル> \\
        --task-dir <YYMMDD_existing-title> \\
        --plugin-root <plugin_root_path> \\
        [--id <N>]

作成先:
    <worktree>/.work/tasks/<task_dir>/<YYMMDD>-<日本語タイトル>.md

--ja-title が指定された場合、ファイル名に日本語タイトルを使用する。
--ja-title が省略された場合、ブランチ名をハイフン化してフォールバックとして使う
（例: refactor/rename-pr-to-branch → YYMMDD-refactor-rename-pr-to-branch.md）。
日付プレフィックスは --date から取得するか、--task-dir の 6 桁 YYMMDD プレフィックスから抽出する。

--task-dir が省略された場合、--date と --title からフォルダ名を生成する。
--task-dir が指定された場合、--date と --title は任意（ドキュメントの見出しにのみ使用）。

--id はブランチの内部 ID（index.yaml のクロスリファレンス用）。インターフェース互換性のために
受け付けるが、ドキュメントやファイル名には記載しない。--pr は --id の別名（後方互換）。
"""

from __future__ import annotations

import argparse
import pathlib
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="新しいブランチのタスクフォルダとブランチドキュメントをテンプレートから作成する。"
    )
    parser.add_argument("worktree", help="git ワークツリーのパス")
    parser.add_argument(
        "--id",
        "--pr",
        dest="id",
        default=None,
        type=int,
        help="index.yaml で追跡する内部 ID（インターフェース互換性のために受け付けるが、ドキュメントには記載しない）。"
             "--pr は後方互換の別名。",
    )
    parser.add_argument(
        "--branch",
        required=True,
        help="フルブランチ名（例: refactor/rename-pr-to-branch）。ドキュメントヘッダーに使用する。"
             "--ja-title が省略された場合、スラッシュをハイフンに変換してファイル名に使用する。",
    )
    parser.add_argument(
        "--ja-title",
        default="",
        dest="ja_title",
        help="ファイル名ステムに使う日本語タイトル（例: ブランチ文書ファイル名変更）。"
             "指定した場合、ファイルは <YYMMDD>-<ja-title>.md になる。",
    )
    parser.add_argument("--title", default="", help="タスクタイトル（kebab-case）。新規フォルダ作成時にフォルダ名に使用する。")
    parser.add_argument("--date", default="", help="YYMMDD 形式の日付")
    parser.add_argument(
        "--task-dir",
        default="",
        help="既存タスクフォルダ名（例: 260515_my-task）。"
             "省略した場合、--date と --title から新規フォルダを作成する。",
    )
    parser.add_argument("--plugin-root", required=True, help="プラグインルートのパス")
    args = parser.parse_args()

    worktree = pathlib.Path(args.worktree)
    plugin_root = pathlib.Path(args.plugin_root)

    if args.task_dir:
        task_folder_name = args.task_dir
        title_for_heading = args.title or args.task_dir
    else:
        if not args.date or not args.title:
            print(
                "エラー: --task-dir を省略する場合は --date と --title が必要です。",
                file=sys.stderr,
            )
            return 1
        task_folder_name = f"{args.date}_{args.title}"
        title_for_heading = args.title

    tasks_root = worktree / ".work" / "tasks"
    task_dir = tasks_root / task_folder_name

    if args.task_dir and not task_dir.exists():
        existing = sorted(
            p.name for p in tasks_root.iterdir() if p.is_dir() and p.name != ".gitignore"
        ) if tasks_root.exists() else []
        print(
            f"エラー: タスクフォルダ '{task_folder_name}' が存在しません。\n"
            f"既存フォルダ: {existing or '(なし)'}",
            file=sys.stderr,
        )
        return 1

    task_dir.mkdir(parents=True, exist_ok=True)

    # 日付プレフィックスを決定: --date、またはタスクフォルダ名（YYMMDD_xxx 形式）から抽出する。
    date_prefix = args.date
    if not date_prefix and task_folder_name:
        prefix = task_folder_name.split("_")[0]
        if len(prefix) == 6 and prefix.isdigit():
            date_prefix = prefix

    # ファイル名ステムを決定: 日本語タイトル優先、なければブランチ名のハイフン化を使う。
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
        # 後方互換: レガシーテンプレート名にフォールバック。
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
    _create_from_template(
        template_path,
        dest_path,
        {
            "{日本語タイトル}": args.ja_title or title_for_heading,
            "{branch-name}": args.branch,
            "{タイトル}": title_for_heading,
        },
    )

    print(f"Task folder : {task_dir}")
    print(f"Created     : {dest_path}")
    return 0


def _create_from_template(
    template_path: pathlib.Path,
    dest_path: pathlib.Path,
    replacements: dict[str, str],
) -> None:
    if not template_path.exists():
        print(f"エラー: テンプレートが見つかりません: {template_path}", file=sys.stderr)
        sys.exit(1)

    content = template_path.read_text(encoding="utf-8")
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    dest_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
