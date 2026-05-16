---
name: work-start
description: |
  Start a new PR: determine the next PR number, collect info from the user, create a worktree
  and branch, create the PR task document and folder, and add an entry to index.yaml.
  Trigger when the user says "新しい PR を作って", "新しい作業を始めたい", "work-start して",
  "start new work", or "create a new PR".
allowed-tools: Bash Read Write
---

# work-kit:work-start — Start a New PR

Creates a worktree, branch, PR task document, and index.yaml entry for a new PR.
Waits for user approval before implementation begins.

---

## Tasks

### Step 1: Determine the next PR number

#### Condition

- Always — run first

#### Process

1. Read `docs/tasks/index.yaml`
2. Next PR number = max `id` in the `prs` list + 1 (1 if the list is empty)

→ Proceed to Step 2

#### Output

- Next PR number confirmed (e.g., 171)

---

### Step 2: Collect PR information

#### Condition

- Step 1 complete

#### Process

1. Ask the user for:
   - **Type**: `feat` / `fix` / `refactor` / `docs` / `chore` / `test`
   - **Description**: kebab-case short identifier (e.g., `add-bgm-feature`)
   - **Summary**: one-line PR summary
   - **Task list**: what will be done (becomes the checklist)

→ Proceed to Step 3

#### Output

- PR type, description, summary, and task list confirmed

---

### Step 3: Create the worktree and branch

#### Condition

- Step 2 complete

#### Process

1. Create a worktree with a new branch:

```bash
git worktree add -b PR{N}/{type}/{description} ../$(basename $(pwd))-wt-PR{N}
```

→ Proceed to Step 4

#### Output

- Worktree created at `../repo-wt-PR{N}`
- Branch `PR{N}/{type}/{description}` exists

#### Notes

##### Prohibitions

- Never commit directly to master/main

---

### Step 4: Create the PR task document

#### Condition

- Step 3 complete

#### Process

1. Create the task folder: `docs/tasks/{YYYYMMDD}_{description}/`
2. Create the PR document: `docs/tasks/{YYYYMMDD}_{description}/PR{N}.md`

Template:

```markdown
# PR{N} — {summary}

## 概要

{summary}

## 作業内容

{each task item as: - [ ] task}

## 変更ファイル

<!-- Fill in after committing -->
```

→ Proceed to Step 5

#### Output

- `docs/tasks/{YYYYMMDD}_{description}/PR{N}.md` created

---

### Step 5: Add entry to index.yaml

#### Condition

- Step 4 complete

#### Process

1. Append to the `prs` list in `docs/tasks/index.yaml`:

```yaml
- id: {N}
  title: 'PR{N} — {summary}'
  type: {type}
  tags: []
  summary: '{summary}'
  completed: false
  task: '{YYYYMMDD}_{description}'
```

→ Proceed to Step 6

#### Output

- `docs/tasks/index.yaml` updated with the new PR entry

---

### Step 6: Report and wait for approval

#### Process

1. Report what was created:
   - Branch name
   - Worktree path
   - PR document path
2. Wait for user approval before starting implementation

#### Output

- User has reviewed and approved

#### Notes

##### Prohibitions

- Do not start implementation without explicit user approval
