"""
sync_rules.py — Sync a project's edited rule back to the rule-market template library.

Usage:
    python sync_rules.py sync <project-root> <rule-name>

Example:
    python sync_rules.py sync C:/Users/me/repo/myproject cascade-sync

What it does:
    Copies PROJECT/.claude/rules/<rule-name>.md
         → <plugin>/skills/rule-market/rules/<rule-name>.md

The JP mirror is NOT auto-synced — update rules-jp/ manually after running this script.
"""

import sys
from pathlib import Path


def sync(project_root: str, rule_name: str) -> None:
    project = Path(project_root).resolve()
    src = project / ".claude" / "rules" / f"{rule_name}.md"
    if not src.exists():
        print(f"ERROR: {src} not found", file=sys.stderr)
        sys.exit(1)

    plugin_rules = Path(__file__).parent.parent / "rules"
    dst = plugin_rules / f"{rule_name}.md"
    if not plugin_rules.exists():
        print(f"ERROR: plugin rules directory not found: {plugin_rules}", file=sys.stderr)
        sys.exit(1)

    content = src.read_text(encoding="utf-8")
    dst.write_text(content, encoding="utf-8")
    print(f"Synced: {src}")
    print(f"    -> {dst}")
    print()
    print("Next steps:")
    print(f"  1. Update rules-jp/{rule_name}.md (JP mirror) manually")
    print("  2. Bump plugin version in .claude-plugin/plugin.json")
    print("  3. Commit both files together")


def main() -> None:
    if len(sys.argv) < 4 or sys.argv[1] != "sync":
        print(__doc__)
        sys.exit(1)
    sync(project_root=sys.argv[2], rule_name=sys.argv[3])


if __name__ == "__main__":
    main()
