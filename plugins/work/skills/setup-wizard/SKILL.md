---
name: setup-wizard
description: |
  Trigger on `SessionStart` (auto-loaded by hook when `setup_done` is unset) or when the
  user calls `/work:setup-wizard` explicitly. Walks through env config and use-case
  introduction for the work plugin, then marks the plugin as set up.
  AskUserQuestion usage is explicitly permitted inside this skill.
---

# work:setup-wizard — Initial Onboarding

This skill drives the work plugin's first-run onboarding. Guides the user through
env toggle configuration and introduces key workflows, then marks setup as complete.

AskUserQuestion is used internally (explicitly permitted in this skill).

---

## Tasks

### Step 1: Check existing setup state

#### Condition

- Always — run first

#### Process

1. Read `.claude/work.local.md` (the YAML frontmatter)
2. If `setup_done: true` → use `AskUserQuestion` with options:
   - `Re-run setup` — continue to Step 2
   - `Abort` — stop here
3. If false or missing → continue to Step 2

→ Proceed to Step 2

---

### Step 2: Env config — delegate to plugin-config

#### Condition

- Step 1 complete

#### Process

1. Use `AskUserQuestion` with a single question:

   **Question**: "Would you like to configure work plugin env settings now?"

   | Option | Action |
   |---|---|
   | Configure all (launch `/work:plugin-config`) | Invoke `/work:plugin-config` to walk through every toggle |
   | Skip (configure later) | Skip; tell the user they can run `/work:plugin-config` later |

2. Execute the chosen action

→ Proceed to Step 3

---

### Step 3: Use-case showcase

#### Condition

- Step 2 complete

#### Process

1. Use `AskUserQuestion` (multiSelect: true) with the question:

   **Question**: "How do you plan to use the work plugin? (select all that apply)"

   | Option | Description |
   |---|---|
   | Branch & task management | Use `/work:start` to create branches; manage tasks under `.work/tasks/` |
   | Merge workflow | Use `/work:merge` for review, QA, and merging in a single guided flow |
   | Issue tracking | Use `/work:issue-scan` to auto-detect code issues and store them in `.work/issues/` |
   | Workspace config | Configure `WORK_*` env toggles via `/work:plugin-config` |

2. For each selected option, summarize in 3–5 lines and link to the relevant skill documentation

→ Proceed to Step 4

---

### Step 4: Mark setup as done

#### Condition

- Step 3 complete

#### Process

1. Write (or update) `.claude/work.local.md` with `setup_done: true` in the YAML frontmatter:

   ```markdown
   ---
   setup_done: true
   ---

   # work setup notes

   (Add any personal notes here)
   ```

2. Tell the user:
   - Setup is complete
   - They can re-run setup any time via `/work:setup-wizard`
   - They can change env toggles at any time via `/work:plugin-config`
