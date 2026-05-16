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

## Prerequisite

All plugin work must be done in a worktree. Never commit directly to master.

```bash
/wt:wt
```

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

## SKILL.md Frontmatter

```yaml
---
name: {skill-name}
description: {When to trigger and what the skill does. Include specific phrases and contexts.}
---
```

## marketplace.json Entry Format

```json
{
  "name": "{plugin-name}",
  "source": "./plugins/{plugin-name}",
  "description": "{Same as plugin.json description}",
  "version": "1.0.0"
}
```

## Version Bump Rules

| Change type | Bump | Example |
|---|---|---|
| Bug fix, minor correction | PATCH (`1.0.0` → `1.0.1`) | Fix a wrong command, typo in logic |
| New section, new capability | MINOR (`1.0.0` → `1.1.0`) | Add a new workflow section |
| Complete rewrite or breaking change | MAJOR (`1.0.0` → `2.0.0`) | Rethink the entire skill approach |

## Local Testing

```bash
/plugin marketplace add ./
/plugin install {plugin-name}@my-plugins   # choose Local scope
# Clean up after testing
/plugin uninstall {plugin-name}@my-plugins
/plugin marketplace remove my-plugins
```
