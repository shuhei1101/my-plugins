---
name: work-start
description: |
  Start a new PR: create the task folder, PR folder, and TODO.md, update the relevant spec
  in .work/specs/, record unknowns in .work/QA.md, then create the worktree and branch.
  Trigger when the user says "新しい PR を作って", "新しい作業を始めたい", "work-start して",
  "start new work", or "create a new PR".
allowed-tools: Bash Read Write
---

# work-kit:work-start — Start a New PR

Creates the task/PR folder structure with TODO.md, maintains the spec and QA documents,
then sets up the worktree. Waits for user approval before implementation begins.

---

## Tasks

### Step 1: Determine the next PR number

#### Condition

- Always — run first

#### Process

1. Scan all `PR{N}/` folders under `.work/tasks/` to find the maximum N
2. Next PR number = max N + 1 (1 if no folders exist)

→ Proceed to Step 2

#### Output

- Next PR number confirmed

---

### Step 2: Collect request details

#### Condition

- Step 1 complete

#### Process

1. Ask the user for:
   - **Title**: short kebab-case label used in the folder name
   - **Type**: `feat` / `fix` / `refactor` / `docs` / `chore` / `test`
   - **TODO list**: what will be done this PR (becomes the checklist)
   - **Spec**: does a related spec exist in `.work/specs/`? Or does one need to be created?
   - **Open questions**: anything unclear or undecided

→ Proceed to Step 3

#### Output

- Title, type, TODO list, spec info, and open questions confirmed

---

### Step 3: Create task folder, PR folder, and TODO.md

#### Condition

- Step 2 complete

#### Process

1. Create `.work/tasks/{YYYYMMDD}_{title}/`
2. Create `.work/tasks/{YYYYMMDD}_{title}/PR{N}/`
3. Create `.work/tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md`:

```markdown
# PR{N} — {title}

## 仕様参照

<!-- 関連仕様書へのリンク -->
<!-- 例: [機能名](../../../specs/{spec-name}.md) -->

## TODO

{each task as: - [ ] task}

## 変更ファイル

<!-- Fill in after committing -->
```

→ Proceed to Step 4

#### Output

- `.work/tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md` created

---

### Step 4: Maintain the spec document

#### Condition

- Step 3 complete

#### Process

1. Check `.work/specs/` for a related spec
2. If found → update the relevant sections for this PR
3. If not found → create a new spec file:

```markdown
# {Feature Name} Spec

## Overview

{overview}

## Details

{specification}
```

4. Add a link to the spec in TODO.md's `## 仕様参照` section

→ Proceed to Step 5

#### Output

- Spec document exists and is linked from TODO.md

---

### Step 5: Record open questions in QA.md

#### Condition

- Step 4 complete

#### Process

1. Append any open questions from Step 2 to the `## 進行中` section of `.work/QA.md`
2. Skip if there are no open questions

→ Proceed to Step 6

---

### Step 6: Create the worktree and branch

#### Condition

- Step 5 complete

#### Process

1. Create the worktree:

```bash
git worktree add -b PR{N}/{type}/{title} ../$(basename $(pwd))-wt-PR{N}
```

→ Proceed to Step 7

#### Output

- Worktree created at `../repo-wt-PR{N}`
- Branch `PR{N}/{type}/{title}` exists

#### Notes

##### Prohibitions

- Never commit directly to master/main

---

### Step 7: Report and wait for approval

#### Process

1. Report what was created: branch name, worktree path, TODO.md path, spec path
2. Wait for user approval before starting implementation

#### Notes

##### Prohibitions

- Do not start implementation without explicit user approval
