---
name: pr-show
description: Present next PR candidates in 3 categories (ready to start / in progress elsewhere / has conditions).
---

# workspace:pr-show — Show Next PR Candidates

Reads a PR document's `## 次PR候補` table and classifies each candidate as ready to start, in progress elsewhere, or has conditions.

---

## Overview

A standalone skill extracted from merge Step 12. Can be called at any time to check which PRs are next — not only after a merge.

**Data source**: the `## 次PR候補` table in the specified PR document.
Never lists all git branches blindly — only candidates explicitly listed in the table are shown.

---

## Tasks

### Step 1: Locate the data source

#### Condition

- Always — run first

#### Process

1. If called with a PR document path argument (e.g. from merge Step 12), use that file directly
2. If called standalone (no argument):
   - Find all PR documents under `.work/tasks/`:
     ```bash
     find .work/tasks -type f -name "PR*.md"
     ```
   - If only one active PR exists, use its document automatically
   - If multiple exist, ask the user which PR to check

→ Proceed to Step 2

#### Output

- PR document path confirmed

---

### Step 2: Read the `## 次PR候補` table

#### Condition

- Step 1 complete

#### Process

1. Read the `## 次PR候補` section from the PR document
2. If the table contains only a placeholder row (e.g., `{次にやること}` or a lone `-`)
   → output "No next PR candidates." and finish

→ Proceed to Step 3

#### Output

- List of candidate rows (title, summary, 実施条件)

---

### Step 3: Classify each candidate

#### Condition

- Step 2 complete (table has real rows)

#### Process

For each candidate row:

**a. Has conditions (条件あり)**:
- Column 3 (実施条件) references another candidate — e.g. `「{other}」が完了したら`
- pr-handoff intentionally did not reserve a branch for these
- List directly from the table — no branch lookup needed

**b. Ready to start or In progress elsewhere**:
- Column 3 is blank or `即時実施可` — pr-handoff should have reserved a branch
- Find the branch by searching for the candidate title:
  ```bash
  git branch --list "*{candidate-title}*"
  ```
- Count commits ahead of master:
  ```bash
  git log master..{branch} --oneline | wc -l
  ```
- commits ≤ 1 → **Ready to start**
- commits ≥ 2 → **In progress elsewhere**
- Branch not found → pr-handoff was not run; note as "未予約 (pr-handoff not run)"

→ Proceed to Step 4

#### Output

- Each candidate classified into one of the 3 categories

---

### Step 4: Present the table

#### Condition

- Step 3 complete

#### Process

1. Output the table in this format:

   ```markdown
   ## Next PRs you can pick up

   | Category | PR | Summary |
   |---|---|---|
   | Ready to start | PR{N} | {title} (branch: {branch}) |
   |  | PR{M} | {title} (branch: {branch}) |
   | In progress elsewhere | PR{N} | {title} ({commit_count} commits ahead) |
   | Has conditions | — | {title} — condition: depends on `{other-candidate}` being completed |
   ```

   - When multiple PRs share the same category, write the category name only in the first row; leave subsequent cells empty
   - Omit rows for categories with zero items
   - If all categories are empty (placeholder table only), show: "No next PR candidates."

→ Done

#### Output

- Status report table presented to the user

---

## References

### Data source rule

Use only the specified PR document's `## 次PR候補` table — never `git branch --list 'PR*'`.
Unrelated reserved branches from other sessions are intentionally excluded.

### Classification knowledge

| Category | Detail |
|---|---|
| **Ready to start** | State immediately after pr-handoff reservation. Branch has just the PR-document creation commit (1 commit) ahead of master. |
| **In progress elsewhere** | Another Claude Code session has implementation commits on this branch. Two or more commits means the user is actively working there. |
| **Has conditions** | A candidate that pr-handoff classified as a serial-dependency item and chose not to reserve. It becomes eligible once its predecessor PR merges. |

### Why keep "in progress" visible

Hiding them entirely would create the impression "nothing is left." Surfacing them prevents the user from losing track of overall state.

### Why surface "has conditions"

They do not appear as reserved branches, but they live in the PR document's `## 次PR候補` as "next-next" items. Listing them alongside ready-to-start ensures the user does not overlook them.
