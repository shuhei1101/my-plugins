---
name: issue-save
description: |
  Shared sub-skill that saves one issue into `.work/issues/`.
  Reads `_index.yaml`, increments `last_id`, creates `ISSUE-{N}.md`, and updates the index.
  Called by issue-scan and issue-create — not intended for direct user invocation.
disable-model-invocation: true
---

# work:issue-save — Save One Issue

A shared sub-skill that saves one issue to `.work/issues/`.
Called by `issue-scan` and `issue-create` with the issue information to record.

---

## Overview

**Information received from the caller**:
- Title (required): one-sentence summary of the issue
- Type (required): one of `refactor` / `rule-violation` / `ui` / `backend` — recorded in `_index.yaml` only
- Priority (required): one of `high` / `medium` / `low` — recorded in `_index.yaml` only
- Tags (optional): list of relevant keywords — recorded in `_index.yaml` only
- Scan scope (optional): which file or layer was scanned (provided by issue-scan) — recorded in `_index.yaml` only
- Problem description (required): explanation of what the problem is
- Horizontal expansion (optional): notes on whether the same problem exists elsewhere in the codebase (provided by issue-scan)
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
   # {ISSUE-N}: {タイトル}

   **作成日**: {YYYY-MM-DD}

   ## 問題

   {問題の説明}

   ## 水平展開

   {水平展開メモ}   ← 提供されなかった場合はこのセクション自体を省略

   ## 修正案

   {修正案}   ← 提供されなかった場合はこのセクション自体を省略

   ## ユーザーの言葉

   {ユーザーの言葉}   ← 提供されなかった場合はこのセクション自体を省略
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
