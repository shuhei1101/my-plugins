---
name: plugin-migrate
description: |
  Inspect every plugin that has ref-inject applied (detected by the presence of
  hooks/scripts/inject_references.py) and update its injection mechanism files to match the
  current ref-inject templates. The references/ content (user-authored docs, _index.yaml,
  _injection_rules.yaml) is never touched — only the hook mechanism files are updated.
  Manual invocation only — use /ref-inject:plugin-migrate.
---

# ref-inject:plugin-migrate — Update Injection Mechanism in Consumer Plugins

Brings the injection hook files in **all ref-inject consumers** up to date with the current
ref-inject templates. Where `/ref-inject:apply` installs the mechanism for the first time,
`plugin-migrate` keeps it current across template changes.

The `references/` content (user-authored docs, `_index.yaml`, `_injection_rules.yaml`) is
**never modified** — only the mechanism files under `hooks/` are updated.

---

## What counts as a "consumer"

A plugin is a ref-inject consumer if it has `hooks/scripts/inject_references.py`.
This file is the canonical marker left by `/ref-inject:apply`.

---

## Mechanism files updated by this skill

| File | Action |
|---|---|
| `hooks/scripts/inject_references.py` | Overwrite with current template (placeholder-substituted) |
| `hooks/scripts/_common.py` | Overwrite with current template |
| `hooks/templates/injection.md.j2` | Overwrite with current template |
| `hooks/templates/injection.jp.md.j2` | Overwrite with current template |
| `hooks/hooks.json` | Merge the `PreToolUse(Edit\|Write\|MultiEdit\|Read)` entry; leave other hooks intact |

---

## Tasks

### Step 1: Enumerate consumer plugins

#### Condition

- Always — run first

#### Process

1. Run:
   ```bash
   find . -path '*/hooks/scripts/inject_references.py' \
     -not -path '*/ref-inject/templates/*' \
     -not -path '*/.git/*'
   ```
2. Each result lives at `{plugin_root}/hooks/scripts/inject_references.py`.
   Derive `{plugin_root}` (e.g. `plugins/claude-kit`) for each match.
3. If no consumers are found → report "No ref-inject consumers found." and stop.

→ Proceed to Step 2

#### Output

- List of consumer plugin roots confirmed (e.g. `plugins/claude-kit`, `plugins/dev-kit`)

---

### Step 2: Derive placeholder values for each consumer

#### Condition

- Step 1 complete

#### Process

For each consumer plugin root (`{plugin_root}`), derive the placeholder values from the
**directory name** (`{name}` = last path segment):

| Placeholder | Derivation | Example (`claude-kit`) |
|---|---|---|
| `__PLUGIN_NAME__` | `name` | `claude-kit` |
| `__ENV_PREFIX__` | `name` upper-cased, every run of non-alphanumeric → `_` | `CLAUDE_KIT` |
| `__LOG_TAG__` | `{name}-references-injection` | `claude-kit-references-injection` |
| `__DEFAULT_TTL__` | Read from first `TTL` line in the consumer's existing `.py`; fall back to `3600` | `3600` |

→ Proceed to Step 3

#### Output

- Placeholder map for each consumer confirmed

---

### Step 3: Compare mechanism files and report

#### Condition

- Step 2 complete

#### Process

For each consumer plugin:

1. Read the four template files from `${CLAUDE_PLUGIN_ROOT}/templates/hooks/`:
   - `scripts/inject_references.py`
   - `scripts/_common.py`
   - `templates/injection.md.j2`
   - `templates/injection.jp.md.j2`

2. For `inject_references.py`, substitute all four placeholders with the consumer's derived values.
   The other three files have no placeholders — compare verbatim.

3. Read the consumer's current versions of the same four files.

4. Compare. For each file that differs, note it as **needs update**.

5. For `hooks.json`: read both the template's `hooks.json` and the consumer's `hooks.json`.
   Check whether the consumer's `PreToolUse(Edit|Write|MultiEdit|Read)` entry
   matches the template's entry. Note as **needs merge** if it differs.

6. Summarize the findings per consumer:
   - **Up to date**: no differences
   - **Needs update**: list each file that differs

→ Proceed to Step 4

#### Output

- Per-consumer diff summary displayed to the user

---

### Step 4: Apply updates (with user confirmation)

#### Condition

- Step 3 complete
- At least one consumer has files that need updating

#### Process

1. Show the per-consumer summary from Step 4.
2. Ask the user: "Update mechanism files in all consumers? (yes / list specific plugins to skip)"
3. For each consumer the user approves:

   a. **Overwrite** the four hook scripts and templates (placeholder-substituted where applicable).

   b. **Merge `hooks.json`**: do not overwrite the whole file — find the
      `PreToolUse(Edit|Write|MultiEdit|Read)` entry and replace it with the template's entry.
      All other entries in the consumer's `hooks.json` remain unchanged.

4. After writing each consumer, grep `{plugin_root}/hooks/` for any remaining
   `__PLACEHOLDER__` tokens and report if any are found.

→ Proceed to Step 5

#### Notes

##### Prohibitions

- Never overwrite `references/` content (docs, `_index.yaml`, `_injection_rules.yaml`, `CLAUDE.md`)
- Never replace the whole `hooks.json` — always merge the PreToolUse entry in-place

---

### Step 5: Report completion

#### Condition

- Step 4 complete

#### Process

1. List every file updated per consumer.
2. Show `git diff` (truncate if large).
3. If no files changed for a consumer, report "Already up to date".
4. Suggest a commit message:
   - `chore: sync ref-inject injection hook to v{N}`
   - Read `{N}` from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`
5. **This skill never commits** — committing is the user's responsibility.

→ Done

#### Notes

##### Prohibitions

- Auto-committing
