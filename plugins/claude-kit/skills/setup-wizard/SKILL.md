---
name: setup-wizard
description: |
  Trigger on `SessionStart` (auto-loaded by hook when `setup_done` is unset) or when the
  user calls `/claude-kit:setup-wizard` explicitly. Walks through env config (JP mirror,
  injection language) and use-case introduction, then marks the plugin as set up.
  AskUserQuestion usage is explicitly permitted inside this skill.
---

# claude-kit:setup-wizard — Initial Onboarding

This skill drives the claude-kit plugin's first-run onboarding. Guides the user through
env configuration (JP mirror creation, injection language) and introduces key workflows,
then marks setup as complete.

AskUserQuestion is used internally (explicitly permitted in this skill).

---

## Tasks

### Step 1: Check existing setup state

#### Condition

- Always — run first

#### Process

1. Read `.claude/claude-kit.local.md` (the YAML frontmatter)
2. If `setup_done: true` → use `AskUserQuestion` with options:
   - `Re-run setup` — continue to Step 2
   - `Abort` — stop here
3. If false or missing → continue to Step 2

→ Proceed to Step 2

---

### Step 2: Env config — delegate to config skill

#### Condition

- Step 1 complete

#### Process

1. Use `AskUserQuestion` with a single question:

   **Question**: "Would you like to configure claude-kit env settings now? (JP mirror, injection language, etc.)"

   | Option | Action |
   |---|---|
   | Configure (launch `/claude-kit:config`) | Invoke `/claude-kit:config` to walk through every variable |
   | Skip (configure later) | Skip; tell the user they can run `/claude-kit:config` later |

2. Execute the chosen action

→ Proceed to Step 3

---

### Step 3: Use-case showcase

#### Condition

- Step 2 complete

#### Process

1. Use `AskUserQuestion` (multiSelect: true) with the question:

   **Question**: "How do you plan to use claude-kit? (select all that apply)"

   | Option | Description |
   |---|---|
   | Skill & rule authoring | Use `/claude-kit:skill-creator` and `/claude-kit:rule-creator` to author skills and rules |
   | Hook creation | Use `/claude-kit:hook-creator` to create prompt-injection hooks |
   | Plugin creation | Use `/claude-kit:plugin-creator` to scaffold new plugins |
   | Env config management | Use `/claude-kit:config` to manage JP mirror, injection language, and other settings |

2. For each selected option, summarize in 3–5 lines and link to the relevant skill documentation

→ Proceed to Step 4

---

### Step 4: Mark setup as done

#### Condition

- Step 3 complete

#### Process

1. Write (or update) `.claude/claude-kit.local.md` with `setup_done: true` in the YAML frontmatter:

   ```markdown
   ---
   setup_done: true
   ---

   # claude-kit setup notes

   (Add any personal notes here)
   ```

2. Tell the user:
   - Setup is complete
   - They can re-run setup any time via `/claude-kit:setup-wizard`
   - They can change env settings at any time via `/claude-kit:config`
