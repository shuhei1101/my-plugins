# Environment Variables Guide

How to make a plugin's **executable code** configurable through environment variables. This applies
to **hooks and scripts** (`hooks/*.py`, `scripts/*.py`, inline `-c` hook commands) — the only plugin
parts that run as a process and can read `os.environ`. Markdown instruction files (`CLAUDE.md`, rules,
`SKILL.md`) are loaded into context, not executed, so they cannot read env vars — they only *document*
which env vars the plugin's code reads.
Japanese mirror: `references/environment.jp.md`

---

## Set — `settings.json` `env` block

Claude Code exports the key/value pairs in a `settings.json` `env` block into the environment of every
hook and tool subprocess. It is honored at three scopes; later scopes override earlier:

| Scope | File | Committed? |
|---|---|---|
| User | `~/.claude/settings.json` | n/a (personal) |
| Project (team) | `.claude/settings.json` | ✅ committed to git |
| Project (local) | `.claude/settings.local.json` | ❌ gitignored |

```json
{
  "env": {
    "MY_KIT_INJECTION_TTL": "7200",
    "MY_KIT_INJECTION_LANG": "jp"
  }
}
```

---

## Read — `os.environ` in the hook/script

Read with a sensible default and validate; never assume the var is set (the `env` block is optional):

```python
import os

raw = os.environ.get("MY_KIT_INJECTION_TTL")        # None if unset
ttl = int(raw) if raw and raw.isdigit() else 3600   # fall back to a default

lang = os.environ.get("MY_KIT_INJECTION_LANG", "en").lower()
```

> `env` values are plain strings — parse/validate (`int(...)`, `.lower()`, allow-list) in the reader.

---

## Worked example (this repo)

The `*-kit` reference-injection hooks (`hooks/scripts/inject_references.py` in dev-kit / claude-kit)
are tuned this way:

| Env var | Effect | Default |
|---|---|---|
| `{PREFIX}_INJECTION_TTL` | Seconds before a reference is re-injected | `3600` |
| `{PREFIX}_INJECTION_LANG` | `jp` → inject the Japanese descriptions/template | `en` |

`{PREFIX}` is the plugin name upper-cased with non-alphanumerics → `_` (e.g. `dev-kit` → `DEV_KIT`).

---

## Conventions

- **Namespace the key** with the plugin name (`{PREFIX}_...`) so plugins don't collide.
- **Always provide a default** in the reader — the env block is optional; the code must work without it.
- **Document each env var the plugin reads in the plugin's own `CLAUDE.md`** (name, effect, default), so
  users know what is configurable without reading the source.
- Do **not** put secrets in a committed `.claude/settings.json`; use `settings.local.json` (gitignored)
  for machine-specific or sensitive values.
- Markdown files (`CLAUDE.md` / rules / `SKILL.md`) cannot read env — if behavior must vary by env, the
  variation belongs in a hook or script, with the markdown only documenting it.

---

## Path variables vs env variables

Distinct mechanisms — don't confuse them:

| | Set where | Read where |
|---|---|---|
| **Env var** (`MY_KIT_*`) | `settings.json` `env` block | `os.environ` in hooks/scripts |
| **Path variable** (`${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PROJECT_DIR}`) | expanded by Claude Code in `hooks.json` / `settings.json` command args | not expanded in injected prompt text — see `hooks.md` |
