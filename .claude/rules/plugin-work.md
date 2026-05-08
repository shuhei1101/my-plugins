---
paths:
  - "plugins/**"
  - ".claude-plugin/**"
---

# Plugin Work Rules

## Prerequisite: Always Use a Worktree

Before creating or updating any plugin, use the `wt` skill to create a worktree and branch.

```bash
/wt:wt
```

Never work directly on the main branch.

---

## When Editing Any Plugin File

**Always update both version references before committing:**

- [ ] `plugins/{plugin-name}/.claude-plugin/plugin.json` — bump `version`
- [ ] `.claude-plugin/marketplace.json` — bump the matching plugin's `version`

Forgetting either will leave the catalog out of sync with the installed plugin.

---

## Creating a New Plugin

### 1. Create the plugin directory

```
plugins/{plugin-name}/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── {skill-name}/
        └── SKILL.md
```

### 2. Write plugin.json

```json
{
  "name": "{plugin-name}",
  "description": "{Short description of what this plugin does}",
  "version": "1.0.0"
}
```

Field rules:
- `name`: kebab-case identifier; also used as the skill namespace
- `version`: semantic versioning (`MAJOR.MINOR.PATCH`)

### 3. Write SKILL.md

```markdown
---
name: {skill-name}
description: {When to trigger and what the skill does. Include specific phrases and contexts.}
---

# {Skill Title}

{Skill instructions in English. All content here — no external reference files.}
```

### 4. Register in marketplace.json

Add an entry to `.claude-plugin/marketplace.json`:

```json
{
  "name": "{plugin-name}",
  "source": "./plugins/{plugin-name}",
  "description": "{Same as plugin.json description}",
  "version": "1.0.0"
}
```

### 5. Test locally

```bash
# Test the plugin in isolation
claude --plugin-dir ./plugins/{plugin-name}

# Or test the full marketplace
claude
/plugin marketplace add ./
/plugin install {plugin-name}@my-plugins   # choose Local scope for testing
```

After installing, reload and verify the skill triggers as expected. Clean up when done:

```bash
/plugin uninstall {plugin-name}@my-plugins
/plugin marketplace remove my-plugins
```

---

## Updating an Existing Plugin

### Version bump rules

| Change type | Version bump | Example |
|-------------|-------------|---------|
| Bug fix, minor correction | PATCH (`1.0.0` → `1.0.1`) | Fix a wrong command, typo in logic |
| New section, new capability | MINOR (`1.0.0` → `1.1.0`) | Add a new workflow section |
| Complete rewrite or breaking change | MAJOR (`1.0.0` → `2.0.0`) | Rethink the entire skill approach |
