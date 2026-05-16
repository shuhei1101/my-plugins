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
  - **Exception: `rules/` subfolder** — a skill may include a `rules/` directory alongside `SKILL.md` for rule-file templates that get deployed into projects on initialization. These are not read during normal skill execution. `SKILL.md` must embed the template content inline; `rules/` is the human-readable source of truth.
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
| `docs-manage` | 1.2.0 | Project documentation management with Issue-driven decision tracking |
| `py` | 1.1.0 | Python project coding standards and conventions |
| `wt` | 1.1.0 | Git worktree-based implementation workflow management |
| `claude-kit` | 3.2.0 | Toolkit for authoring Claude Code instruction files — CLAUDE.md, path-scoped rules, and skills |
| `yaml-rule` | 1.0.0 | YAML file management conventions for assets and project configuration — index.yaml, settings.yaml, and developer note standards |
| `work-kit` | 2.0.0 | Hook-based project lifecycle management — injects PR task context on every prompt and reminds task updates on stop |

---

## Plugin Work Rules

Plugin creation and update procedures (worktree setup, step-by-step creation guide, version bump rules) are in `.claude/rules/plugin-work.md`. That rule file auto-loads whenever Claude edits files under `plugins/` or `.claude-plugin/`.

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
