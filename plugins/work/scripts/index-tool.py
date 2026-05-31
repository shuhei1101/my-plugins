"""
index-tool — workspace の index.yaml 操作用 CLI。

使い方:
  python index-tool.py next-id [index_yaml]
  python index-tool.py add [index_yaml] --id N --branch B --title T --type T --summary S --task T
  python index-tool.py list-active [index_yaml]
  python index-tool.py set-completed [index_yaml] --id N
  python index-tool.py archive [index_yaml] [archive_yaml]

  index_yaml   index.yaml のパス（デフォルト: .work/tasks/index.yaml）
  archive_yaml index.archive.yaml のパス（デフォルト: .work/tasks/index.archive.yaml）

サブコマンド:
  next-id        次の ID（last_id + 1、存在しない場合は 1）を出力する
  add            新しいブランチエントリを追記し last_id を更新する
  list-active    アクティブ（completed: false）なブランチエントリを 1 行ずつ出力する:
                   id|title|type|task
  set-completed  ブランチエントリを completed: true にマークする
  archive        完了済みエントリを index.yaml から index.archive.yaml に移動する。
                 移動した件数を出力する。

index.yaml の操作をこのスクリプトに集約することで、Claude Code がコンテキストに
YAML ファイルを丸ごと読み込まずに済む。
"""

from __future__ import annotations

# ── 標準ライブラリ ──────────────────────────────────────────
import argparse
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── サードパーティ ──────────────────────────────────────────
try:
    import yaml  # pip install pyyaml
except ImportError:
    print("エラー: PyYAML がインストールされていません。`pip install pyyaml` を実行してください。", file=sys.stderr)
    sys.exit(1)

# ── 定数 ────────────────────────────────────────────────────
DEFAULT_INDEX = Path(".work/tasks/index.yaml")
DEFAULT_ARCHIVE = Path(".work/tasks/index.archive.yaml")


# ── 内部ヘルパ ──────────────────────────────────────────────
def _load(path: Path) -> dict:
    """YAML ファイルを読み込んで dict を返す。ファイルが存在しない場合は空 dict を返す。"""
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _save(path: Path, data: dict, original_text: str) -> None:
    """先頭のコメント行を保持したまま YAML を書き戻す。"""
    comment_lines = [l for l in original_text.splitlines() if l.startswith("#")]
    header = "\n".join(comment_lines) + "\n\n" if comment_lines else ""
    path.write_text(header + yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False), encoding="utf-8")


# ── サブコマンドハンドラ ─────────────────────────────────────
def cmd_next_id(args: argparse.Namespace) -> None:
    """次の利用可能な ID を出力する。"""
    index_path = Path(args.index_yaml)
    data = _load(index_path)
    branches: list[dict] = data.get("branches", [])
    last_id: int = data.get("last_id") or (max((p["id"] for p in branches), default=0))
    print(last_id + 1)


def cmd_add(args: argparse.Namespace) -> None:
    """新しいブランチエントリを追記し last_id を更新する。"""
    index_path = Path(args.index_yaml)
    original = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    data = yaml.safe_load(original) or {} if original else {}

    branches: list[dict] = data.get("branches", [])
    new_entry = {
        "id": args.id,
        "branch": args.branch,
        "title": args.title,
        "type": args.type,
        "tags": [],
        "summary": args.summary,
        "task": args.task,
        "completed": False,
    }
    branches.append(new_entry)
    data["branches"] = branches
    data["last_id"] = args.id

    _save(index_path, data, original)
    print(f"Added PR{args.id} to {index_path}")


def cmd_list_active(args: argparse.Namespace) -> None:
    """アクティブなブランチエントリを 1 行ずつ出力する: id|title|type|task"""
    index_path = Path(args.index_yaml)
    data = _load(index_path)
    active = [p for p in data.get("branches", []) if not p.get("completed", False)]
    for p in active:
        print(f"{p['id']}|{p['title']}|{p['type']}|{p['task']}")


def cmd_completed_count(args: argparse.Namespace) -> None:
    """完了済みエントリの件数を出力する。"""
    index_path = Path(args.index_yaml)
    data = _load(index_path)
    count = sum(1 for p in data.get("branches", []) if p.get("completed", False))
    print(count)


def cmd_set_completed(args: argparse.Namespace) -> None:
    """指定したブランチエントリを completed: true にマークする。"""
    index_path = Path(args.index_yaml)
    original = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    data = yaml.safe_load(original) or {} if original else {}

    branches: list[dict] = data.get("branches", [])
    target = next((p for p in branches if p["id"] == args.id), None)
    if target is None:
        print(f"エラー: エントリ {args.id} が {index_path} に見つかりません。", file=sys.stderr)
        sys.exit(1)

    target["completed"] = True
    data["branches"] = branches
    _save(index_path, data, original)
    print(f"Entry {args.id} marked as completed in {index_path}")


def cmd_archive(args: argparse.Namespace) -> None:
    """完了済みエントリを index.yaml から index.archive.yaml に移動する。"""
    index_path = Path(args.index_yaml)
    archive_path = Path(args.archive_yaml)

    original = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    data = yaml.safe_load(original) or {} if original else {}

    branches: list[dict] = data.get("branches", [])
    completed = [p for p in branches if p.get("completed", False)]
    remaining = [p for p in branches if not p.get("completed", False)]

    if not completed:
        print(0)
        return

    # アーカイブに追記
    archive_original = archive_path.read_text(encoding="utf-8") if archive_path.exists() else ""
    archive_data = yaml.safe_load(archive_original) or {} if archive_original else {}
    archive_branches: list[dict] = archive_data.get("branches", [])
    archive_branches.extend(completed)
    archive_data["branches"] = archive_branches
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    _save(archive_path, archive_data, archive_original)

    # index から削除
    data["branches"] = remaining
    _save(index_path, data, original)

    print(len(completed))


# ── main ────────────────────────────────────────────────────
def main() -> int:
    args = parse_args()
    handlers = {
        "next-id": cmd_next_id,
        "add": cmd_add,
        "list-active": cmd_list_active,
        "completed-count": cmd_completed_count,
        "set-completed": cmd_set_completed,
        "archive": cmd_archive,
    }
    try:
        handlers[args.subcommand](args)
        return 0
    except SystemExit:
        raise
    except Exception:
        import traceback
        traceback.print_exc()
        return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    # next-id
    p_next = sub.add_parser("next-id", help="次の利用可能な ID を出力する")
    p_next.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))

    # add
    p_add = sub.add_parser("add", help="新しいブランチエントリを追加する")
    p_add.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))
    p_add.add_argument("--id", type=int, required=True)
    p_add.add_argument("--branch", default="")
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--type", required=True, dest="type")
    p_add.add_argument("--summary", required=True)
    p_add.add_argument("--task", required=True)

    # list-active
    p_list = sub.add_parser("list-active", help="アクティブ（未完了）なブランチを列挙する")
    p_list.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))

    # completed-count
    p_count = sub.add_parser("completed-count", help="完了済みエントリの件数を出力する")
    p_count.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))

    # set-completed
    p_set = sub.add_parser("set-completed", help="ブランチエントリを完了済みにマークする")
    p_set.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))
    p_set.add_argument("--id", type=int, required=True)

    # archive
    p_archive = sub.add_parser("archive", help="完了済みエントリをアーカイブファイルに移動する")
    p_archive.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))
    p_archive.add_argument("archive_yaml", nargs="?", default=str(DEFAULT_ARCHIVE))

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
