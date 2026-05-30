---
paths:
  - "plugins/**"
  - ".claude-plugin/**"
---

# Plugin Work Rules

## Overview

Rules for creating and updating plugins in this marketplace. Auto-loads whenever a file under `plugins/**` or `.claude-plugin/**` is read or edited.

## Related Files

| File | Role |
|---|---|
| `plugins/{name}/.claude-plugin/plugin.json` | Plugin manifest (name, version, description) |
| `.claude-plugin/marketplace.json` | Marketplace catalog — must always match plugin.json version |
| `plugins/{name}/skills/{skill}/SKILL.md` | Skill definition |

## When Editing

Always update both before committing:

- [ ] `plugins/{name}/.claude-plugin/plugin.json` — bump `version`
- [ ] `.claude-plugin/marketplace.json` — bump the matching plugin's `version`

## plugin.json Format

```json
{
  "name": "{plugin-name}",
  "description": "{Short description of what this plugin does}",
  "version": "1.0.0"
}
```

- `name`: kebab-case identifier; also the skill namespace
- `version`: semantic versioning (`MAJOR.MINOR.PATCH`)

## marketplace.json Entry Format

```json
{
  "name": "{plugin-name}",
  "source": "./plugins/{plugin-name}",
  "description": "{Same as plugin.json description}",
  "version": "1.0.0"
}
```

## When Renaming Files or Skills

When a skill name, file name, or folder name is changed, other files in the same plugin may reference it. After any rename, always:

1. Search the entire plugin directory for the old name
2. Update every reference to the new name
3. Confirm no references remain before committing

> Skills can be referenced or called from `trigger` fields in SKILL.md or from steps in other skills. Renaming on the filesystem alone is not enough.

## Script Paths in Skills

When a skill (SKILL.md) step calls a script, never use `plugins/{name}/scripts/` — that path only works inside the `my-plugins` repository. When the plugin is installed in another project, the scripts live in the plugin cache. Always use `${CLAUDE_PLUGIN_ROOT}/scripts/` instead.

```bash
# Wrong — only works inside my-plugins
python plugins/work-kit/scripts/index-tool.py next-id ...

# Correct — works in any project
python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py" next-id ...
```

`${CLAUDE_PLUGIN_ROOT}` is the plugin root — two levels above `skills/{skill-name}/`.

---

## Version Bump Rules

| Change type | Bump | Example |
|---|---|---|
| Bug fix, minor correction | PATCH (`1.0.0` → `1.0.1`) | Fix a wrong command, typo in logic |
| New section, new capability | MINOR (`1.0.0` → `1.1.0`) | Add a new workflow section |
| Complete rewrite or breaking change | MAJOR (`1.0.0` → `2.0.0`) | Rethink the entire skill approach |
