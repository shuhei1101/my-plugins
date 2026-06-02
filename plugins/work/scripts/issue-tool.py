"""
issue-tool — workspace の `.work/issues/` 操作用 CLI。

使い方:
  python issue-tool.py close --issue-id ISSUE-N --resolution {resolved|wontfix} [--linked-branch BRANCH] [--issues-dir .work/issues]
  python issue-tool.py set-status --issue-id ISSUE-N --status {not_started|in_progress} [--issues-dir .work/issues]

サブコマンド:
  close          イシューを 1 件クローズする:
                   1. .work/issues/ISSUE-{N}.md を .work/issues/closed/ISSUE-{N}.md に移動
                   2. _index.yaml から該当エントリを削除
                   3. _index.archive.yaml の closed_issues に linked_branch 付きで追記
                 --linked-branch は対応ブランチ名（任意・wontfix で未着手のまま閉じる場合は省略可）。
  set-status     _index.yaml の該当エントリの status を更新する（フロントマターの status を
                 AI 側がインデックスへミラーするために使用。エントリが無ければ警告のみ）。

`.work/issues/` 配下の YAML 読み書きをこのスクリプト経由に集約することで、
Claude Code のコンテキストに YAML ファイルを丸ごと読み込ませずに済み、
イシュー記述ルール（work-dir/イシュー.md）に沿った一貫したフォーマットで書き込める。
"""

from __future__ import annotations

# ── 標準ライブラリ ──────────────────────────────────────────
import argparse
import shutil
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── サードパーティ ──────────────────────────────────────────
try:
    import yaml  # pip install pyyaml
except ImportError:
    print("エラー: PyYAML がインストールされていません。`pip install pyyaml` を実行してください。", file=sys.stderr)
    sys.exit(1)

# ── 定数 ────────────────────────────────────────────────────
DEFAULT_ISSUES_DIR = Path(".work/issues")


# ── 内部ヘルパ ──────────────────────────────────────────────
def _load(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _save(path: Path, data: dict, original_text: str) -> None:
    """先頭のコメント行を保持したまま YAML を書き戻す。"""
    comment_lines = [l for l in original_text.splitlines() if l.startswith("#")]
    header = "\n".join(comment_lines) + "\n\n" if comment_lines else ""
    path.write_text(
        header + yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )


# ── サブコマンドハンドラ ─────────────────────────────────────
def cmd_close(args: argparse.Namespace) -> None:
    """イシューを 1 件クローズする: ファイル移動・_index.yaml 更新・_index.archive.yaml 追記。"""
    issues_dir = Path(args.issues_dir)
    issue_id: str = args.issue_id
    resolution: str = args.resolution
    linked_branch: str | None = args.linked_branch

    if not issues_dir.exists():
        print(f"Skip: {issues_dir} does not exist", file=sys.stderr)
        return

    index_path = issues_dir / "_index.yaml"
    archive_path = issues_dir / "_index.archive.yaml"
    issue_file = issues_dir / f"{issue_id}.md"
    closed_dir = issues_dir / "closed"

    # 1. _index.yaml を読んで、削除前にイシューのメタ情報を控えておく
    index_original = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    index_data: dict = yaml.safe_load(index_original) or {} if index_original else {}
    issues: list[dict] = index_data.get("issues", [])
    entry = next((i for i in issues if i.get("id") == issue_id), None)
    if entry is None:
        print(f"Warning: {issue_id} not found in {index_path}", file=sys.stderr)
        entry = {"id": issue_id, "title": "", "tags": []}

    # 2. イシューファイルを closed/ に移動する（存在する場合のみ）
    if issue_file.exists():
        closed_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(issue_file), str(closed_dir / issue_file.name))
    else:
        print(f"Warning: {issue_file} not found; skipping file move", file=sys.stderr)

    # 3. _index.yaml から該当エントリを削除する
    if entry in issues:
        issues.remove(entry)
        index_data["issues"] = issues
        if index_path.exists():
            _save(index_path, index_data, index_original)

    # 4. _index.archive.yaml の closed_issues に追記する
    archive_original = archive_path.read_text(encoding="utf-8") if archive_path.exists() else ""
    archive_data: dict = yaml.safe_load(archive_original) or {} if archive_original else {}
    closed_issues: list[dict] = archive_data.get("closed_issues", [])
    record = {
        "id": issue_id,
        "title": entry.get("title", ""),
        "closed": date.today().isoformat(),
        "resolution": resolution,
        "tags": entry.get("tags", []) or [],
    }
    if linked_branch:
        record["linked_branch"] = linked_branch
    closed_issues.append(record)
    archive_data["closed_issues"] = closed_issues
    if "scan_records" not in archive_data:
        archive_data["scan_records"] = []
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    _save(archive_path, archive_data, archive_original)

    print(f"Closed {issue_id} (resolution={resolution}, linked_branch={linked_branch})")


def cmd_set_status(args: argparse.Namespace) -> None:
    """_index.yaml の該当イシューエントリの status を更新する。"""
    issues_dir = Path(args.issues_dir)
    issue_id: str = args.issue_id
    status: str = args.status

    index_path = issues_dir / "_index.yaml"
    if not index_path.exists():
        print(f"Skip: {index_path} does not exist", file=sys.stderr)
        return

    index_original = index_path.read_text(encoding="utf-8")
    index_data: dict = yaml.safe_load(index_original) or {}
    issues: list[dict] = index_data.get("issues", [])
    entry = next((i for i in issues if i.get("id") == issue_id), None)
    if entry is None:
        print(f"Warning: {issue_id} not found in {index_path}", file=sys.stderr)
        return

    entry["status"] = status
    index_data["issues"] = issues
    _save(index_path, index_data, index_original)
    print(f"Set {issue_id} status={status}")


# ── main ────────────────────────────────────────────────────
def main() -> int:
    args = parse_args()
    handlers = {
        "close": cmd_close,
        "set-status": cmd_set_status,
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

    p_close = sub.add_parser("close", help="イシューを 1 件クローズしてアーカイブに記録する")
    p_close.add_argument("--issue-id", required=True, help="例: ISSUE-001")
    p_close.add_argument(
        "--resolution",
        required=True,
        choices=["resolved", "wontfix"],
        help="クローズ時の解決区分",
    )
    p_close.add_argument("--linked-branch", default=None, help="このイシューをクローズしたブランチ名（任意）")
    p_close.add_argument("--issues-dir", default=str(DEFAULT_ISSUES_DIR), help=".work/issues/ のパス")

    p_status = sub.add_parser("set-status", help="_index.yaml の status を更新する")
    p_status.add_argument("--issue-id", required=True, help="例: ISSUE-001")
    p_status.add_argument(
        "--status",
        required=True,
        choices=["not_started", "in_progress"],
        help="設定するステータス",
    )
    p_status.add_argument("--issues-dir", default=str(DEFAULT_ISSUES_DIR), help=".work/issues/ のパス")

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
