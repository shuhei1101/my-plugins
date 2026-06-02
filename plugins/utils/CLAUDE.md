# utils Plugin Developer Guide

General-purpose utility skills that don't belong to a more specific plugin.

---

## Layout

```
utils/
├── .claude-plugin/plugin.json
├── CLAUDE.md / CLAUDE.jp.md
├── agents/
│   ├── jp-mirror-translator.md       # Subagent definition (Sonnet, JP→EN direction only)
│   └── jp-mirror-translator.jp.md
└── skills/
    ├── jp-mirror-sync/
    │   ├── SKILL.md                  # User-facing interface (launches parallel subagents)
    │   └── SKILL.jp.md
    └── plugin-migrate/
        ├── SKILL.md
        └── SKILL.jp.md
```

---

## Skills

| Skill | Description |
|---|---|
| `utils:jp-mirror-sync` | Accept one or more `.jp.md` files and spawn one subagent per file in parallel to create or update the English counterparts |
| `utils:plugin-migrate` | Bring utils-created files up to current conventions |

## Agents

| Agent | Description |
|---|---|
| `utils:jp-mirror-translator` | Translate a single `.jp.md` file to its `.md` English counterpart. Creates the English file if absent; updates it if present (JP mirror is source of truth). Model: Sonnet |

---

## Environment Variables

None.

---

## Changelog

| Version | Date | Summary |
|---|---|---|
| 1.0.0 | 2026-06-02 | Initial release — `jp-mirror-sync` skill and `jp-mirror-translator` subagent |
