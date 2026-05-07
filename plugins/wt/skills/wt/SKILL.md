---
name: wt
description: Git worktree-based implementation workflow. Always apply this skill when the user wants to start a new implementation, create a new PR, begin work on a new branch, resume a worktree session, or manage parallel development tasks. Trigger whenever the user says "implement X", "new PR", "start working on", "worktree", "create a branch for", "parallel implementation", or resumes mid-session work. Every piece of work — code or docs — must use a worktree to prevent AI session interference.
---

# wt — Git Worktree Implementation Workflow

## Core Principle

**1 session = 1 PR.** Every task — implementation or documentation — must be done inside a dedicated worktree on a dedicated branch. This prevents multiple AI sessions from stepping on each other.

The lifecycle is: **Plan → Setup → Implement → Review → Merge → Cleanup**

---

## Phase 1: Planning

Before touching any code or files:

1. **Understand the task.** Read `README.md`, scan `docs/` if present, and clarify scope with the user. If requirements are unclear, ask targeted questions before proceeding.
2. **Determine the PR number.** Scan `docs/PR/` for existing files to find the highest PR number. The next number is max + 1. If `docs/PR/` doesn't exist, create it.
3. **Create the PR document** at `docs/PR/PR{N}.md` using this template:

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

Add optional sections as needed: `## Design Notes`, `## Dependencies`, `## Risks`, `## User Verification`.

4. **Confirm the plan with the user** before creating any branch or worktree.

---

## Phase 2: Setup

After the user approves the plan:

1. **Confirm the base branch.** Run `git branch --show-current` and `git status`. Warn if there are uncommitted changes or if the current branch is `master`/`main`.

2. **Determine the branch name** using the format `PR{N}/{type}/{description}`:
   - `type` follows Conventional Commits: `feat` / `fix` / `docs` / `refactor` / `test` / `chore`
   - Spaces and special characters → hyphens
   - Japanese is allowed
   - Examples: `PR30/feat/login-implement`, `PR31/docs/update-wiki`, `PR32/fix/tts-timeout`
   - Check for conflicts: `git branch --list {branch-name}`

3. **Create branch and worktree:**

   ```bash
   git branch {branch-name} {base-branch}
   git worktree add {worktree-path} {branch-name}
   ```

   Worktree path default: `{parent-dir}/{repo-name}-wt-PR{N}`
   Example: if repo is `/c/Users/shuhe/repo/voice-paste`, worktree is `/c/Users/shuhe/repo/voice-paste-wt-PR30`

4. **Symlink dependencies** (skip silently if the target doesn't exist):
   - Python project (`pyproject.toml` or `setup.py` present): `ln -s {main-repo}/venv {worktree}/venv`
   - Node.js project (`package.json` present): `ln -s {main-repo}/node_modules {worktree}/node_modules` and `.next` if present

5. **Make the initial commits** inside the worktree:

   ```bash
   git commit --allow-empty -m "chore: start PR{N} {description}"
   git add docs/PR/PR{N}.md
   git commit -m "docs: add PR{N} plan"
   ```

6. **Save session state** to `~/.claude/skill-memory/worktree/{YYYYMMDDHHMMSS}_session.md`:
   ```
   base branch, worktree path, PR number, current phase
   ```

---

## Phase 3: Implementation

All work happens inside the worktree directory — never touch the main repo during implementation.

- Follow the tasks in `docs/PR/PR{N}.md`, checking them off as they complete
- Update `~/.claude/skill-memory/worktree/` session file at each phase boundary
- Commit with Conventional Commits format:
  - `feat:` new feature, `fix:` bug fix, `refactor:` refactoring, `docs:` docs, `test:` tests, `chore:` maintenance
  - Example: `git add . && git commit -m "feat: implement JWT authentication"`
- Verify changed files before committing

---

## Phase 4: Review & Merge

### User Review

After committing, show the user the worktree path and ask them to verify the implementation:

```
Review the changes at: {worktree-path}
```

If the user requests changes, return to Phase 3.

### Squash Merge

When the user confirms the review is done, output only:

```
Commit complete — PR{N}: {one-line description of what changed}
```

Then stop. Do **not** show merge commands. Do **not** ask "shall I merge?". The user performs the merge themselves in their own terminal:

```bash
# User runs this in the main repo
git checkout {base-branch}
git merge --squash {branch-name}
git commit -m "{description} #PR{N}"
```

Wait for the user to tell you the merge is done.

### Cleanup

After the user confirms the merge is complete, remove the worktree and branch:

```bash
git worktree remove {worktree-path}
git branch -D {branch-name}
```

Use `-D` (force delete) — squash-merged branches fail the `-d` safeguard check by design.

Update the session file: `## Status: completed`

Remote push is always the user's responsibility — this skill never runs `git push`.

---

## Resuming a Session

When the user wants to resume interrupted work:

1. Read `~/.claude/skill-memory/worktree/` to find the relevant session file
2. Check `## Current Status` to identify the last completed phase
3. Run `git worktree list` to confirm the worktree still exists
4. Jump directly to the correct phase and continue

---

## Key Git Commands Reference

```bash
# List worktrees
git worktree list

# Current branch
git branch --show-current

# Check for uncommitted changes
git status

# Next PR number — find max in existing docs
ls docs/PR/

# Create branch + worktree
git branch PR{N}/{type}/{desc} {base}
git worktree add {path} PR{N}/{type}/{desc}

# Empty initial commit
git commit --allow-empty -m "chore: start PR{N} {desc}"

# Squash merge (run in main repo, not worktree)
git checkout {base}
git merge --squash {branch}
git commit -m "{desc} #PR{N}"

# Cleanup
git worktree remove {path}
git branch -D {branch}
```
