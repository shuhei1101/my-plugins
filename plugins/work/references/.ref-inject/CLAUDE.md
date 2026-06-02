# work references

This folder contains reference documents auto-injected by the work plugin's `inject_references.py`
hook when you edit matching files.

## Reading manually

To read a reference, use the `Read` tool with the absolute path:

```
Read: plugins/work/references/{filename}.md
```

## Reading automatically

The `PreToolUse` injection hook fires on `Edit / Write / MultiEdit / Read` and matches the edited
file path against `references/_injection_rules.yaml`. Matched `required` references are injected in
full; `optional` references are injected as path + description only.

Injection is de-duped per session via a TTL token at `~/.claude/tokens/work/{session_id}.yaml`.
Re-injection happens once the TTL elapses (default 3600s; override with `WORK_INJECTION_TTL`).

## Reference list

See `_index.yaml` for the full list with descriptions.

## Maintenance

- **Adding a reference**: add an entry to `_index.yaml` (and `_index.jp.yaml`), then add a pattern to `_injection_rules.yaml`
- **Removing a reference**: remove from `_index.yaml`, `_index.jp.yaml`, and `_injection_rules.yaml`
- **Updating a reference**: update the `.md` and its `.jp.md` mirror in the same commit
