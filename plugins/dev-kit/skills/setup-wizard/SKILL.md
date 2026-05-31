---
name: setup-wizard
description: |
  Trigger on `SessionStart` (auto-loaded by hook when `setup_done` is unset) or when the
  user calls `/dev-kit:setup-wizard` explicitly. Walks through language opt-in and feature
  toggle configuration, then marks the plugin as set up.
  AskUserQuestion usage is explicitly permitted inside this skill.
---

# dev-kit:setup-wizard — Initial Onboarding

This skill drives the dev-kit plugin's first-run onboarding. Guides the user through
language opt-in configuration (Python / HTML / Next.js / Markdown) and introduces key
workflows, then marks setup as complete.

AskUserQuestion is used internally (explicitly permitted in this skill).

---

## Tasks

### Step 1: Check existing setup state

#### Condition

- Always — run first

#### Process

1. Read `.claude/dev-kit.local.md` (the YAML frontmatter)
2. If `setup_done: true` → use `AskUserQuestion` with options:
   - `Re-run setup` — continue to Step 2
   - `Abort` — stop here
3. If false or missing → continue to Step 2

→ Proceed to Step 2

---

### Step 2: Language / feature config — delegate to plugin-config

#### Condition

- Step 1 complete

#### Process

1. Use `AskUserQuestion` with a single question:

   **Question**: "Would you like to configure dev-kit language opt-ins now?"

   | Option | Action |
   |---|---|
   | Configure (launch `/dev-kit:plugin-config`) | Invoke `/dev-kit:plugin-config` to walk through every toggle |
   | Skip (configure later) | Skip; tell the user they can run `/dev-kit:plugin-config` later |

2. Execute the chosen action

→ Proceed to Step 3

---

### Step 3: Use-case showcase

#### Condition

- Step 2 complete

#### Process

1. Use `AskUserQuestion` (multiSelect: true) with the question:

   **Question**: "Which languages or frameworks will you use dev-kit with? (select all that apply)"

   | Option | Description |
   |---|---|
   | Python | Set `DEV_KIT_PYTHON=true`; injects Python conventions when editing `.py` files |
   | HTML / CSS / JS | Set `DEV_KIT_HTML=true`; injects FLOCSS design-token conventions for frontend work |
   | Next.js | Set `DEV_KIT_NEXT=true`; injects App Router conventions when editing `.ts`/`.tsx` files |
   | Markdown | Set `DEV_KIT_MARKDOWN=true`; injects Markdown formatting conventions when editing `.md` files |

2. For each selected option, summarize in 3–5 lines the conventions that will be injected
   and how to enable/disable them

→ Proceed to Step 4

---

### Step 4: Mark setup as done

#### Condition

- Step 3 complete

#### Process

1. Write (or update) `.claude/dev-kit.local.md` with `setup_done: true` in the YAML frontmatter:

   ```markdown
   ---
   setup_done: true
   ---

   # dev-kit setup notes

   (Add any personal notes here)
   ```

2. Tell the user:
   - Setup is complete
   - They can re-run setup any time via `/dev-kit:setup-wizard`
   - They can change language toggles at any time via `/dev-kit:plugin-config`
