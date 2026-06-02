# The session-start git snapshot is stale — a recorded "next PR" may already be merged

## What happened

This session implemented PR160 (ref-inject two-tier injection cache). When the user then
asked to "also do claude-kit", I initially treated it as the pending next-PR candidate I had
recorded in PR160's TODO (`migrate-claude-kit-to-ref-inject`).

Investigation showed that migration had **already been implemented and merged to master by
another session as PR159** — and master had advanced two PRs (PR159 + PR161) past the commit
shown in the session-start git status (`a26e1a8` → `e0f9344`). The git status injected at
session start, and therefore my mental model of "what's on master", was stale.

## Root cause

The git status provided at session start is a one-time snapshot ("will not update during the
conversation"). On a long session, master can advance via other sessions / worktrees. I
planned a follow-up — and had earlier recorded it as a next-PR candidate — based on that
stale view rather than on the actual current master.

A second consequence: the PR160 worktree had been branched off the stale `a26e1a8` (before
PR159 merged), so it did not contain claude-kit's migrated files. Syncing claude-kit required
a `git merge master` first (same family as `worktree-reserved-before-predecessor-merge`).

## Fix / Lesson

Before proposing or starting any follow-up / next-PR / cross-PR work, check the **actual**
current master (`git log -5 master`, `git worktree list`) instead of trusting the
session-start snapshot. A next-PR candidate recorded earlier may already be merged by a
parallel session, and the working branch may predate it.
