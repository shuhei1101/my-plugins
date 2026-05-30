---
paths:
  - "plugins/*/.claude-plugin/plugin.json"
  - ".claude-plugin/marketplace.json"
---

# Plugin Manifest Sync Rules

When editing `plugins/{name}/.claude-plugin/plugin.json`, **always update `.claude-plugin/marketplace.json` in the same commit**.

`plugin.json` is the plugin's self-declaration; `marketplace.json` is the catalog source. Updating only one leaves the plugin listed under its old name or path, breaking installation.

## Related Files

| File path | Role |
|---|---|
| `plugins/{name}/.claude-plugin/plugin.json` | Plugin manifest (name / description / version) |
| `.claude-plugin/marketplace.json` | Full plugin catalog (name / source / description / version) |
| `.claude/rules/feature/plugin-manifest-sync.md` | This rule |

## When Editing

Always check the counterpart file:

- [ ] Changed `name` in `plugin.json` → updated `name` and `source` in the matching `marketplace.json` entry?
- [ ] Changed `description` in `plugin.json` → updated `description` in the matching `marketplace.json` entry?
- [ ] Changed `version` in `plugin.json` → updated `version` in the matching `marketplace.json` entry?
- [ ] Renamed the plugin folder with `git mv` → `marketplace.json` `source` path points to the new folder name?
- [ ] Added a new file to this domain → updated this rule's `paths:` and Related Files list?

## Rule Maintenance

When performing file operations in this domain:
- **Added a new file** → add it to `paths:` and the Related Files list
- **Deleted or renamed a file** → remove or update it in `paths:` and Related Files
- **Domain responsibilities changed** → update the Overview section
