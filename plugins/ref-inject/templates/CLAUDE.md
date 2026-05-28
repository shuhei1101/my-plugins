# __PLUGIN_NAME__ Plugin Developer Guide

__PLUGIN_DESCRIPTION__

Generated from the `ref-inject` template. It ships a reference auto-injection hook
that, on every `Edit` / `Write` / `MultiEdit` / `Read`, matches the edited file path
against `references/injection_rules.yaml` and injects the relevant references.

---

## Structure

```
__PLUGIN_NAME__/
├── .claude-plugin/plugin.json
├── hooks/
│   ├── inject_references.py     # PreToolUse: matches path → injects references
│   ├── refresh_on_compact.py    # PreCompact: clears the session token → re-inject after /compact
│   ├── hooks.json
│   └── templates/injection.md.j2 (+ injection.jp.md.j2)
└── references/
    ├── index.yaml (+ index.jp.yaml)   # path + description (parsed by the hook)
    ├── injection_rules.yaml           # edit-path pattern → required / optional
    ├── CLAUDE.md (+ CLAUDE.jp.md)
    └── ...                            # your reference docs
```

---

## Injection behaviour

- `required` references are injected **in full body**; `optional` as **path + description only**
- A per-pattern TTL token (`~/.claude/tokens/__PLUGIN_NAME__/{session_id}.yaml`) prevents
  re-injecting the same pattern within `__ENV_PREFIX___INJECTION_TTL` seconds (default __DEFAULT_TTL__)
- `/compact` clears the token so references re-inject afterwards
- `__ENV_PREFIX___INJECTION_LANG=jp` switches descriptions/template to Japanese

Set the TTL in `settings.json`:

```jsonc
{ "env": { "__ENV_PREFIX___INJECTION_TTL": "3600" } }
```

---

## Maintenance

The hook/template/token structure is owned by `ref-inject`. To change the **mechanism**,
edit the `ref-inject` templates and regenerate via `/ref-inject:create`. Edit files here
directly only to add/adjust **references** (`references/` content + `index.yaml` + `injection_rules.yaml`).
