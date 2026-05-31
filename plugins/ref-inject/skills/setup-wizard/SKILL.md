---
name: setup-wizard
description: |
  Trigger on `SessionStart` (auto-loaded by hook when `setup_done` is unset) or when the
  user calls `/ref-inject:setup-wizard` explicitly. Introduces ref-inject use cases and
  marks the plugin as set up.
  AskUserQuestion usage is explicitly permitted inside this skill.
---

# ref-inject:setup-wizard — Initial Onboarding

This skill drives the ref-inject plugin's first-run onboarding. Introduces key use cases
and marks setup as complete.

ref-inject has no user-facing env toggles, so the env-config step is skipped.

AskUserQuestion is used internally (explicitly permitted in this skill).

---

## Tasks

### Step 1: Check existing setup state

#### Condition

- Always — run first

#### Process

1. Read `.claude/ref-inject.local.md` (the YAML frontmatter)
2. If `setup_done: true` → use `AskUserQuestion` with options:
   - `Re-run setup` — continue to Step 2
   - `Abort` — stop here
3. If false or missing → continue to Step 2

→ Proceed to Step 2

---

### Step 2: Use-case showcase

#### Condition

- Step 1 complete

#### Process

1. Use `AskUserQuestion` (multiSelect: true) with the question:

   **Question**: "How do you plan to use ref-inject? (select all that apply)"

   | Option | Description |
   |---|---|
   | Add injection to a new plugin | Use `/ref-inject:apply` to attach reference auto-injection to a new plugin |
   | Add injection to an existing plugin | Use `/ref-inject:apply` to retrofit reference auto-injection into an existing plugin |
   | Sync injection files | Use `/ref-inject:plugin-migrate` to update all consumers' injection files to the latest templates |

2. For each selected option, summarize in 3–5 lines and link to the relevant skill documentation

→ Proceed to Step 3

---

### Step 3: Mark setup as done

#### Condition

- Step 2 complete

#### Process

1. Write (or update) `.claude/ref-inject.local.md` with `setup_done: true` in the YAML frontmatter:

   ```markdown
   ---
   setup_done: true
   ---

   # ref-inject setup notes

   (Add any personal notes here)
   ```

2. Tell the user:
   - Setup is complete
   - They can re-run setup any time via `/ref-inject:setup-wizard`
