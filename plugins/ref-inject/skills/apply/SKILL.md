---
name: apply
description: |
  Apply (attach) the ref-inject reference auto-injection mechanism to a target plugin — new or existing. Copies the injection hook (inject_references.py + hooks.json), the Jinja2 templates, and a references/ skeleton into the plugin, substituting per-plugin placeholders. Does not own plugin-level concerns (plugin.json, the plugin's own CLAUDE.md, marketplace.json) — only the injection part.
  Trigger when the user says "このプラグインに ref-inject を付けて", "リファレンス注入を追加して", "apply ref-inject to {plugin}", "add reference injection to a plugin", or invokes /ref-inject:apply explicitly.
---

# ref-inject:apply — Attach the reference-injection mechanism to a plugin

Adds the `ref-inject` reference auto-injection mechanism to a **target plugin**. The plugin
may already exist (with its own `plugin.json` / `CLAUDE.md`) or be freshly scaffolded by
`plugin-creator` — this skill only contributes the **injection part**. **Claude reads each
template and writes the destination file itself**, substituting placeholders, so the structure
stays in context.

The injected mechanism: a `PreToolUse(Edit | Write | MultiEdit | Read)` hook matches the edited
file path against `references/_injection_rules.yaml` and injects matched references —
`required` → **full body**, `optional` → **path + description only** — de-duped by a two-tier
TTL token (per-pattern + per-reference; a reference already injected this session is shown by path
only, re-injected once the TTL elapses).

---

## Overview

This skill is **scoped to the injection machinery only**. It is *not* a plugin generator:

- It does **not** create or edit the plugin's `plugin.json`
- It does **not** create or own the plugin's root `CLAUDE.md`
- It does **not** touch `marketplace.json`

Those are plugin-level concerns owned by `plugin-creator`. Here the target plugin already exists
(or is created first by `plugin-creator`); this skill just attaches the ref-inject files if the
plugin does not have them yet.

---

## Tasks

### Step 1: Identify the target plugin and derive values

#### Condition

- Always — run first

#### Process

1. Confirm the **target plugin** path (e.g. `plugins/vue-kit`). The directory must already exist.
2. Determine the **TTL** (default re-injection interval in seconds, default `3600`).
3. Derive the placeholder values from the plugin's directory name (`{name}`):

| Placeholder | Value | Example (`vue-kit`) |
|---|---|---|
| `__PLUGIN_NAME__` | `name` | `vue-kit` |
| `__ENV_PREFIX__` | `name` upper-cased, every run of non-alphanumeric → `_` | `VUE_KIT` |
| `__LOG_TAG__` | `{name}-references-injection` | `vue-kit-references-injection` |
| `__DEFAULT_TTL__` | `ttl` (number) | `3600` |

(There is no `__PLUGIN_DESCRIPTION__` here — descriptions are plugin-level.)

→ Proceed to Step 2

#### Output

- Target plugin path and derived placeholder values confirmed

---

### Step 2: Copy the injection files, substituting placeholders

#### Condition

- Step 1 complete

#### Process

For **every** file under `${CLAUDE_PLUGIN_ROOT}/templates/`, `Read` it and `Write` it to the
matching path under the target plugin, replacing all placeholders with the derived values.
Substitute placeholders in text files; copy binaries verbatim.

| Template (under `templates/`) | Destination (under the target plugin) |
|---|---|
| `hooks/scripts/inject_references.py` | `hooks/scripts/inject_references.py` |
| `hooks/scripts/references_edit_guard.py` | `hooks/scripts/references_edit_guard.py` |
| `hooks/scripts/_common.py` | `hooks/scripts/_common.py` |
| `hooks/prompts/references-edit-guard.md` / `.jp.md` | `hooks/prompts/…` (same names) |
| `hooks/hooks.json` | `hooks/hooks.json` |
| `hooks/templates/injection.md.j2` / `injection.jp.md.j2` | `hooks/templates/…` (same names) |
| `references/_index.yaml` / `_index.jp.yaml` | `references/…` (same names) |
| `references/_injection_rules.yaml` | `references/_injection_rules.yaml` |
| `references/CLAUDE.md` / `CLAUDE.jp.md` | `references/…` (same names) |
| `references/example/getting-started.md` | `references/example/getting-started.md` |

Notes:
- Paths mirror the template — no relocation.
- Leave `${CLAUDE_PLUGIN_ROOT}` in `hooks.json` literal — Claude Code expands it at runtime.
- **If the target already has `hooks/hooks.json`** (other hooks present): do not overwrite it — merge the `PreToolUse` (Edit/Write/MultiEdit/Read) **and `PostToolUse` (Edit/Write/MultiEdit)** entries into the existing file instead.
- **If the target already has the injection files** (a re-apply / mechanism update): overwrite `hooks/*` but leave existing `references/` content (_index.yaml / _injection_rules.yaml / real docs) untouched — only add the skeleton files that are missing.
- After writing, confirm no `__PLACEHOLDER__` token remains (grep the target plugin's `hooks/`).

→ Proceed to Step 3

#### Output

- The target plugin has the injection hook, templates, and references skeleton

---

### Step 3: Report and hand off

#### Condition

- Step 2 complete

#### Process

1. Report which files were written to the target plugin.
2. Tell the user the remaining steps (all plugin-owned, outside this skill):
   - Fill `references/` with real docs (1 reference = 1 use case); replace `references/example/`
   - List each doc's path + description in `references/_index.yaml` (+ `_index.jp.yaml`)
   - Bind edit-path patterns in `references/_injection_rules.yaml`
   - Optionally set `{ENV_PREFIX}_INJECTION_TTL` in `settings.json` `env`
   - If this is a brand-new plugin, ensure `plugin.json` and `marketplace.json` exist (via `plugin-creator`), and mention the injection hook in the plugin's `CLAUDE.md`
3. Do **not** hand-edit the mechanism per plugin — change the `ref-inject` templates and re-apply.

#### Notes

- The hook needs `PyYAML` and `Jinja2` in the project where the target plugin runs.
