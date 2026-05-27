---
name: refs-inject-kit:add-plugin
description: >
  Register a reference-bearing plugin (e.g. py-kit, next-kit) with refs-inject-kit
  by adding it to the central `injection_rules.yaml`. Lists the plugin's available
  references from its `references/index.yaml` and assists the user in writing rules.
  Trigger when the user says "refs-inject-kit にプラグイン追加", "add-plugin", or
  "{plugin-name} を refs-inject-kit に登録".
---

# refs-inject-kit:add-plugin — register a plugin

Add a reference-bearing plugin (`py-kit`, `next-kit`, …) to refs-inject-kit's central `injection_rules.yaml`.

The scope is **deliberately small**: this skill helps you list a plugin's references and append a stub entry to `enabled_plugins`. Writing concrete rules is done manually by the user (or with AI help in the same chat) — this skill does not auto-generate rules.

---

## Tasks

### Step 1: Resolve the plugin

#### Condition

- Always — first thing

#### Process

1. Take the plugin name from `$ARGUMENTS` (e.g. `py-kit`). If missing, ask the user.
2. Resolve the plugin's `references/` directory in this order:
   1. `${CLAUDE_PROJECT_DIR}/plugins/{plugin}/references/` (marketplace development)
   2. `${HOME}/.claude/plugins/cache/*/{plugin}/*/references/` (installed)
3. If neither exists, report the failure and stop.

→ Proceed to Step 2

---

### Step 2: List the plugin's available references

#### Condition

- Step 1 complete

#### Process

1. Read the resolved `references/index.yaml`.
2. Print a numbered list of `references[].path` with their `description` so the user can see what's available.

→ Proceed to Step 3

---

### Step 3: Update `injection_rules.yaml`

#### Condition

- Step 2 complete

#### Process

1. Read `${refs-inject-kit-root}/injection_rules.yaml`.
2. Add the plugin name to `enabled_plugins:` if not already present.
3. Append a stub commented section at the end of `rules:`:

   ```yaml
     # ========== {plugin-name} ==========
     # Add path-pattern → reference rules here.
     # Example:
     #   - pattern: "**/*.py"
     #     required:
     #       - "${{plugin-name}}/core/naming.md"
   ```

4. Save the file.
5. Print: "Added `{plugin-name}` to enabled_plugins and inserted a stub section. Edit `injection_rules.yaml` to add concrete rules — reference paths use the `${{plugin-name}}/sub/path.md` format."

→ Done

---

## Notes

### Prohibitions

- **Do not auto-generate rules.** Rules require human judgement about which references apply to which patterns. The user (or AI in a follow-up turn) writes them by hand.
- Do not overwrite existing rules for the same plugin — append only.

### See also

- `${refs-inject-kit-root}/CLAUDE.md` — overall plugin guide
- `${refs-inject-kit-root}/injection_rules.yaml` — the file this skill edits
