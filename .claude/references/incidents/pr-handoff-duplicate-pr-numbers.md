# Incident: pr-handoff Reserves Two Candidates with the Same PR Number

## Date

2026-05-30

## What happened

`/work-kit:pr-handoff` reserved two next-PR candidates and both received `id: 165` in `index.yaml`.
The result was two entries with the same id:

```yaml
- id: 165
  title: PR165 — add-plugin-config-skill
  ...
- id: 165
  title: PR165 — remove-mark-generated
  ...
```

When the user asked to "start PR165", two worktrees existed (`my-plugins-wt-PR165` and
`my-plugins-wt-PR165b`) and it was unclear which to use.

## Why it happened

`pr-handoff` calls `/work-kit:work-start` for each "即時実施可" candidate in sequence, but
`index.yaml` is gitignored and only updated locally. If two work-start calls run close together
and both read `last_id: 164`, both write `last_id: 165` — resulting in duplicate IDs.

## Fix applied

1. Renamed branch `PR165/feat/add-plugin-config-skill` → `PR167/feat/add-plugin-config-skill`
2. Moved worktree from `my-plugins-wt-PR165` → `my-plugins-wt-PR167`
3. Updated `index.yaml`: changed `id: 165` (add-plugin-config-skill) → `id: 167`, `last_id: 166` → `167`
4. Renamed task folder `PR165/` → `PR167/` and updated TODO.md heading

## Prevention

After any `pr-handoff` run that reserves multiple candidates, verify there are no duplicate IDs:

```bash
python -c "
import yaml
data = yaml.safe_load(open('.work/tasks/index.yaml'))
ids = [p['id'] for p in data.get('prs', [])]
dupes = [i for i in ids if ids.count(i) > 1]
print('Duplicates:', dupes if dupes else 'none')
"
```

If duplicates are found, manually renumber the later-reserved PR to `last_id + 1` and update:
- `index.yaml` entry id and title
- Branch name (`git branch -m`)
- Worktree path (remove + re-add)
- Task folder (`PR{old}/` → `PR{new}/`)
- TODO.md heading

Ideally, fix `index-tool.py`'s `add` command to re-read `last_id` atomically before writing,
or pr-handoff to reserve candidates sequentially with a delay.
