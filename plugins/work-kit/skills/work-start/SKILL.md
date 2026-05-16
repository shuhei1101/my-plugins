---
name: work-start
description: |
  Start a new PR: create the task folder, PR folder, TODO.md, add an entry to index.yaml,
  update the relevant spec in .work/specs/, record unknowns in .work/QA.md, then create
  the worktree and branch.
  Trigger when the user says "新しい PR を作って", "新しい作業を始めたい", "work-start して",
  "start new work", or "create a new PR".
allowed-tools: Bash Read Write
---

# work-kit:work-start — Start a New PR

Creates the task/PR folder structure with TODO.md, adds an entry to index.yaml,
maintains the spec and QA documents, then sets up the worktree.
Waits for user approval before implementation begins.

---

## Tasks

### Step 1: Determine the next PR number

#### Condition

- Always — run first

#### Process

1. If the user has already specified a PR number or branch name, use that value
2. Otherwise read `.work/tasks/index.yaml` and use max `id` + 1 as the next PR number (1 if the list is empty)

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
3. Create `TODO.md` using the template at `.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md`

→ Proceed to Step 4

#### Output

- `.work/tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md` created

---

### Step 4: Add entry to index.yaml

#### Condition

- Step 3 complete

#### Process

1. Append to the `prs` list in `.work/tasks/index.yaml`:

```yaml
- id: {N}
  title: 'PR{N} — {title}'
  type: {type}
  tags: []
  summary: '{summary}'
  task: '{YYYYMMDD}_{title}'
  completed: false
```

→ Proceed to Step 5

#### Output

- `.work/tasks/index.yaml` updated with the new PR entry

---

### Step 5: Maintain the spec document

#### Condition

- Step 4 complete

#### Process

1. Check `.work/specs/` for a related spec
2. If found → update the relevant sections for this PR
3. If not found → create a new spec using the template at `.work/specs/xxx.md`
4. Add a link to the spec in TODO.md's `## 仕様参照` section

→ Proceed to Step 6

---

### Step 6: Record open questions in QA.md

#### Condition

- Step 5 complete

#### Process

1. Append any open questions from Step 2 to `.work/QA.md` as QA-XXX entries
2. Skip if there are no open questions

→ Proceed to Step 7

---

### Step 7: Create the worktree and branch

#### Condition

- Step 6 complete

#### Process

1. Create the worktree:

```bash
git worktree add -b PR{N}/{type}/{title} ../$(basename $(pwd))-wt-PR{N}
```

→ Proceed to Step 8

#### Notes

##### Prohibitions

- Never commit directly to master/main

---

### Step 8: Add worktree to VS Code workspace

#### Condition

- Step 7 complete

#### Process

1. Get the repository name: `REPO=$(basename $(pwd))`
2. Look for `../${REPO}.code-workspace`
3. If not found, scan `../` for `*.code-workspace` files containing `${REPO}`
4. If still not found, ask the user for the workspace file path
5. Add the following entry to the `folders` array in the workspace file:

```json
{"path": "./${REPO}-wt-PR{N}"}
```

→ Proceed to Step 9

#### Output

- Workspace file updated with the new worktree entry

---

### Step 9: Report and wait for approval

#### Process

1. Report what was created: branch name, worktree path, TODO.md path, spec path
2. Wait for user approval before starting implementation

#### Notes

##### Prohibitions

- Do not start implementation without explicit user approval
