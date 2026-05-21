---
name: work-add
description: |
  Create a git worktree for a PR branch.
  Called by work-kit:work-start (Step 4) to create the worktree, or invoked directly.
  Trigger when the user says "ワークツリーを作って", "worktree を作成して", "work-add して",
  or invoked by work-start as `/worktree-kit:work-add`.
---

# worktree-kit:work-add — Create PR Worktree

Creates a git worktree and branch for a PR.

---

## Tasks

### Step 1: Resolve arguments

#### Condition

- Always — run first

#### Process

1. If called with arguments (e.g. `PR58 refactor/split-work-kit-worktree`), parse them:
   - First arg: PR number or `PR{N}` form → extract `N`
   - Second arg: branch suffix (`{type}/{title}`)
2. If called without arguments, ask the user:
   - PR number
   - Branch type and title (kebab-case)

→ Proceed to Step 2

#### Output

- `N` — PR number (integer)
- `TYPE_TITLE` — branch suffix, e.g. `refactor/split-work-kit-worktree`

---

### Step 2: Create the worktree

#### Condition

- Step 1 complete

#### Process

1. Determine the repo root name:

```bash
basename $(pwd)
```

2. Create the worktree and branch:

```bash
git worktree add -b PR{N}/{TYPE_TITLE} ../$(basename $(pwd))-wt-PR{N}
```

→ Proceed to Step 3

#### Output

- Worktree created at `../repo-wt-PR{N}`
- Branch `PR{N}/{TYPE_TITLE}` exists

#### Notes

##### Prohibitions

- Never commit directly to master/main

---

### Step 3: Report to caller

#### Condition

- Step 2 complete

#### Process

1. Report the created worktree path and branch name
2. If called from `work-start`, return control to the caller

#### Output

- Worktree path: `../repo-wt-PR{N}`
- Branch name: `PR{N}/{TYPE_TITLE}`
