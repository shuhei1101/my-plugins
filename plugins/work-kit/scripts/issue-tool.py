"""
issue-tool — CLI for work-kit `.work/issues/` operations.

Usage:
  python issue-tool.py close --issue-id ISSUE-N --resolution {resolved|wontfix} --linked-pr N [--issues-dir .work/issues]

Subcommands:
  close          Close one issue:
                   1. Move .work/issues/ISSUE-{N}.md -> .work/issues/closed/ISSUE-{N}.md
                   2. Remove the entry from _index.yaml
                   3. Append a closed_issues entry to _index.archive.yaml (with linked_pr)

By routing `.work/issues/` operations through this script, Claude Code avoids
loading the YAML files into its context window and keeps the format consistent
with issue-save.
"""

# ── stdlib ──────────────────────────────────────────────────
import argparse
import shutil
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── third-party ─────────────────────────────────────────────
try:
    import yaml  # pip install pyyaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ── constants ───────────────────────────────────────────────
DEFAULT_ISSUES_DIR = Path(".work/issues")


# ── private helpers ─────────────────────────────────────────
def _load(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _save(path: Path, data: dict, original_text: str) -> None:
    """Write data back, preserving any leading comment lines."""
    comment_lines = [l for l in original_text.splitlines() if l.startswith("#")]
    header = "\n".join(comment_lines) + "\n\n" if comment_lines else ""
    path.write_text(
        header + yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )


# ── subcommand handlers ──────────────────────────────────────
def cmd_close(args: argparse.Namespace) -> None:
    """Close one issue: move file, update _index.yaml, append to _index.archive.yaml."""
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

    # 1. Read _index.yaml to capture the issue entry before removing it.
    index_original = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    index_data: dict = yaml.safe_load(index_original) or {} if index_original else {}
    issues: list[dict] = index_data.get("issues", [])
    entry = next((i for i in issues if i.get("id") == issue_id), None)
    if entry is None:
        print(f"Warning: {issue_id} not found in {index_path}", file=sys.stderr)
        entry = {"id": issue_id, "title": "", "tags": []}

    # 2. Move the issue file to closed/ (if present).
    if issue_file.exists():
        closed_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(issue_file), str(closed_dir / issue_file.name))
    else:
        print(f"Warning: {issue_file} not found; skipping file move", file=sys.stderr)

    # 3. Remove from _index.yaml.
    if entry in issues:
        issues.remove(entry)
        index_data["issues"] = issues
        if index_path.exists():
            _save(index_path, index_data, index_original)

    # 4. Append to _index.archive.yaml.closed_issues.
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

    p_close = sub.add_parser("close", help="Close one issue and record it in the archive")
    p_close.add_argument("--issue-id", required=True, help="e.g. ISSUE-001")
    p_close.add_argument(
        "--resolution",
        required=True,
        choices=["resolved", "wontfix"],
        help="How the issue was resolved",
    )
    p_close.add_argument("--linked-pr", required=True, type=int, help="PR number that closed this issue")
    p_close.add_argument("--issues-dir", default=str(DEFAULT_ISSUES_DIR), help="Path to .work/issues/")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
