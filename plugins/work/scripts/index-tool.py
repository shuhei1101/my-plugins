"""
index-tool — CLI for workspace index.yaml operations.

Usage:
  python index-tool.py add [index_yaml] --branch B --title T --type T --summary S --task T [--created YYYY-MM-DD]
  python index-tool.py list-active [index_yaml]
  python index-tool.py completed-count [index_yaml]
  python index-tool.py set-completed [index_yaml] --branch B
  python index-tool.py archive [index_yaml] [archive_yaml]

  index_yaml   Path to index.yaml (default: .work/tasks/index.yaml)
  archive_yaml Path to index.archive.yaml (default: .work/tasks/index.archive.yaml)

Subcommands:
  add              Append a new branch entry
  list-active      Print active (completed: false) entries as lines:
                     branch|title|type|task
  completed-count  Print the number of completed entries
  set-completed    Mark a branch entry (matched by --branch) as completed: true
  archive          Move completed entries from index.yaml to index.archive.yaml.
                   Prints the number of entries moved.

The branch index is keyed by the `branch` name. Each entry has the fields:
  branch, created, title, type, summary, task, completed
The top-level document is `{branches: [...]}` — there is no numeric id or last_id.
`created` (YYYY-MM-DD, set at add time) is a surrogate that disambiguates same-named
branches recurring over time in the archive; it is not a counter.

By routing index.yaml operations through this script, Claude Code avoids
loading the full YAML file into its context window.
"""

# ── stdlib ──────────────────────────────────────────────────
import argparse
import datetime
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── third-party ─────────────────────────────────────────────
try:
    import yaml  # pip install pyyaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ── constants ───────────────────────────────────────────────
DEFAULT_INDEX = Path(".work/tasks/index.yaml")
DEFAULT_ARCHIVE = Path(".work/tasks/index.archive.yaml")


# ── private helpers ─────────────────────────────────────────
def _load(path: Path) -> dict:
    """Return parsed YAML content, or empty dict if the file is missing."""
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _save(path: Path, data: dict, original_text: str) -> None:
    """Write data back to path, preserving any leading comment lines."""
    comment_lines = [l for l in original_text.splitlines() if l.startswith("#")]
    header = "\n".join(comment_lines) + "\n\n" if comment_lines else ""
    path.write_text(header + yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False), encoding="utf-8")


# ── subcommand handlers ──────────────────────────────────────
def cmd_add(args: argparse.Namespace) -> None:
    """Append a new branch entry."""
    if not args.created:
        args.created = datetime.date.today().isoformat()
    index_path = Path(args.index_yaml)
    original = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    data = yaml.safe_load(original) or {} if original else {}

    branches: list[dict] = data.get("branches", [])
    new_entry = {
        "branch": args.branch,
        "created": args.created,
        "title": args.title,
        "type": args.type,
        "summary": args.summary,
        "task": args.task,
        "completed": False,
    }
    branches.append(new_entry)
    data["branches"] = branches

    _save(index_path, data, original)
    print(f"Added entry {args.branch} to {index_path}")


def cmd_list_active(args: argparse.Namespace) -> None:
    """Print active branch entries, one per line: branch|title|type|task"""
    index_path = Path(args.index_yaml)
    data = _load(index_path)
    active = [p for p in data.get("branches", []) if not p.get("completed", False)]
    for p in active:
        print(f"{p.get('branch', '')}|{p.get('title', '')}|{p.get('type', '')}|{p.get('task', '')}")


def cmd_completed_count(args: argparse.Namespace) -> None:
    """Print the number of completed entries."""
    index_path = Path(args.index_yaml)
    data = _load(index_path)
    count = sum(1 for p in data.get("branches", []) if p.get("completed", False))
    print(count)


def cmd_set_completed(args: argparse.Namespace) -> None:
    """Mark a specific branch entry (matched by --branch) as completed: true."""
    index_path = Path(args.index_yaml)
    original = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    data = yaml.safe_load(original) or {} if original else {}

    branches: list[dict] = data.get("branches", [])
    target = next((p for p in branches if p.get("branch") == args.branch), None)
    if target is None:
        print(f"Error: branch {args.branch} not found in {index_path}", file=sys.stderr)
        sys.exit(1)

    target["completed"] = True
    data["branches"] = branches
    _save(index_path, data, original)
    print(f"Branch {args.branch} marked as completed in {index_path}")


def cmd_archive(args: argparse.Namespace) -> None:
    """Move completed entries from index.yaml to index.archive.yaml."""
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

    # Append to archive
    archive_original = archive_path.read_text(encoding="utf-8") if archive_path.exists() else ""
    archive_data = yaml.safe_load(archive_original) or {} if archive_original else {}
    archive_branches: list[dict] = archive_data.get("branches", [])
    archive_branches.extend(completed)
    archive_data["branches"] = archive_branches
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    _save(archive_path, archive_data, archive_original)

    # Remove from index
    data["branches"] = remaining
    _save(index_path, data, original)

    print(len(completed))


# ── main ────────────────────────────────────────────────────
def main(args: argparse.Namespace) -> None:
    handlers = {
        "add": cmd_add,
        "list-active": cmd_list_active,
        "completed-count": cmd_completed_count,
        "set-completed": cmd_set_completed,
        "archive": cmd_archive,
    }
    handlers[args.subcommand](args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    # add
    p_add = sub.add_parser("add", help="Add a new branch entry")
    p_add.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))
    p_add.add_argument("--branch", required=True)
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--type", required=True, dest="type")
    p_add.add_argument("--summary", required=True)
    p_add.add_argument("--task", required=True)
    p_add.add_argument(
        "--created",
        default=None,
        help="Creation date YYYY-MM-DD. Defaults to today. Acts as a surrogate to "
             "disambiguate same-named branches across time in the archive.",
    )

    # list-active
    p_list = sub.add_parser("list-active", help="List active (not completed) branches")
    p_list.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))

    # completed-count
    p_count = sub.add_parser("completed-count", help="Print count of completed entries")
    p_count.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))

    # set-completed
    p_set = sub.add_parser("set-completed", help="Mark a branch entry as completed")
    p_set.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))
    p_set.add_argument("--branch", required=True)

    # archive
    p_archive = sub.add_parser("archive", help="Move completed entries to archive file")
    p_archive.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))
    p_archive.add_argument("archive_yaml", nargs="?", default=str(DEFAULT_ARCHIVE))

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
