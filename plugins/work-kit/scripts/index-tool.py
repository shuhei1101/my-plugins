"""
index-tool — CLI for work-kit index.yaml operations.

Usage:
  python index-tool.py next-id [index_yaml]
  python index-tool.py add [index_yaml] --id N --title T --type T --summary S --task T
  python index-tool.py list-active [index_yaml]

  index_yaml  Path to index.yaml (default: .work/tasks/index.yaml)

Subcommands:
  next-id      Print the next available PR number (last_id + 1, or 1 if absent)
  add          Append a new PR entry and update last_id
  list-active  Print active (completed: false) PR entries as lines:
                 id|title|type|task

By routing index.yaml operations through this script, Claude Code avoids
loading the full YAML file into its context window.
"""

# ── stdlib ──────────────────────────────────────────────────
import argparse
import sys
from pathlib import Path

# ── third-party ─────────────────────────────────────────────
try:
    import yaml  # pip install pyyaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ── constants ───────────────────────────────────────────────
DEFAULT_INDEX = Path(".work/tasks/index.yaml")


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
def cmd_next_id(args: argparse.Namespace) -> None:
    """Print the next PR number."""
    index_path = Path(args.index_yaml)
    data = _load(index_path)
    prs: list[dict] = data.get("prs", [])
    last_id: int = data.get("last_id") or (max((p["id"] for p in prs), default=0))
    print(last_id + 1)


def cmd_add(args: argparse.Namespace) -> None:
    """Append a new PR entry and update last_id."""
    index_path = Path(args.index_yaml)
    original = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    data = yaml.safe_load(original) or {} if original else {}

    prs: list[dict] = data.get("prs", [])
    new_entry = {
        "id": args.id,
        "title": args.title,
        "type": args.type,
        "tags": [],
        "summary": args.summary,
        "task": args.task,
        "completed": False,
    }
    prs.append(new_entry)
    data["prs"] = prs
    data["last_id"] = args.id

    _save(index_path, data, original)
    print(f"Added PR{args.id} to {index_path}")


def cmd_list_active(args: argparse.Namespace) -> None:
    """Print active PR entries, one per line: id|title|type|task"""
    index_path = Path(args.index_yaml)
    data = _load(index_path)
    active = [p for p in data.get("prs", []) if not p.get("completed", False)]
    for p in active:
        print(f"{p['id']}|{p['title']}|{p['type']}|{p['task']}")


def cmd_completed_count(args: argparse.Namespace) -> None:
    """Print the number of completed PR entries."""
    index_path = Path(args.index_yaml)
    data = _load(index_path)
    count = sum(1 for p in data.get("prs", []) if p.get("completed", False))
    print(count)


# ── main ────────────────────────────────────────────────────
def main(args: argparse.Namespace) -> None:
    handlers = {
        "next-id": cmd_next_id,
        "add": cmd_add,
        "list-active": cmd_list_active,
        "completed-count": cmd_completed_count,
    }
    handlers[args.subcommand](args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    # next-id
    p_next = sub.add_parser("next-id", help="Print next PR number")
    p_next.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))

    # add
    p_add = sub.add_parser("add", help="Add a new PR entry")
    p_add.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))
    p_add.add_argument("--id", type=int, required=True)
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--type", required=True, dest="type")
    p_add.add_argument("--summary", required=True)
    p_add.add_argument("--task", required=True)

    # list-active
    p_list = sub.add_parser("list-active", help="List active (not completed) PRs")
    p_list.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))

    # completed-count
    p_count = sub.add_parser("completed-count", help="Print count of completed PRs")
    p_count.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
