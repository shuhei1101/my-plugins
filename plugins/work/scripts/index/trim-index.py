"""
trim-index.py — keep index.yaml small by trimming completed entries.

Reads index.yaml, keeps all active (completed: false) entries plus the most
recent N completed ones, and rewrites the file. Older completed entries are
dropped (they remain in index.archive.yaml if they were archived).

Usage:
    python trim-index.py [index_yaml] [--keep N]

Entries are keyed by `branch`; "most recent" means latest in list order.
"""

import argparse
import sys
from pathlib import Path

# 共通ガード (scripts/_branch_guard.py)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _branch_guard import assert_not_protected_branch  # noqa: E402

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

DEFAULT_INDEX = Path(".work/tasks/index.yaml")


def _dump(data: dict) -> str:
    return yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)


def main() -> None:
    # 保護ブランチ (master/main/develop) 上では実行禁止
    assert_not_protected_branch("trim-index.py")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("index_yaml", nargs="?", default=str(DEFAULT_INDEX))
    parser.add_argument("--keep", type=int, default=20)
    args = parser.parse_args()

    index_path = Path(args.index_yaml)
    if not index_path.exists():
        print(f"Error: {index_path} not found", file=sys.stderr)
        sys.exit(1)

    original = index_path.read_text(encoding="utf-8")
    data = yaml.safe_load(original) or {}

    branches = data.get("branches", [])
    active = [p for p in branches if not p.get("completed", False)]
    done = [p for p in branches if p.get("completed", False)]

    # keep the most recent N completed entries (latest in list order)
    kept_done = done[-args.keep:] if args.keep > 0 else []

    # ── merge, preserving order: active first, then kept completed ──
    merged = active + kept_done

    # de-dup by branch, keep first occurrence
    seen = set()
    deduped = []
    for p in merged:
        key = p.get("branch")
        if key in seen:
            continue
        seen.add(key)
        deduped.append(p)

    # write back: comment header + branches
    comment = "".join(l for l in original.splitlines(keepends=True) if l.lstrip().startswith("#"))
    index_path.write_text(comment + _dump({"branches": deduped}), encoding="utf-8")
    print(f"index.yaml: kept {len(active)} active + {len(kept_done)} completed")


if __name__ == "__main__":
    main()
