---
name: issue-save
description: |
  Shared sub-skill that saves one issue into `.work/issues/`.
  Reads `_index.yaml`, increments `last_id`, creates `ISSUE-{N}.md`, and updates the index.
  Called by issue-scan and issue-create — not intended for direct user invocation.
disable-model-invocation: true
---

# work-kit:issue-save — Save One Issue

A shared sub-skill that saves one issue to `.work/issues/`.
Called by `issue-scan` and `issue-create` with the issue information to record.

---

## Overview

**Information received from the caller**:
- Title (required): one-sentence summary of the issue
- Type (required): one of `refactor` / `rule-violation` / `ui` / `backend`
- Priority (required): one of `high` / `medium` / `low`
- Tags (optional): list of relevant keywords
- Scan scope (optional): which file or layer was scanned (provided by issue-scan)
- Problem description (required): explanation of what the problem is
- User's words (optional): quote from the user's input (provided by issue-create)
- Suggested fix (optional): direction for a fix — omit if unknown

**Return value**: the created issue ID (e.g. `ISSUE-003`), returned to the caller

---

## Tasks

### Step 1: Confirm the received information

#### Condition

- Always — run first

#### Process

1. Confirm the issue information passed by the caller
2. Check that required fields are present (title, type, priority, problem description)
   - If any are missing, return an error to the caller and stop

→ Proceed to Step 2

#### Output

- Issue information confirmed and ready to save

---

### Step 2: Determine the next ID

#### Condition

- Always — run after Step 1

#### Process

1. Read `.work/issues/_index.yaml` (treat as `last_id: 0, issues: []` if missing)
2. Increment `last_id` by 1
3. Determine the issue ID: `ISSUE-{last_id:03d}` (zero-padded to 3 digits)

→ Proceed to Step 3

#### Output

- New `last_id` and issue ID

---

### Step 3: Create the issue file

#### Condition

- Always — run after Step 2

#### Process

1. Create `.work/issues/ISSUE-{N}.md` with this structure:

   ```markdown
   # {ISSUE-N}: {title}

   **Type**: {type}
   **Priority**: {priority}
   **Created**: {YYYY-MM-DD}
   **Tags**: [{tags}]
   **Scan scope**: {scope}   ← omit this line if no scope was provided

   ## Problem

   {problem description}

   ## User's words

   {user's words}   ← omit this section if not provided

   ## Suggested fix

   {suggested fix}   ← omit this section if not provided
   ```

→ Proceed to Step 4

#### Output

- `.work/issues/ISSUE-{N}.md` created

---

### Step 4: Update _index.yaml

#### Condition

- Always — run after Step 3

#### Process

1. Append the following entry to `_index.yaml`:
   ```yaml
   - id: ISSUE-{N}
     title: "{title}"
     created: {YYYY-MM-DD}
     type: {type}
     scan_scope:
       - "{scope}"   ← use scan_scope: [] if no scope was provided
     priority: {priority}
     tags: [{tags}]
   ```
2. Update `last_id` to the new value and write `_index.yaml`

→ Done

#### Output

- Return the created issue ID (e.g. `ISSUE-003`) to the caller
