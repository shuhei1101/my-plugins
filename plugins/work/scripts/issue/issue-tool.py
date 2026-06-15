"""
issue-tool — workspace の `.work/issues/` 操作用 CLI。

使い方:
  python issue-tool.py close --issue-id ISSUE-N --resolution {resolved|wontfix} [--linked-branch BRANCH] [--issues-dir .work/issues]
  python issue-tool.py move-to-progress --issue-id ISSUE-N [--issues-dir .work/issues]
  python issue-tool.py set-status --issue-id ISSUE-N --status {not_started|in_progress} [--issues-dir .work/issues]
  python issue-tool.py add-branch --issue-id ISSUE-N --branch BRANCH [--issues-dir .work/issues]

サブコマンド:
  close              イシューを 1 件クローズする:
                       1. ISSUE-{N}.md を closed/ に移動
                       2. _index.yaml から該当エントリを削除
                       3. _index.archive.yaml の closed_issues に linked_branch 付きで追記
                     --linked-branch は対応ブランチ名（任意・wontfix で未着手のまま閉じる場合は省略可）。
  move-to-progress   イシューを targets/ から progress/ へ移し、_index.yaml の status を in_progress にする。
  set-status         _index.yaml の該当エントリの status を更新する（ファイルは移動しない）。
  add-branch         _index.yaml の該当エントリの branches 配列にブランチ名を追記する。

イシューファイルはフロントマターを持たない（# ISSUE-N から始まる）。作業状態（status / branches）は
すべて _index.yaml が正で、このスクリプト経由で更新する。
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# 共通ガード (scripts/_branch_guard.py)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _branch_guard import assert_not_protected_branch  # noqa: E402

try:
    import yaml
except ImportError:
    print("エラー: PyYAML がインストールされていません。`pip install pyyaml` を実行してください。", file=sys.stderr)
    sys.exit(1)

DEFAULT_ISSUES_DIR = Path(".work/issues")


def _load(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _save(path: Path, data: dict, original_text: str) -> None:
    comment_lines = [l for l in original_text.splitlines() if l.startswith("#")]
    header = "\n".join(comment_lines) + "\n\n" if comment_lines else ""
    path.write_text(
        header + yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )


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
    closed_dir = issues_dir / "closed"

    # イシューファイルを targets/ か progress/ か直下から探す
    candidates = [
        issues_dir / f"{issue_id}.md",
        issues_dir / "targets" / f"{issue_id}.md",
        issues_dir / "progress" / f"{issue_id}.md",
    ]
    issue_file = next((p for p in candidates if p.exists()), None)

    index_original = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    index_data: dict = yaml.safe_load(index_original) or {} if index_original else {}
    issues: list[dict] = index_data.get("issues", [])
    entry = next((i for i in issues if i.get("id") == issue_id), None)
    if entry is None:
        print(f"Warning: {issue_id} not found in {index_path}", file=sys.stderr)
        entry = {"id": issue_id, "title": "", "tags": []}

    if issue_file:
        closed_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(issue_file), str(closed_dir / f"{issue_id}.md"))
    else:
        print(f"Warning: {issue_id}.md not found in {issues_dir}; skipping file move", file=sys.stderr)

    if entry in issues:
        issues.remove(entry)
        index_data["issues"] = issues
        if index_path.exists():
            _save(index_path, index_data, index_original)

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


def cmd_move_to_progress(args: argparse.Namespace) -> None:
    """イシューを targets/ から progress/ へ移し、_index.yaml の status を in_progress にする。"""
    issues_dir = Path(args.issues_dir)
    issue_id: str = args.issue_id

    targets_dir = issues_dir / "targets"
    progress_dir = issues_dir / "progress"
    src = targets_dir / f"{issue_id}.md"

    if not src.exists():
        print(f"Warning: {src} not found; skipping file move", file=sys.stderr)
    else:
        progress_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(progress_dir / f"{issue_id}.md"))
        print(f"Moved {issue_id}.md: targets/ → progress/")

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

    entry["status"] = "in_progress"
    index_data["issues"] = issues
    _save(index_path, index_data, index_original)
    print(f"Set {issue_id} status=in_progress")


def cmd_set_status(args: argparse.Namespace) -> None:
    """_index.yaml の該当イシューエントリの status を更新する（ファイルは移動しない）。"""
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


def cmd_add_branch(args: argparse.Namespace) -> None:
    """_index.yaml の該当イシューエントリの branches 配列にブランチ名を追記する。"""
    issues_dir = Path(args.issues_dir)
    issue_id: str = args.issue_id
    branch: str = args.branch

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

    branches: list[str] = entry.get("branches") or []
    if branch in branches:
        print(f"Skip: {issue_id} already has branch {branch}")
        return
    branches.append(branch)
    entry["branches"] = branches
    index_data["issues"] = issues
    _save(index_path, index_data, index_original)
    print(f"Added branch {branch} to {issue_id}")


def main() -> int:
    # 保護ブランチ (master/main/develop) 上では実行禁止
    assert_not_protected_branch("issue-tool.py")
    args = parse_args()
    handlers = {
        "close": cmd_close,
        "move-to-progress": cmd_move_to_progress,
        "set-status": cmd_set_status,
        "add-branch": cmd_add_branch,
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
    p_close.add_argument("--issue-id", required=True)
    p_close.add_argument("--resolution", required=True, choices=["resolved", "wontfix"])
    p_close.add_argument("--linked-branch", default=None)
    p_close.add_argument("--issues-dir", default=str(DEFAULT_ISSUES_DIR))

    p_prog = sub.add_parser("move-to-progress", help="targets/ から progress/ へ移し in_progress にする")
    p_prog.add_argument("--issue-id", required=True)
    p_prog.add_argument("--issues-dir", default=str(DEFAULT_ISSUES_DIR))

    p_status = sub.add_parser("set-status", help="_index.yaml の status を更新する（ファイルは移動しない）")
    p_status.add_argument("--issue-id", required=True)
    p_status.add_argument("--status", required=True, choices=["not_started", "in_progress"])
    p_status.add_argument("--issues-dir", default=str(DEFAULT_ISSUES_DIR))

    p_branch = sub.add_parser("add-branch", help="_index.yaml の branches にブランチ名を追記する")
    p_branch.add_argument("--issue-id", required=True)
    p_branch.add_argument("--branch", required=True)
    p_branch.add_argument("--issues-dir", default=str(DEFAULT_ISSUES_DIR))

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
