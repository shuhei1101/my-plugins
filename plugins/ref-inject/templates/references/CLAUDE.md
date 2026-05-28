# __PLUGIN_NAME__ references

Reference docs auto-injected by the `__LOG_TAG__` hook based on the edited file path.

## Reading manually

- `index.yaml` — the list of all references (path + one-line description; parsed by the hook)
- `injection_rules.yaml` — edit-path pattern → `required` / `optional` references

## Reading automatically

On `PreToolUse(Edit | Write | MultiEdit | Read)`, `hooks/inject_references.py`:

1. Matches the edited file path against `injection_rules.yaml` patterns
2. Injects each matched `required` reference **in full body**, and each `optional` as **path + description only**
3. De-dupes via a per-pattern TTL token at `~/.claude/tokens/__PLUGIN_NAME__/{session_id}.yaml`
   (re-injects after `__ENV_PREFIX___INJECTION_TTL` seconds, default __DEFAULT_TTL__)
4. `hooks/refresh_on_compact.py` clears the token on `PreCompact` so references re-inject after `/compact`

Set `__ENV_PREFIX___INJECTION_LANG=jp` to inject Japanese descriptions (`index.jp.yaml` + `injection.jp.md.j2`).

## Maintenance

- Add a reference: create the file, add it to `index.yaml` (+ `index.jp.yaml`), bind it to a pattern in `injection_rules.yaml`
- Keep `1 reference = 1 use case` so a single edited file does not pull in unrelated docs
- After editing `injection_rules.yaml`, verify no reference is orphaned (listed in index but bound to no pattern, or vice versa)
