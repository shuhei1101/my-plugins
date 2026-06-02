---
name: issue-resolve
description: |
  Autonomously work through reviewed issues in `.work/issues/`, top to bottom — one actionable
  issue per invocation. Issues whose `## 意思` is affirmative are dispatched to a
  `work:issue-resolver` subagent that creates a branch and drives it to the merge-waiting final
  commit; issues whose `## 意思` is negative are closed on a shared `chore/rejected-issues` branch.
  Designed to run under `/loop`. Trigger when the user says "イシューを対応して", "イシューを消化して",
  "resolve issues", "issue-resolve", or invokes `/loop /work:issue-resolve` / `/work:issue-resolve`
  explicitly.
---

# work:issue-resolve — Work Through Reviewed Issues (loop-driven)

Processes the issues that `work:issue-review` has triaged. Built to run under `/loop`: each
invocation handles the **single top-most actionable issue**, so repeated loop ticks drain the queue
while leaving a pile of merge-waiting branches for the user to review and merge.

- **意思 affirmative + status: not_started** → dispatch a `work:issue-resolver` subagent (one
  subagent per issue) that creates a branch via `work:start`, implements the fix, and stops at the
  **merge-waiting final commit** (merge is the user's call, separately).
- **意思 negative** → close as `wontfix` on the shared `chore/rejected-issues` branch (file moved to
  `closed/`), accumulating there until the user merges that branch.
- **意思 blank** (unreviewed) and **意思 affirmative + status: in_progress** (being worked, possibly
  another session) → skipped.

The issue format (no frontmatter, two halves) / lifecycle is governed by `work-dir/イシュー.md`
(auto-injected) — follow it. The `## 意思` `**回答**:` is free human text; read "対応する/様子見" as
affirmative and "対応しない" as negative.

---

## Overview

- **Prerequisite**: issues have been triaged with `work:issue-review` (their `## 意思` is filled in).
- **One actionable issue per invocation** keeps each loop tick to a single branch / merge unit.
- QA is resolved at review time (on the issue), so the resolver subagent should reach the final
  commit without stopping. **If a genuine blocker arises, the subagent stops** (see Step 3).

---

## Tasks

### Step 1: Find the top-most actionable issue

#### Process

1. If `.work/issues/` does not exist → report and stop.
2. Glob `.work/issues/ISSUE-*.md` (exclude `closed/`). For each, read the `## 意思` `**回答**:`; read
   the work `status` from the matching `_index.yaml` entry. Sort ascending by issue number.
3. Walk the list top-down and select the **first** issue that is actionable:
   - `## 意思` negative (対応しない) → REJECT action (Step 2).
   - `## 意思` affirmative (対応する/様子見) and `status: not_started` → ACCEPT action (Step 3).
   - Skip `## 意思` blank (unreviewed) and affirmative + `status: in_progress`.
4. If no actionable issue exists → report "対応可能なイシューはありません" and stop (the loop can end).

→ Reject → Step 2 · Accept → Step 3

---

### Step 2: REJECT — close on the shared `chore/rejected-issues` branch

#### Process

1. Ensure the shared reject branch + worktree exists:
   - Check `git worktree list` for `chore/rejected-issues`.
   - **If missing**: create it with `/work:start` (type `chore`, title `rejected-issues`). Its branch
     document states its sole purpose — *"reject されたイシューを `closed/` へ退避するための集約ブランチ。
     マージするとリジェクトが確定する"* — and carries a table that each closed reject is appended to.
     This makes the intent survive across sessions (context is otherwise lost).
2. In the reject worktree, close the issue (its file is git-tracked and present there):
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/issue-tool.py" close \
     --issues-dir {REJECT_WT}/.work/issues \
     --issue-id ISSUE-{N} \
     --resolution wontfix \
     --linked-branch chore/rejected-issues
   ```
   This moves `ISSUE-{N}.md` → `closed/` and appends a `wontfix` record to `_index.archive.yaml`.
3. Append a row to the reject branch document recording the issue ID, title, and the reject reason
   (from the issue's `## 自由記述` / `## 意思` answer).
4. Commit on `chore/rejected-issues` (issue move + branch doc). Do **not** merge — the user merges
   when ready.

→ Proceed to Step 4

#### Notes

- Never close rejects on `master` — the move/archive must be committed on a branch (master-commit
  is guarded). The shared chore branch keeps all rejects together as one merge unit.

---

### Step 3: ACCEPT — dispatch an `work:issue-resolver` subagent

#### Process

1. Mark the issue in-progress in the **main repo** `_index.yaml` (cross-session lock, before
   dispatch):
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/issue-tool.py" set-status \
     --issues-dir .work/issues --issue-id ISSUE-{N} --status in_progress
   ```
2. **Pick the subagent model by issue difficulty** (you, the orchestrator, decide and pass it via
   the Agent tool's `model` parameter — the agent itself fixes no model):
   - **Easy / localized** (single-file edit, doc/typo/rename, narrow scope) → `model: sonnet`
   - **Hard / complex** (cross-cutting change, tricky logic, multiple files, risky refactor) → `model: opus`
   - **Never use `haiku`.**
   Judge from the issue's `## 概要` / `## 対応案` scope; when unsure, prefer `opus`.
3. Dispatch **one** `work:issue-resolver` subagent (agent type `work:issue-resolver`, with the
   `model` chosen above) for this issue. Pass it: the `ISSUE-{N}` id and path, its resolved approach
   (the adopted `## 対応案` option 〔settled via the `## QA` answer〕 + the `## 自由記述` answer), and
   the instruction to take the branch all the way to the **merge-waiting final commit** (do not merge).
4. On the subagent's return:
   - **Completed (merge-waiting)** → record the branch it created; the user will merge it later.
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

### Step 4: Report

#### Process

1. Report what this invocation did: the issue handled, the action (accept→branch / reject→closed),
   and the branch name. List anything left for the user (branches awaiting merge, surfaced blockers).
2. Under `/loop`, the loop re-invokes to handle the next issue.
