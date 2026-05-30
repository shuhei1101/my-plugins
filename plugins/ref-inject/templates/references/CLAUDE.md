# __PLUGIN_NAME__ references

Reference docs auto-injected by the `__LOG_TAG__` hook based on the edited file path.

## Reading manually

- `_index.yaml` — the list of all references (path + one-line description; parsed by the hook)
- `_injection_rules.yaml` — edit-path pattern → `required` / `optional` references

## Reading automatically

On `PreToolUse(Edit | Write | MultiEdit | Read)`, `hooks/scripts/inject_references.py`:

1. Matches the edited file path against `_injection_rules.yaml` patterns
2. Injects each matched `required` reference **in full body**, and each `optional` as **path + description only**
3. De-dupes via a two-tier TTL token at `~/.claude/tokens/__PLUGIN_NAME__/{session_id}.yaml`
   (re-injects once `__ENV_PREFIX___INJECTION_TTL` seconds elapse, default __DEFAULT_TTL__):
   - `patterns`: a matched pattern is skipped entirely while still fresh
   - `references`: a `required` reference whose body was already injected this session (via any
     pattern) is shown by **path only**, so a reference shared across patterns is never re-injected

Set `__ENV_PREFIX___INJECTION_LANG=jp` to inject Japanese descriptions (`_index.jp.yaml` + `injection.jp.md.j2`).

## Maintenance

- Add a reference: create the file, add it to `_index.yaml` (+ `_index.jp.yaml`), bind it to a pattern in `_injection_rules.yaml`
- Keep `1 reference = 1 use case` so a single edited file does not pull in unrelated docs
- After editing `_injection_rules.yaml`, verify no reference is orphaned (listed in index but bound to no pattern, or vice versa)
