---
name: plugin-migrate
description: |
  Bring files created by the utils plugin up to the current conventions.
  Trigger when the user says "utils を更新して" or invokes "utils:plugin-migrate" explicitly.
---

# utils:plugin-migrate — Plugin Migration

Apply convention changes introduced by newer versions of the utils plugin to existing files.

---

## Tasks

### Step 1: Pre-conditions

#### Process

1. Confirm the current branch is not `master` / `main`
   - If on `master` / `main`, stop and ask the user to create a working branch first

→ Proceed to Step 2

---

### Step 2: Check installed version

#### Process

1. Read `plugins/utils/.claude-plugin/plugin.json` to get the installed version
2. Review which convention changes apply for that version range

→ Proceed to Step 3

---

### Step 3: Check and fix conventions

#### Process

No static templates exist as of v1.0.0. When future versions introduce convention changes,
add migration steps here.

Current checks:
- `agents/jp-mirror-translator.md` has `model: sonnet`
- `skills/jp-mirror-sync/SKILL.md` contains the subagent launch procedure

→ Proceed to Step 4

---

### Step 4: Report

#### Process

1. Report each item checked and any fixes applied
2. If changes were made, ask the user to commit them
