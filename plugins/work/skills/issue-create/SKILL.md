---
name: issue-create
description: |
  Interpret a user's description of a problem and split it into discrete issue files under `.work/issues/`.
  Trigger when the user says "create an issue", "register this problem", "make issues for this",
  "イシューを作って", "問題を登録して", "issue-create", or invokes `/work:issue-create` explicitly.
---

# work:issue-create — Create Issues from User Description

Interprets a user's description of problems, splits it into discrete actionable issues, and writes
each as an issue file in `.work/issues/`. The issue file format, ID numbering, and index update are
governed by the `work-dir/イシュー.md` reference, which is auto-injected when you write a
`.work/issues/ISSUE-*.md` file — follow it directly; there is no separate save skill.

Example: "The chat history is hard to read, and settings reset on restart"
→ ISSUE-006: Improve chat history UI readability
→ ISSUE-007: Settings not persisted across restarts

---

## Overview

**Prerequisites**:
- `.work/issues/` must exist (run `/work:setup` if it doesn't)

**Splitting principle**:
- Problems that can be addressed independently → separate issues
- Multiple symptoms from the same root cause → one issue

---

## Tasks

### Step 1: Check current issue state

#### Condition

- Always — run first

#### Process

1. Check whether `.work/issues/` exists:
   - If not → report that setup must be run first (`/work:setup`), then stop
2. Read `_index.yaml` if it exists and note the current `last_id` (default 0 if missing)

→ Proceed to Step 2

#### Output

- Current `last_id`

---

### Step 2: Interpret and split the user's description

#### Condition

- Always — run after Step 1

#### Process

1. Read the user's input (from arguments or the prompt)
2. Split it into discrete problem units:
   - Independently fixable problems → separate issues
   - Same component or same root cause → merge into one issue
3. For each problem, determine title / type / priority / tags (see the injected `work-dir/イシュー.md`
   reference for the meaning of each field)
4. Present the split to the user for confirmation:
   - "I will split this into N issues. Does this look right?"
   - Show each issue: title, type, priority
5. If the user requests adjustments, revise before proceeding

→ Proceed to Step 3

#### Output

- Confirmed issue split (title, type, priority, tags for each)

---

### Step 3: Write the issue files

#### Condition

- Always — run after Step 2

#### Process

1. For each confirmed issue, allocate the next ID (`last_id + 1`, incrementing as you go) and write
   `.work/issues/ISSUE-{N}.md`.
   - Writing the file auto-injects the `work-dir/イシュー.md` reference — **follow its format exactly**.
   - The file **opens with the YAML frontmatter** defaulted for a fresh, unreviewed issue:
     `decision: pending`, `status: not_started`, `branches: []`. Do not set accept/reject here —
     the user does that later in `work:issue-review`.
   - The body is Japanese and follows the injected template sections (`## 概要` / `## 背景` /
     `## 現状` / `## 問題点` / `## 原因` / `## 期待される状態` / `## 修正案` etc.).
     Do not write Type/Priority/Tags lines (those live in `_index.yaml`).
   - **Raise QA when there are open questions** (e.g. which 修正案 to adopt, design choices the
     user must decide): add `## QA` with `QA-XXX` entries (状態: 未解決). These are answered later in
     `work:issue-review`. If there are no open questions, omit the `## QA` heading entirely.
2. After writing all files, update `_index.yaml` per the reference: append each issue's entry
   (`type` / `priority` / `tags` / `scan_scope` / `status: not_started` are recorded here) and set
   `last_id` to the highest ID used.
3. Collect the created ISSUE IDs.

→ Proceed to Step 4

#### Output

- List of created ISSUE IDs

---

### Step 4: Report results

#### Condition

- Always — run last

#### Process

1. Report the created issues (id, title, priority)
2. Mention that priority can be adjusted by editing the issue file or `_index.yaml`

#### Notes

- Do NOT run `git commit` in this skill — the user reviews before committing
- File format, numbering, and index rules all live in the `work-dir/イシュー.md` reference — do not
  duplicate them here; the reference is injected when you write the file
