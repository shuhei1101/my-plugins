#!/usr/bin/env python3
"""
trim-index.py — Move completed PR entries from index.yaml to index.archive.yaml.

Usage:
    python trim-index.py [index_yaml_path]

Default path: .work/tasks/index.yaml (relative to cwd)

Reads index.yaml, moves all `completed: true` entries to index.archive.yaml,
and rewrites index.yaml with only active (`completed: false`) entries.
The `last_id` field is preserved/updated so PR numbering stays correct
even after completed entries are removed.
"""
import sys
import pathlib
import re


def parse_index_yaml(text: str) -> tuple[dict, list[dict]]:
    """Return (meta, prs) where meta has comment/last_id lines and prs is list of entry dicts."""
    import yaml
    data = yaml.safe_load(text)
    return data


def dump_entry(entry: dict) -> str:
    lines = [f"  - id: {entry['id']}"]
    lines.append(f"    title: '{entry['title']}'")
    lines.append(f"    type: {entry['type']}")
    tags = entry.get('tags', [])
    lines.append(f"    tags: {tags}")
    lines.append(f"    summary: '{entry['summary']}'")
    lines.append(f"    task: '{entry['task']}'")
    lines.append(f"    completed: {str(entry['completed']).lower()}")
    return '\n'.join(lines)


def main():
    index_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('.work/tasks/index.yaml')
    archive_path = index_path.parent / 'index.archive.yaml'

    if not index_path.exists():
        print(f'Error: {index_path} not found', file=sys.stderr)
        sys.exit(1)

    try:
        import yaml
    except ImportError:
        print('Error: PyYAML not installed. Run: pip install pyyaml', file=sys.stderr)
        sys.exit(1)

    text = index_path.read_text(encoding='utf-8')
    data = yaml.safe_load(text)

    prs = data.get('prs', [])
    last_id = data.get('last_id') or (max((p['id'] for p in prs), default=0))

    active = [p for p in prs if not p.get('completed', False)]
    done = [p for p in prs if p.get('completed', False)]

    if not done:
        print('Nothing to archive — no completed entries found.')
        return

    # Append completed entries to archive
    archive_header = ''
    if archive_path.exists():
        archive_text = archive_path.read_text(encoding='utf-8')
        archive_data = yaml.safe_load(archive_text) or {}
        existing = archive_data.get('prs', [])
        existing_ids = {p['id'] for p in existing}
        to_add = [p for p in done if p['id'] not in existing_ids]
        all_archived = existing + to_add
    else:
        archive_header = '# .work/tasks/index.archive.yaml — Archived (completed) PR entries\n\n'
        all_archived = done

    # Write archive
    archive_out = archive_header + yaml.dump(
        {'prs': all_archived},
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )
    archive_path.write_text(archive_out, encoding='utf-8')

    # Rewrite index.yaml preserving header comment and last_id
    header_lines = []
    for line in text.splitlines():
        if line.startswith('#'):
            header_lines.append(line)
        else:
            break
    header = '\n'.join(header_lines) + '\n\n' if header_lines else ''

    new_data = {'last_id': last_id, 'prs': active}
    index_out = header + yaml.dump(
        new_data,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )
    index_path.write_text(index_out, encoding='utf-8')

    print(f'Archived {len(done)} completed PR(s) to {archive_path}')
    print(f'index.yaml now has {len(active)} active PR(s), last_id={last_id}')


if __name__ == '__main__':
    main()
