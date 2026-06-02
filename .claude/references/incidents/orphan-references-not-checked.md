# Orphan references not checked after adding (PR140)

## What happened

py-kit references were rebuilt into 38 → 43 files across 10 topic folders. `injection_rules.yaml` was authored by hand. After the third commit, the user asked: "ちゃんと全部のフォルダに紐づくようになっているか調べて". A quick YAML-vs-filesystem diff script revealed **5 references were orphans** (existed under `references/` but were not referenced by any `rules[].pattern`):

- `scripts/python-script.md`
- `scripts/tkinter.md`
- `fastapi/health.md`
- `performance/cheatsheet.md`
- `architecture/refactoring-judgement.md`

The orphans were files for which AI either:
- Forgot to add a binding rule when creating the reference
- Assumed they'd be invoked manually only (e.g. `cheatsheet.md`, `tkinter.md`)
- Created the reference as a "fallback explanation" without a path pattern in mind

## Root cause

AI added references without a verification step. When 38+ references and 20+ rules are juggled in one pass, **silent drift between the two sets is invisible** without scripted checking.

## Lesson

**After every `injection_rules.yaml` edit, run an orphan-check script.** Minimal Python (no extra deps beyond pyyaml):

```python
import yaml, pathlib
refs_dir = pathlib.Path('plugins/py-kit/references')
rules = yaml.safe_load((refs_dir / 'injection_rules.yaml').read_text(encoding='utf-8'))['rules']

used = set()
for r in rules:
    for k in ('required', 'optional'):
        for p in r.get(k) or []:
            used.add(p)

existing = {
    md.relative_to(refs_dir).as_posix()
    for md in refs_dir.glob('**/*.md')
    if md.name not in ('CLAUDE.md', 'CLAUDE.jp.md')
    and not md.name.endswith('.jp.md')
}

orphans = sorted(existing - used)
unknowns = sorted(used - existing)
print('orphan:', orphans)
print('unknown:', unknowns)
```

Run on:
- Any new reference creation
- Any `injection_rules.yaml` edit
- Before merging PRs that touch references

For references that genuinely have no path-pattern home (e.g. `performance/cheatsheet.md` — only loaded during manual profiling work), document the intentional exception in `injection_rules.yaml` as a YAML comment **or** assign a best-fit pattern (e.g. `**/benchmarks/**/*.py`).

## Related

- PR140 fix: commit 2492991 (added 5 patterns to absorb the orphans)
- Same pattern would apply to any plugin using `references/` + `injection_rules.yaml`
