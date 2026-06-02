---
name: worktree-create
description: |
  Create a git worktree for a branch.
  Called by work:start (Step 4) to create the worktree, or invoked directly.
  Trigger when the user says "ワークツリーを作って", "worktree を作成して", "work-add して",
  or invoked by work:start as `/work:worktree-create`.
---

# work:worktree-create — Create Worktree

Creates a git worktree and branch.

> **Naming**: branches use `{type}/{title}` (no `PR{N}/` prefix). The worktree path mirrors the
> branch name as `../{repo}-wt-{type}-{title}` (slashes replaced with hyphens).
> Existing worktrees with the legacy `wt-PR{N}` naming are left as-is — only newly created
> worktrees follow the new format.

---

## Tasks

### Step 1: Resolve arguments

#### Condition

- Always — run first

#### Process

1. If called with arguments (e.g. `refactor/rename-pr-to-branch`), parse them:
   - Single arg: branch name (`{type}/{title}`)
   - Legacy invocation `/work:worktree-create PR58 refactor/foo` is also accepted for back-compat:
     the `PR{N}` token is dropped and only the branch suffix is used.
2. If called without arguments, ask the user:
   - Branch type (`feat` / `fix` / `refactor` / `docs` / `chore` / `test`)
   - Title (kebab-case)

→ Proceed to Step 2

#### Output

- `BRANCH` — full branch name (`{type}/{title}`)

---

### Step 2: Create the worktree

#### Condition

- Step 1 complete

#### Process

1. Derive the worktree suffix by replacing slashes with hyphens:

```bash
BRANCH=refactor/rename-pr-to-branch
WT_SUFFIX="${BRANCH//\//-}"  # → refactor-rename-pr-to-branch
```

2. Read `${WORK_BASE_BRANCH}`:

```bash
base="${WORK_BASE_BRANCH:-}"
```

3. Create the worktree and branch:

```bash
if [ -n "$base" ]; then
  git worktree add -b "$BRANCH" "../$(basename $(pwd))-wt-${WT_SUFFIX}" "$base"
else
  git worktree add -b "$BRANCH" "../$(basename $(pwd))-wt-${WT_SUFFIX}"
fi
```

→ Proceed to Step 3

#### Output

- Worktree created at `../{repo}-wt-{type}-{title}`
- Branch `{type}/{title}` exists

#### Notes

##### Prohibitions

- Never commit directly to master/main

---

### Step 3: Report to caller

#### Condition

- Step 2 complete

#### Process

1. Report the created worktree path and branch name
2. If called from `work:start`, return control to the caller

#### Output

- Worktree path: `../{repo}-wt-{type}-{title}`
- Branch name: `{type}/{title}`
