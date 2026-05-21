# master Direct Edit Causes Merge Conflict

**Date**: 2026-05-21
**Category**: wrong-assumption

## What Happened

While preparing to modify `SKILL.jp.md` and `SKILL.md`, the files were edited directly
on the `master` branch before running `work-start` to create a worktree. Later, when
the same files were correctly edited inside the worktree and a `git merge --no-ff` was
attempted, Git reported a conflict because master already contained uncommitted changes
to those files. The fix was `git restore <files>` on master, discarding the stale edits.

## How to Avoid

Never edit files on `master`. Always run `/work-kit:work-start` first to create the
worktree and branch, then make all changes inside the worktree. The UserPromptSubmit
hook enforces this, but the check can be skipped mentally when a task feels "small".

## Context

Applies to the `my-plugins` repository. The worktree is created at
`../my-plugins-wt-PR{N}` and the branch is `PR{N}/{type}/{title}`.
