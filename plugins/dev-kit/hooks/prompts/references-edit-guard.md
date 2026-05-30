You are about to edit or create a file under this plugin's `references/` directory. **Before performing the edit**, verify the registration so a missing entry doesn't slip through.

## Checks

1. **About to add a new reference file?**
   - Before (or right after) creating it, register the path in `references/_index.yaml` and `references/_index.jp.yaml` with `path` + `description`
   - If the new reference should be auto-injected for some path pattern, add a matching `pattern` entry in `references/_injection_rules.yaml` (under `required` or `optional`)

2. **About to rename or move a reference file?**
   - Update every occurrence of the old path inside `_index.yaml`, `_index.jp.yaml`, and `_injection_rules.yaml` in the same change

3. **Just editing the body of an existing reference?**
   - No registry update needed — proceed with the edit as planned

## Suggested action

When (1) or (2) applies, open `_index.yaml` and `_injection_rules.yaml` with `Read` first and treat the registry update as part of the same change. This way the registry never drifts behind the actual `references/` files.

This reminder fires only once per session.
