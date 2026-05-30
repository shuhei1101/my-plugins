"""
issue-tool — workspace の `.work/issues/` 操作用 CLI。

使い方:
  python issue-tool.py close --issue-id ISSUE-N --resolution {resolved|wontfix} --linked-pr N [--issues-dir .work/issues]

サブコマンド:
  close          イシューを 1 件クローズする:
                   1. .work/issues/ISSUE-{N}.md を .work/issues/closed/ISSUE-{N}.md に移動
                   2. _index.yaml から該当エントリを削除
                   3. _index.archive.yaml の closed_issues に linked_pr 付きで追記

`.work/issues/` 配下の YAML 読み書きをこのスクリプト経由に集約することで、
Claude Code のコンテキストに YAML ファイルを丸ごと読み込ませずに済み、
issue-save と同じフォーマットで一貫した書き込みができる。
"""

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
    print("Error: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
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
    linked_pr: int = args.linked_pr

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
    closed_issues.append({
        "id": issue_id,
        "title": entry.get("title", ""),
        "closed": date.today().isoformat(),
        "resolution": resolution,
        "linked_pr": linked_pr,
        "tags": entry.get("tags", []) or [],
    })
    archive_data["closed_issues"] = closed_issues
    if "scan_records" not in archive_data:
        archive_data["scan_records"] = []
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    _save(archive_path, archive_data, archive_original)

    print(f"Closed {issue_id} (resolution={resolution}, linked_pr=PR{linked_pr})")


# ── main ────────────────────────────────────────────────────
def main(args: argparse.Namespace) -> None:
    handlers = {
        "close": cmd_close,
    }
    handlers[args.subcommand](args)


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
    p_close.add_argument("--linked-pr", required=True, type=int, help="このイシューをクローズした PR 番号")
    p_close.add_argument("--issues-dir", default=str(DEFAULT_ISSUES_DIR), help=".work/issues/ のパス")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
