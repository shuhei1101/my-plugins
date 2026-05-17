"""
trim-index — Move completed PR entries from index.yaml to index.archive.yaml.

Usage:
  python trim-index.py [index_yaml]

  index_yaml  Path to index.yaml (default: .work/tasks/index.yaml)

Reads index.yaml, moves all `completed: true` entries to index.archive.yaml
in the same directory, and rewrites index.yaml with only active entries.
The `last_id` field is preserved so PR numbering remains correct after
completed entries are removed.
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
ARCHIVE_NAME = "index.archive.yaml"
HEADER_COMMENT = "# .work/tasks/index.archive.yaml — Archived (completed) PR entries\n\n"


# ── private helpers ─────────────────────────────────────────
def _load(path: Path) -> dict:
    """Load a YAML file and return its content as a dict (empty dict if missing)."""
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _dump(data: dict) -> str:
    return yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)


def _header_comment(text: str) -> str:
    """Return the leading comment block from a YAML file."""
    lines = []
    for line in text.splitlines():
        if line.startswith("#"):
            lines.append(line)
        else:
            break
    return "\n".join(lines) + "\n\n" if lines else ""


# ── main ────────────────────────────────────────────────────
def main(args: argparse.Namespace) -> None:
    index_path = Path(args.index_yaml)
    archive_path = index_path.parent / ARCHIVE_NAME

    if not index_path.exists():
        print(f"Error: {index_path} not found", file=sys.stderr)
        sys.exit(1)

    raw = index_path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw) or {}

    prs: list[dict] = data.get("prs", [])
    last_id: int = data.get("last_id") or (max((p["id"] for p in prs), default=0))

    active = [p for p in prs if not p.get("completed", False)]
    done = [p for p in prs if p.get("completed", False)]

    if not done:
        print("Nothing to archive — no completed entries found.")
        return

    # Merge into archive (skip duplicates by id)
    archive_data = _load(archive_path)
    existing: list[dict] = archive_data.get("prs", [])
    existing_ids = {p["id"] for p in existing}
    merged = existing + [p for p in done if p["id"] not in existing_ids]

    prefix = HEADER_COMMENT if not archive_path.exists() else ""
    archive_path.write_text(prefix + _dump({"prs": merged}), encoding="utf-8")

    # Rewrite index.yaml: preserve header comment + last_id + active entries only
    comment = _header_comment(raw)
    index_path.write_text(comment + _dump({"last_id": last_id, "prs": active}), encoding="utf-8")

    print(f"Archived {len(done)} completed PR(s) to {archive_path}")
    print(f"index.yaml now has {len(active)} active PR(s), last_id={last_id}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "index_yaml",
        nargs="?",
        default=str(DEFAULT_INDEX),
        help=f"Path to index.yaml (default: {DEFAULT_INDEX})",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
