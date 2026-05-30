# setup-wizard Skill Authoring Guide

Design guide for the **mandatory** `setup-wizard` skill required when creating any new plugin.
Provides the initial-onboarding flow and use-case entry points the first time a user touches the plugin.
Japanese mirror: `references/setup-wizard.jp.md`

Counterpart to `plugin-update` (version sync) — `setup-wizard` covers initial setup.
Read `common.md` and `skills.md` alongside this guide.

---

## Why mandatory

- Each plugin's env toggles and initial settings are scattered across `CLAUDE.md`; users won't discover them by reading on their own
- Without a first-run flow, the plugin's features go unused — there's no "first step" handed to the user
- Keeping the setup-complete flag **per plugin** avoids cross-plugin coupling; each plugin owns its own state

---

## Standard contract

| Item | Convention |
|---|---|
| Name | `setup-wizard` (kebab-case literal — not `<plugin>-setup-wizard`) |
| Trigger | Manual (`/<plugin>:setup-wizard`) + SessionStart hook auto-prompt (only when the flag is unset) |
| First action | Read `setup_done` from `.claude/{plugin}.local.md`; if already true, ask whether to re-run or abort |
| Scope | Only this plugin's own env / onboarding; never touch other plugins' state |
| Completion mark | Write `setup_done: true` into the YAML frontmatter of `.claude/{plugin}.local.md` |

### Relationship to plugin-config

`setup-wizard` delegates env configuration to **its own plugin's `plugin-config` skill**.
When the plugin has env toggles, implementing `plugin-config` is also mandatory (see "Related required skills" below).

---

## SessionStart hook layout

Each plugin ships its own SessionStart hook. The hook reads `setup_done`; if false or unset,
it injects a prompt telling Claude to launch `/<plugin>:setup-wizard`.

### hooks.json example

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/setup_check.py"
          }
        ]
      }
    ]
  }
}
```

### Script requirements

- Read `.claude/{plugin}.local.md` and check the `setup_done` field in the YAML frontmatter
- Truthy → exit silently with status 0
- Falsy / missing → write a JSON payload to stdout with `decision: block` and a `reason` that asks Claude to invoke `/<plugin>:setup-wizard` to complete setup

---

## Flag schema

Stored in `.claude/{plugin-name}.local.md` (reusing the existing `plugin-settings` mechanism):

```markdown
---
setup_done: true
---

# {plugin-name} setup notes

(free user notes)
```

**No version field is stored.** Version drift is handled by convention, not by the flag:
when a plugin is updated, its `setup-wizard` must be refreshed in the same change.
This convention is stated in this reference; add the same item to the plugin's `plugin-update` checklist.

---

## Standard setup-wizard flow

Each step uses `AskUserQuestion`. **`AskUserQuestion` allows 2–4 options per question**
(official schema cap; an "Other" choice is appended automatically).

### Step 1 — Detect existing setup

Read `.claude/{plugin}.local.md`:

- `setup_done: true` → ask "Re-run setup? ([re-run] / [abort])" and branch on the answer
- false / missing → continue

### Step 2 — env / initial config

Present options via `AskUserQuestion`:

| Label | Action |
|---|---|
| Configure all | Launch this plugin's `plugin-config` skill to walk through every env |
| Essentials only | Configure only env keys the plugin marks as required |
| Skip | Skip env setup; tell the user they can run `/<plugin>:plugin-config` later |

### Step 3 — Use-case showcase

`AskUserQuestion` with 2–4 use-case options. Summarize each selected use case in 3–5 lines and link
to the corresponding section of the plugin's `CLAUDE.md`.

> **Be a table of contents, not a manual.** Write the detailed usage in `CLAUDE.md`; have
> `setup-wizard` point at it. Don't duplicate long-form usage docs inside the wizard.

### Step 4 — Mark setup complete

Write `setup_done: true` into the YAML frontmatter of `.claude/{plugin}.local.md`, and tell the
user they can re-run setup any time via `/<plugin>:setup-wizard`.

---

## Related required skills

`setup-wizard` does not stand alone. For plugins with env toggles, also implement:

| Skill | Role |
|---|---|
| `plugin-config` | Single-purpose skill that edits env vars one-by-one via `AskUserQuestion`. Delegated to from `setup-wizard` |
| `plugin-update` | Version sync. See the "Required skills" section in this reference |

If the plugin has no env vars, `plugin-config` is not required, but the use-case showcase step in
`setup-wizard` is still valuable — `setup-wizard` itself remains mandatory.

---

## Skeleton (copy & adapt)

```markdown
---
name: setup-wizard
description: |
  Trigger on `SessionStart` (auto-loaded by hook when `setup_done` is unset) or when the
  user calls `/<plugin>:setup-wizard` explicitly. Walks through env config and use-case
  introduction, then marks the plugin as set up.
---

# <plugin>:setup-wizard — Initial Onboarding

This skill drives <plugin>'s first-run onboarding. AskUserQuestion is used internally
(its usage is explicitly permitted inside this skill).

## Tasks

### Step 1: Check existing setup state
{Read `.claude/<plugin>.local.md` and branch on `setup_done`.}

### Step 2: env config (delegate to plugin-config)
{Use AskUserQuestion to present "configure all / essentials only / skip"; on selection,
invoke `plugin-config`.}

### Step 3: Use-case showcase
{Use AskUserQuestion to present 2–4 use cases; summarize the chosen one and link to CLAUDE.md.}

### Step 4: Mark setup as done
{Write `setup_done: true` into the frontmatter of `.claude/<plugin>.local.md`.}
```

Create the JP mirror `SKILL.jp.md` simultaneously (see `common.md` JP/EN mirror rules).

---

## Checklist

- [ ] Created `skills/setup-wizard/SKILL.md` and `SKILL.jp.md`
- [ ] Added a `SessionStart` entry to `hooks/hooks.json` and implemented `hooks/scripts/setup_check.py`
- [ ] If the plugin has env vars, also implemented `skills/plugin-config/SKILL.md` (+ `.jp.md`)
- [ ] Added a one-liner to the plugin's `CLAUDE.md` pointing at the first-run setup flow
- [ ] Bumped the version and noted "added setup-wizard" in the changelog
