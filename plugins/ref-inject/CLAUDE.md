# ref-inject Plugin Developer Guide

`ref-inject` is a **generator** plugin. It scaffolds new reference auto-injection plugins
(the `*-kit` style used by `py-kit` / `next-kit`): a `PreToolUse` hook that matches the
edited file path against `injection_rules.yaml` and injects the relevant references.

It does **not** centralize a shared runtime (that approach was rejected — see
`premature-cross-plugin-centralization`). Instead it emits **independent copies** from
`templates/`, automating the copy-paste that the incident log blessed as the cheaper path.

---

## Structure

```
ref-inject/
├── .claude-plugin/plugin.json
├── CLAUDE.md / CLAUDE.jp.md
├── skills/create/SKILL.md (+ .jp.md)   # /ref-inject:create — gathers inputs, runs the generator
├── scripts/generate.py                  # copies templates + substitutes placeholders + registers marketplace
└── templates/                           # the seed files emitted into a new plugin
    ├── plugin.json                       # → {new}/.claude-plugin/plugin.json
    ├── CLAUDE.md (+ .jp.md)              # → {new}/CLAUDE.md
    ├── hooks/
    │   ├── inject_references.py          # PreToolUse: match path → inject references
    │   ├── refresh_on_compact.py         # PreCompact: clear session token → re-inject after /compact
    │   ├── hooks.json
    │   └── templates/injection.md.j2 (+ .jp.md.j2)
    └── references/
        ├── index.yaml (+ index.jp.yaml)
        ├── injection_rules.yaml
        ├── CLAUDE.md (+ CLAUDE.jp.md)
        └── example/getting-started.md
```

---

## Placeholders

`scripts/generate.py` substitutes these in every text template:

| Placeholder | Replaced with | Example |
|---|---|---|
| `__PLUGIN_NAME__` | plugin name (kebab) | `vue-kit` |
| `__ENV_PREFIX__` | name upper-cased, non-alnum → `_` | `VUE_KIT` |
| `__LOG_TAG__` | `{name}-references-injection` | `vue-kit-references-injection` |
| `__DEFAULT_TTL__` | default TTL seconds | `3600` |
| `__PLUGIN_DESCRIPTION__` | one-line description | … |

---

## Injection design (baked into the generated hook)

- `required` references → **full body** injected; `optional` → **path + description only**
- Token: `~/.claude/tokens/{plugin}/{session_id}.yaml`, a pattern-keyed YAML map; each entry has `injected_at` (epoch). Re-inject when `now - injected_at >= TTL`. Extensible (add fields later).
- TTL: default `3600`s, overridable via `settings.json` `env` → `{PREFIX}_INJECTION_TTL`
- Cleanup: every hook fire scans all `{session_id}.yaml`, drops expired entries, deletes emptied files
- `/compact`: `refresh_on_compact.py` deletes the session token so references re-inject
- Language: `{PREFIX}_INJECTION_LANG=jp` switches descriptions/template to Japanese

This replaces the old per-pattern empty-file token (PR150/151) and the pointer-only
injection (PR147) — `required` bodies are back because the TTL token throttles re-injection.

---

## Usage

`/ref-inject:create` (or "create a reference injection plugin"). Then fill `references/`
with real docs and bind them in `injection_rules.yaml`.

To change the **mechanism** for all generated plugins, edit `templates/` here and regenerate
each consumer with `/ref-inject:create --force` (overwrites references skeleton — use the
mechanism only on plugins whose references you can re-derive, or copy hooks/ manually).

---

## Related Plugins

| Plugin | Relationship |
|---|---|
| `py-kit` / `next-kit` | Reference-injection consumers; to be migrated onto ref-inject's generated form |
| `claude-kit` | Source of `plugin-creator` / creator skills and the common hook policy |
