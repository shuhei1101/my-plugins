---
name: wt
description: Git worktree-based implementation workflow. Always apply this skill when the user wants to start a new implementation, create a new PR, begin work on a new branch, resume a worktree session, or manage parallel development tasks. Trigger whenever the user says "implement X", "new PR", "start working on", "worktree", "create a branch for", "parallel implementation", or resumes mid-session work. Every piece of work — code or docs — must use a worktree to prevent AI session interference.
---

# wt — Git Worktree Implementation Workflow

One session = one PR. Every task — implementation or documentation — runs inside a dedicated worktree on its own branch to prevent multiple AI sessions from interfering.

---

## Overview

Lifecycle: **Plan → Setup → Implement → Review → Merge → Cleanup**

All file writes during implementation happen inside the worktree. The main repository is never touched during implementation.

---

## Tasks

### Step 1: Plan

#### Condition

- User wants to start a new task or PR

#### Input

- User's description of the task

#### Process

1. Read `README.md` and scan `docs/` to understand the project. Clarify scope with the user if requirements are unclear.
2. Determine the PR number:
   - Scan `docs/PR/` for existing files to find the highest PR number
   - Next number = max + 1. Create `docs/PR/` if it does not exist.
3. Create the PR document at `docs/PR/PR{N}.md`:

```markdown
## Overview
{one concise phrase describing what this PR does}

## Tasks
- [ ] {task 1}
- [ ] {task 2}

## Implementation
| Action | File path | Class.Method | Change |
|--------|-----------|--------------|--------|
| add | src/foo.py | Foo.bar | new method |
| edit | src/main.py | main | call Foo.bar |

## Tests
| Action | File path | Target file | Class.Method | Change |
|--------|-----------|-------------|--------------|--------|
| add | tests/test_foo.py | src/foo.py | TestFoo.test_bar | test bar |
```

Optional sections: `## Design Notes`, `## Dependencies`, `## Risks`, `## User Verification`.

4. Confirm the plan with the user before creating any branch or worktree.

→ Proceed to Step 2

#### Output

- `docs/PR/PR{N}.md` created
- User has approved the plan

---

### Step 2: Set up the worktree

#### Condition

- User approved the plan from Step 1

#### Input

- PR number and base branch

#### Process

1. Confirm the base branch and clean state:
   ```bash
   git branch --show-current
   git status
   ```
   Warn if there are uncommitted changes or if on `master`/`main`.

2. Determine the branch name using the format `PR{N}/{type}/{description}`:
   - `type` follows Conventional Commits: `feat` / `fix` / `docs` / `refactor` / `test` / `chore`
   - Spaces and special characters → hyphens
   - Check for conflicts: `git branch --list {branch-name}`

3. Create branch and worktree:
   ```bash
   git branch {branch-name} {base-branch}
   git worktree add {worktree-path} {branch-name}
   ```
   Default path: `{parent-dir}/{repo-name}-wt-PR{N}`

4. Symlink dependencies (skip silently if target does not exist):
   - Python project (`pyproject.toml` or `setup.py`): `ln -s {main-repo}/venv {worktree}/venv`
   - Node.js project (`package.json`): `ln -s {main-repo}/node_modules {worktree}/node_modules` and `.next` if present
   - If symlinking fails: use `PYTHONPATH` to reuse the main repo's venv (see References)

5. Make the initial commits inside the worktree:
   ```bash
   git commit --allow-empty -m "chore: start PR{N} {description}"
   git add docs/PR/PR{N}.md
   git commit -m "docs: add PR{N} plan"
   ```

6. Save session state to `~/.claude/skill-memory/worktree/{YYYYMMDDHHMMSS}_session.md`:
   ```
   base branch, worktree path, PR number, current phase
   ```

→ Proceed to Step 3

#### Output

- Worktree created at `{worktree-path}`
- Branch `PR{N}/{type}/{description}` ready
- Session state saved

---

### Step 3: Implement

#### Condition

- Worktree is set up from Step 2

#### Input

- Task list in `docs/PR/PR{N}.md`

#### Process

1. All work happens inside the worktree directory — never touch the main repo during implementation.
2. Follow the tasks in `docs/PR/PR{N}.md`, checking them off as they complete.
3. Commit using Conventional Commits format:
   ```bash
   git add {files}
   git commit -m "feat: implement JWT authentication"
   ```
   Types: `feat` / `fix` / `refactor` / `docs` / `test` / `chore`
4. Update `~/.claude/skill-memory/worktree/` session file at each phase boundary.

→ Proceed to Step 4 when all tasks are checked off

#### Output

- All tasks completed and committed inside the worktree

#### Notes

##### Prohibitions

- Never run `pip install -e .` inside a worktree — it redirects the main repo's package to the worktree's `src/`, breaking the main server after cleanup

##### Gitignored config file rule

Files in `.gitignore` (`config/settings.yaml`, `.env`, etc.) must be edited in the main repo directly. Changes to these files inside a worktree are lost when `git worktree remove` runs.

In practice: when a PR adds new keys to `settings.yaml`, edit the main repo's `settings.yaml` directly and edit only `settings.yaml.sample` (tracked) inside the worktree.

---

### Step 4: Review and merge

#### Condition

- All tasks from Step 3 are complete and committed

#### Process

1. Show the user the worktree path and ask them to verify the implementation:
   ```
   Review the changes at: {worktree-path}
   ```
2. If the user requests changes → return to Step 3.
3. When the user confirms the review is done, output only:
   ```
   Commit complete — PR{N}: {one-line description of what changed}
   ```
   Then stop. Do **not** show merge commands. Do **not** ask "shall I merge?". The user runs the merge themselves:
   ```bash
   git checkout {base-branch}
   git merge --no-ff {branch-name}   # --no-ff preserves branch line in history
   ```
4. Wait for the user to confirm the merge is done.

→ Proceed to Step 5

#### Output

- User has merged the branch into the base branch

#### Notes

##### Prohibitions

- Never use `--squash` — always use `--no-ff` to preserve branch history as a merge commit

---

### Step 5: Clean up

#### Condition

- User confirms the merge is complete

#### Process

1. Remove the worktree and branch:
   ```bash
   git worktree remove {worktree-path}
   git branch -d {branch-name}
   ```
2. Update the session file: `## Status: completed`

→ Done

#### Output

- Worktree and branch removed
- Session marked as completed

#### Notes

##### Prohibitions

- Remote push is always the user's responsibility — this skill never runs `git push`

---

## References

### Worktree server launch and venv policy

**Never run `pip install -e .` inside a worktree.** Use `PYTHONPATH` instead:

```powershell
$env:PORT = "809{N}"
$env:PYTHONPATH = "{worktree-path}\src"
{main-repo}\.venv\Scripts\python.exe -m {package_name}
```

To stop a worktree server before cleanup:

```powershell
$port = 8091
$p = (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue).OwningProcess
if ($p) { Stop-Process -Id $p -Force }
```

### Resuming a session

1. Read `~/.claude/skill-memory/worktree/` to find the relevant session file
2. Check `## Current Status` to identify the last completed step
3. Run `git worktree list` to confirm the worktree still exists
4. Jump directly to the correct step and continue

### Key git commands

```bash
# List worktrees
git worktree list

# Current branch
git branch --show-current

# Check for uncommitted changes
git status

# Create branch + worktree
git branch PR{N}/{type}/{desc} {base}
git worktree add {path} PR{N}/{type}/{desc}

# Empty initial commit
git commit --allow-empty -m "chore: start PR{N} {desc}"

# Merge (run in main repo, not worktree)
git checkout {base}
git merge --no-ff {branch}

# Cleanup
git worktree remove {path}
git branch -d {branch}
```

---

## Project Rule Deployment

**On first use in a project**, check if `.claude/rules/pr-docs.md` exists. If not, create it:

1. Check: `Glob(".claude/rules/pr-docs.md")` in the project root.
2. If missing, create `.claude/rules/pr-docs.md` with this content:

```markdown
---
paths:
  - "docs/PR/**/*.md"
  - "docs/PR/index.yaml"
---

# PR Document Rules

## When to create a PR doc

Create `docs/PR/PR{N}.md` before or during every PR — never after the merge. For planning PRs (no implementation, only design/roadmap), create the doc first and set `planning: true` in index.yaml.

## Required sections

\`\`\`markdown
# PR{N} — {short title}

## Overview

{1–3 lines: what this PR does and why.}

## Scope

### Includes
- {item}

### Excludes
- {item}

## Changed Files

- `path/to/file` — one-line reason
\`\`\`

Optional sections: `Background`, `Prerequisites`, `Implementation Log`, `Decisions`, `Open Issues`.

## index.yaml — mandatory update

Every time you create or significantly update `docs/PR/PR{N}.md`, add or update the entry in `docs/PR/index.yaml`.

| Field | Rule |
|---|---|
| `id` | PR number (int) |
| `title` | Exact h1 text from PR{N}.md |
| `type` | `feat` / `fix` / `docs` / `refactor` / `chore` / `test` |
| `tags` | Free-form list |
| `planning` | `true` if this PR contains no implementation — only planning or design docs |
| `summary` | One line (≤120 chars) describing the PR without opening the file |
| `children` | List of child PR numbers when this planning PR defines sub-PRs |
| `parent` | Parent PR number when this PR was defined by a planning PR |
```

3. Create `.claude/rules-jp/pr-docs.md` as a stub:

```markdown
> **このファイルは日本語ミラーです。本体は `.claude/rules/pr-docs.md`。**
```

4. Commit: `git add .claude/rules/ && git commit -m "chore: add pr-docs rule"`
