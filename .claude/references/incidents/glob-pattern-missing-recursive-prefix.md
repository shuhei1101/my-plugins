# Glob pattern missing `**/` prefix for monorepo (PR140)

## What happened

While adding a rule for "Python files under `tools/` should pull in `python-script.md`", AI wrote:

```yaml
- pattern: "tools/**/*.py"
  required: [scripts/python-script.md]
```

User caught it: **「**/tools/ ってしなくていいの？」**.

The pattern `tools/**/*.py` only matches `tools/foo.py` / `tools/sub/bar.py` at the project root. It does **not** match `packages/foo/tools/bar.py` or `apps/web/tools/script.py` in a monorepo structure. AI had not considered that py-kit might be applied to a multi-package repo.

Fixed to `**/tools/**/*.py` which matches at any depth.

## Root cause

When writing path patterns for "by-convention folder names" (tools, scripts, tests, gui, etc.), AI defaulted to root-relative thinking. But:

- Many real projects are monorepos with multiple package roots
- Even non-monorepos may nest helper folders deep (e.g. `backend/services/api/tools/`)
- The original PR (PR140) targeted py-kit which has no opinion about repo layout — it must work in both flat and nested layouts

## Lesson

**For "by-name folder" path patterns in glob rules, prefix with `**/` by default.**

| Pattern | Matches | Use when |
|---|---|---|
| `tools/**/*.py` | Only root-level `tools/` | You specifically want to exclude nested `tools/` |
| `**/tools/**/*.py` | `tools/` at any depth | Default — works in flat and monorepo layouts |
| `src/tools/**/*.py` | Only `src/tools/` | You want a single specific location |

Apply to: `tools/`, `scripts/`, `tests/`, `gui/`, `benchmarks/`, `perf/`, and any conventional folder name. Reserve root-anchored patterns for files that *must* be at the project root (e.g. `.env`, `pyproject.toml`, `tsconfig.json`).

## Related

- PR140 fix: commit f1fd5ac
- See also `plugins/py-kit/references/injection_rules.yaml` — most folder-name patterns use `**/`
