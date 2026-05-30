You just edited or created a file under this plugin's `references/` directory. Before continuing, verify the path is registered correctly:

## Checks

1. **Added a new reference file?**
   - Register it in `references/_index.yaml` and `references/_index.jp.yaml` with both `path` and `description`
   - Add a matching `pattern` entry in `references/_injection_rules.yaml` (under `required` or `optional`) if the new reference should be auto-injected for some path pattern

2. **Renamed or moved a reference file?**
   - Update every occurrence of the old path inside `_index.yaml`, `_index.jp.yaml`, and `_injection_rules.yaml` to the new path

3. **Only edited the body of an existing reference?**
   - No registry update needed — you can ignore this reminder

## Suggested action

When (1) or (2) applies, open `_index.yaml` and `_injection_rules.yaml` with `Read` and confirm the edited/created file's path is present (or intentionally absent). Fix missing entries; otherwise do nothing.

This reminder fires only once per session.
