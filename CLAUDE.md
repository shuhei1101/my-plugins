# CLAUDE.md — my-plugins Developer Guide

This repository is a Claude Code plugin marketplace. It hosts skills distributed as plugins, installable via the `/plugin` command.

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
│       ├── references/        # Optional: shared reference docs read by skills
│       │   ├── {topic}.md        # Reference content (English, loaded on demand)
│       │   └── {topic}.jp.md     # Japanese translation (reference only)
│       └── skills/
│           └── {skill-name}/
│               ├── SKILL.md      # Skill definition (English, auto-loaded)
│               └── SKILL.jp.md   # Japanese translation (reference only)
├── CLAUDE.md      # This file (English, auto-loaded)
└── CLAUDE.jp.md   # Japanese translation (reference only)
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
