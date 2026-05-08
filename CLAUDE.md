# CLAUDE.md — my-plugins Developer Guide

This repository is a Claude Code plugin marketplace. It hosts skills distributed as plugins, installable via the `/plugin` command.

---

## Japanese Translation Files (`.jp.md`)

Every English document in this repo has a paired Japanese translation:

| English (auto-loaded) | Japanese (reference only) |
|-----------------------|--------------------------|
| `CLAUDE.md` | `CLAUDE.jp.md` |
| `plugins/*/skills/*/SKILL.md` | `plugins/*/skills/*/SKILL.jp.md` |

**These `.jp.md` files are never auto-loaded by Claude Code** — Claude Code only reads files named exactly `CLAUDE.md` or `SKILL.md`. The `.jp.md` variants are purely for human reference.

### Update workflow

The user reads `.jp.md` to understand the content and gives instructions in Japanese. When a change is needed:

1. **Update `.jp.md` first** — confirm the intended change is correctly reflected in Japanese
2. **Then update the English original** — apply the same change to the authoritative file

Both files must always be kept in sync. Never update one without updating the other.

---

## Repository Structure

```
my-plugins/
├── .claude-plugin/
│   └── marketplace.json       # Plugin catalog — the source of truth for what's published
├── plugins/
│   └── {plugin-name}/
│       ├── .claude-plugin/
│       │   └── plugin.json    # Plugin manifest (name, description, version)
│       └── skills/
│           └── {skill-name}/
│               ├── SKILL.md      # Skill definition (English, auto-loaded)
│               └── SKILL.jp.md   # Japanese translation (reference only)
├── CLAUDE.md      # This file (English, auto-loaded)
└── CLAUDE.jp.md   # Japanese translation (reference only)
```

---

## Skills Design Rules

All skills in this repo are **auto-trigger skills** — not interactive wizard-style. Follow these rules when writing SKILL.md:

- Write all content in **English**
- Put **all content inside SKILL.md** — no separate `references/` files. External references add read latency on every trigger.
- No interactive step menus, choice lists, or dialog prompts in the skill body
- The `description` frontmatter field drives auto-triggering. Make it explicit and slightly "pushy": list specific contexts and user phrases that should trigger the skill, even when the skill isn't explicitly requested
- Keep SKILL.md under 500 lines where possible

### SKILL.md frontmatter

```yaml
---
name: {skill-name}
description: {What the skill does and when to trigger it. Be specific about contexts.}
---
```

Optional frontmatter fields:

| Field | Description |
|-------|-------------|
| `disable-model-invocation` | `true` = manual invocation only (`/{plugin}:{skill}`) |
| `allowed-tools` | Tools available during skill execution (e.g., `Read, Grep, Bash`) |
| `context` | `fork` = run in a subagent |

---

## Current Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| `wiki` | 1.0.0 | Project documentation Wiki management with Issue-driven decision tracking |
| `py` | 1.0.0 | Python project coding standards and conventions |
| `wt` | 1.0.1 | Git worktree-based implementation workflow management |

---

## Prerequisite for All Plugin Work

Whether creating a new plugin or updating an existing one, **always use the `wt` skill to create a worktree and branch before starting work**.

Never work directly on the main branch.

```bash
# Invoke the wt skill before starting any plugin work
/wt:wt
```

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

### Checklist

When modifying a plugin, always update all three locations that reference its version:

- [ ] `plugins/{plugin-name}/.claude-plugin/plugin.json` — bump `version`
- [ ] `.claude-plugin/marketplace.json` — bump the matching plugin's `version`
- [ ] Commit with a message that reflects the change

### Version bump rules

| Change type | Version bump | Example |
|-------------|-------------|---------|
| Bug fix, minor correction | PATCH (`1.0.0` → `1.0.1`) | Fix a wrong command, typo in logic |
| New section, new capability | MINOR (`1.0.0` → `1.1.0`) | Add a new workflow section |
| Complete rewrite or breaking change | MAJOR (`1.0.0` → `2.0.0`) | Rethink the entire skill approach |

---

## Plugin Components Reference

A plugin can contain more than just skills:

```
plugins/{plugin-name}/
├── .claude-plugin/
│   └── plugin.json      # Required
├── skills/              # Auto-trigger or manual skills
│   └── {skill-name}/
│       └── SKILL.md
├── agents/              # Custom subagent definitions
│   └── {agent-name}.md
├── hooks/               # Hook configuration
│   └── hooks.json
├── .mcp.json            # MCP server config
├── .lsp.json            # LSP server config
└── settings.json        # Default settings
```

---

## Installing This Marketplace

### Add the marketplace

```bash
# Via URL
/plugin marketplace add https://github.com/shuhei1101/my-plugins.git

# Via local path (if cloned)
/plugin marketplace add ./my-plugins
```

### Install a plugin

```bash
/plugin install {plugin-name}@my-plugins
```

Scopes:
- **User** — active across all projects (`~/.claude/settings.json`)
- **Project** — shared with all collaborators (`.claude/settings.json`)
- **Local** — your machine only for this project (`.claude/settings.local.json`)

### Update / manage

```bash
/plugin marketplace update my-plugins     # fetch latest plugin list
/plugin disable {plugin-name}@my-plugins
/plugin enable {plugin-name}@my-plugins
/plugin uninstall {plugin-name}@my-plugins
```

### Auto-configure for a team

Add to the project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "my-plugins": {
      "source": {
        "source": "url",
        "url": "https://github.com/shuhei1101/my-plugins.git"
      }
    }
  },
  "enabledPlugins": {
    "{plugin-name}@my-plugins": true
  }
}
```

---

## Reference Links

| Topic | URL |
|-------|-----|
| Skills | https://code.claude.com/docs/ja/skills |
| Plugins | https://code.claude.com/docs/ja/plugins |
| Installing plugins | https://code.claude.com/docs/ja/discover-plugins |
| Marketplaces | https://code.claude.com/docs/ja/plugin-marketplaces |
| Plugin reference (schema) | https://code.claude.com/docs/ja/plugins-reference |
| Subagents | https://code.claude.com/docs/ja/sub-agents |
| Hooks | https://code.claude.com/docs/ja/hooks |
| MCP servers | https://code.claude.com/docs/ja/mcp |
