---
name: work:issue-resolve
description: |
  Autonomously work through reviewed issues in `.work/issues/`, top to bottom — up to
  `${ISSUE_RESOLVE_AGENTS}` (default: `1`) actionable issues per invocation, processed sequentially.
  Issues whose `## 意思` is affirmative are dispatched to a `work:issue-resolver` subagent that
  creates a branch and drives it to the merge-waiting final commit; issues whose `## 意思` is
  negative are closed on a throwaway per-issue branch that is merged to master immediately within
  the same invocation.
  Designed to run under `/loop`. Trigger when the user says "イシューを対応して", "イシューを消化して",
  "resolve issues", "issue-resolve", or invokes `/loop /work:issue-resolve` / `/work:issue-resolve`
  explicitly.
---

# work:issue-resolve — Work Through Reviewed Issues (loop-driven)

Processes the issues that `work:issue-review` has triaged. Built to run under `/loop`: each
invocation handles up to **N actionable issues** (`${ISSUE_RESOLVE_AGENTS}`, default `1`),
sequentially top-to-bottom. Repeated loop ticks drain the queue while leaving a pile of
merge-waiting branches (from accepts) for the user to review and merge.

- **意思 affirmative + status: not_started** → dispatch a `work:issue-resolver` subagent (one
  subagent per issue) that creates a branch, implements the fix, and — depending on
  `direct_merge` — either merges directly into master or stops at the merge-waiting final commit.
- **意思 negative** → close as `wontfix` on a throwaway per-issue branch and **merge it to master
  immediately** within the same invocation (file moved to `closed/`). Nothing accumulates, so the
  issue index and master never drift. (A reject is a pure status change — safe to finalize at once;
  an accept is real work and still waits for the user to merge.)
- **意思 not checked** (unreviewed — all checkboxes still `- [ ]`) and **意思 affirmative + status:
  in_progress** (being worked, possibly another session) → skipped.

The issue format (no frontmatter, answer section at the top) / lifecycle is governed by `work-dir/イシュー.md`
(auto-injected) — follow it. The `## 意思` checkboxes are read by the AI: `- [x] 対応する` is
affirmative and `- [x] 対応しない` is negative; all still unchecked (`- [ ]`) means unreviewed.

---

## Overview

- **Prerequisite**: issues have been triaged with `work:issue-review` (their `## 意思` is filled in).
- **Up to N actionable issues per invocation** (`${ISSUE_RESOLVE_AGENTS}`, default `1`) — issues are
  processed sequentially, keeping each handled unit (branch / close) atomic and auditable.
- QA is resolved at review time (on the issue), so the resolver subagent should reach the final
  commit without stopping. **If a genuine blocker arises, the subagent stops** (see Step 3).

**Environment variables**:
- `${ISSUE_RESOLVE_AGENTS}` (default: `1`) — maximum number of actionable issues processed per
  invocation. Issues are handled one by one in ascending issue-number order.

---

## Tasks

### Step 1: Find the top-most actionable issue

#### Process

1. Read `${ISSUE_RESOLVE_AGENTS}` (default `1`); store as `N`. Initialize `handled = 0`.
2. If `.work/issues/` does not exist → report and stop.
3. Read `.work/issues/_index.yaml`. Collect entries with `status: not_started` and sort them
   ascending by issue number. These are the only candidates worth opening.
4. Walk the candidates top-down. For each, open the issue file and read the `## 意思` checkboxes:
   - `- [x] 対応しない` → REJECT action (Step 2).
   - `- [x] 対応する` → ACCEPT action (Step 3).
   - all `- [ ]` (none checked → unreviewed) → skip.
5. If no actionable issue exists → report "対応可能なイシューはありません" and stop (the loop can end).

→ Reject → Step 2 · Accept → Step 3

---

### Step 2: REJECT — close on a throwaway branch and merge to master immediately

Run all of this **in the main repository** (where this orchestrator runs, on `master`), not in a
worktree. The close must touch the main repo's `_index.yaml` (it is gitignored and per-working-copy
— this is the source of truth Step 1 reads), while the tracked change (the file move + archive) is
carried to `master` on a throwaway branch. The main repo's working tree must be clean before starting.

#### Process

1. Create and switch to a throwaway branch for this single reject (no task document — it lives only
   for this invocation):
   ```bash
   git switch -c chore/reject-ISSUE-{N}
   ```
2. Close the issue **in the main repo's `.work/issues`** (relative path — cwd is the main repo).
   This moves `ISSUE-{N}.md` → `closed/`, removes the entry from `_index.yaml`, and appends a
   `wontfix` record to `_index.archive.yaml`:
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/issue-tool.py" close \
     --issues-dir .work/issues \
     --issue-id ISSUE-{N} \
     --resolution wontfix \
     --linked-branch chore/reject-ISSUE-{N}
   ```
3. Commit the tracked change (file move + `_index.archive.yaml`) on the throwaway branch.
   `_index.yaml` is gitignored, so it is not committed — but its entry-removed state persists
   across the next branch switch (switch never touches gitignored files):
   ```bash
   git add .work/issues/
   git commit -m "chore: reject ISSUE-{N} ({title})"
   ```
4. Switch back to `master` and merge the throwaway branch with `--no-ff`, then delete it:
   ```bash
   git switch master
   git merge --no-ff -m "chore: reject ISSUE-{N} ({title})" chore/reject-ISSUE-{N}
   git branch -d chore/reject-ISSUE-{N}
   ```
   The merge into `master` trips `git-guard` once — confirm it and let the retry through. (The
   `master-commit-guard` does **not** fire here: it only matches `git commit`, and merge commits
   are exempt anyway.)

→ Proceed to Step 4

#### Notes

- **Why immediate merge**: a reject is a pure status change (move to `closed/` + archive record),
  so finalizing it at once keeps `master` and the issue index consistent every tick. The old shared
  `chore/rejected-issues` accumulation branch let the main repo's `_index.yaml` (entry still
  `not_started`) drift from the unmerged file move — exactly the inconsistency this avoids.
- **Why in the main repo, not a worktree**: a fresh worktree would have no `_index.yaml` (gitignored,
  never committed), so the close could not update the source-of-truth index. Running the close in the
  main repo updates `_index.yaml` directly; the gitignored edit survives the `master` switch, while
  the tracked move reaches `master` via the merge commit.
- **Never `git commit` directly on `master`** (guarded). The close/archive lands on the throwaway
  branch and reaches `master` only through the merge commit.

---

### Step 3: ACCEPT — dispatch an `work:issue-resolver` subagent

#### Process

1. Mark the issue in-progress in the **main repo** `_index.yaml` (cross-session lock, before
   dispatch):
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/issue-tool.py" set-status \
     --issues-dir .work/issues --issue-id ISSUE-{N} --status in_progress
   ```
2. **Determine `direct_merge`** for this issue:
   1. Read the `_index.yaml` entry for ISSUE-{N}; if it has a `direct_merge` field, use that value.
   2. Otherwise, analyze the issue content:
      - Any mention of UI, screen, visual, frontend, or user-visible output → `direct_merge: false`
      - Type is `refactor`, `test`, `docs`, or `backend`; no UI indicators → `direct_merge: true`
      - Unclear → `direct_merge: true` (default)
3. **Pick the subagent model by issue difficulty** (you, the orchestrator, decide and pass it via
   the Agent tool's `model` parameter — the agent itself fixes no model):
   - **Easy / localized** (single-file edit, doc/typo/rename, narrow scope) → `model: sonnet`
   - **Hard / complex** (cross-cutting change, tricky logic, multiple files, risky refactor) → `model: opus`
   - **Never use `haiku`.**
   Judge from the issue's `## 概要` / `## 対応案` scope; when unsure, prefer `opus`.
4. Dispatch **one** `work:issue-resolver` subagent (agent type `work:issue-resolver`, with the
   `model` chosen above) for this issue. Pass it: the `ISSUE-{N}` id and path, its resolved approach
   (the adopted `## 対応案` option 〔settled via the `## QA` answer〕 + any inline note on the `## 意思`
   answer), and the `direct_merge` value determined above.
5. On the subagent's return:
   - **Completed, merged** (`direct_merge: true`) → the resolver already closed the issue and
     merged. Record the branch; nothing more required.
   - **Completed, merge-waiting** (`direct_merge: false`) → record the branch it created; the user
     will merge it later.
   - **Blocked** (a genuine open question the issue did not pre-resolve) → the subagent recorded the
     blocker as a `## QA` entry in the issue's `# ユーザー回答欄` and reverted; revert the index lock:
     ```bash
     python "${CLAUDE_PLUGIN_ROOT}/scripts/issue-tool.py" set-status \
       --issues-dir .work/issues --issue-id ISSUE-{N} --status not_started
     ```
     Surface the blocker to the user (it needs another `work:issue-review` pass).

→ Proceed to Step 4

#### Notes

- One subagent per issue (= one branch). Under `/loop`, the next tick picks up the next issue.
- The subagent owns the worktree/branch/commits via `work:start`; this orchestrator only selects,
  locks, dispatches, and reports.

---

### Between issues: loop until N

After completing Step 2 or Step 3 for one issue, increment `handled`. If `handled < N` and
the candidate list is not exhausted, **return to Step 1** (re-read the index to pick up any
status changes) and handle the next issue. Once `handled == N` (or no more actionable issues
remain), proceed to Step 4.

---

### Step 4: Report

#### Process

1. Report what this invocation did: the issue handled, the action (accept+direct_merge→merged to
   master / accept+no-direct_merge→merge-waiting branch / reject→closed + merged to master), and
   the branch name. List anything left for the user (merge-waiting branches, surfaced blockers).
2. Under `/loop`, the loop re-invokes to handle the next issue.
