# conversation-to-claude Committed Directly to Master Instead of PR Branch

## What happened

`work-kit:merge` Step 3 invoked `claude-kit:conversation-to-claude`, but at that point the cwd was the **main repository on the master branch**.

`conversation-to-claude` writes to `.claude/rules/` and `.claude/references/` then runs `git commit`. Because cwd was on master, the commits went **directly to master**, bypassing the PR branch.

When the PR was then merged with `--no-ff`, the glossary/incidents updates remained as separate commits on master, never folded into the PR's merge commit.

## Impact

- The `git log` shows scattered `docs: PR{N} — added to glossary` commits separate from the PR's merge commit
- Reverting a single PR cleanly is impossible — the glossary/incidents fragments remain on master
- "PR work" and "session knowledge" — logically one unit — split into separate commits

## Fix

PR93 changed `work-kit:merge` Step 4 (formerly Step 3):

```bash
# Before: invoked from master cwd
/claude-kit:conversation-to-claude

# After: cd into worktree first
cd ../$(basename $(pwd))-wt-PR{N}
/claude-kit:conversation-to-claude
# Commit inside the worktree if needed
git -C ../$(basename $(pwd))-wt-PR{N} add .claude/
git -C ../$(basename $(pwd))-wt-PR{N} commit -m "docs: conversation-to-claude artifacts #PR{N}"
cd -
```

Now the generated `.claude/` files land on the PR branch and become part of the `--no-ff` merge commit.

## Lesson

**When delegating file writes to another skill, the caller must explicitly control the target cwd.**

Skills that perform `git commit` write to whichever branch happens to be at the caller's cwd. When delegating changes that should belong to a feature branch (not master), always `cd` into the worktree (or appropriate branch) before invoking.
