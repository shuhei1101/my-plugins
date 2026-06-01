---
name: issue-review
description: |
  Review un-reviewed issues one by one and fill in their frontmatter decision (accept/reject),
  answer the issue's QA, and record a handling memo. Mobile-first: presents a readable summary of
  each issue and collects answers via AskUserQuestion (tap-friendly), walking through every
  un-reviewed issue in one run. Trigger when the user says "イシューをレビューして",
  "イシューを捌きたい", "review issues", "issue-review", or invokes `/work:issue-review` explicitly.
---

# work:issue-review — Triage Issues (mobile-first)

Walks every un-reviewed issue (`decision: pending`) in `.work/issues/`, top to bottom, and lets the
user decide **対応する (accept) / 対応しない (reject) / 後で (skip)** for each — plus answer the
issue's `## QA` and leave a handling memo. Built for phones: on a phone SSH session you can't
comfortably open issue files, so this skill presents a compact summary and collects answers with
`AskUserQuestion` (tap targets), not raw file viewing.

The result is written into each issue's **frontmatter `decision`** (the source of truth) and its
`## QA` / `## 対応メモ` sections. `work:issue-resolve` later acts on those decisions.

> `AskUserQuestion` use is intentional and required for this skill (see the global AskUserQuestion
> restriction — skills that define its use are exempt).

---

## Overview

- **Prerequisite**: `.work/issues/` exists (run `/work:setup` if not).
- **Un-reviewed** = an issue whose frontmatter `decision` is `pending` (or missing). Issues already
  `accept` / `reject` are skipped; `closed/` is ignored.
- The issue file format / frontmatter is governed by `work-dir/イシュー.md` (auto-injected when you
  edit a `.work/issues/` file) — follow it.

---

## Tasks

### Step 1: Collect un-reviewed issues

#### Process

1. If `.work/issues/` does not exist → tell the user to run `/work:setup`, then stop.
2. Glob `.work/issues/ISSUE-*.md` (exclude `closed/`). For each, read only the frontmatter
   `decision`. Keep those where `decision` is `pending` or absent.
3. Sort the kept issues by ascending issue number.
4. If none remain → report "未レビューのイシューはありません" and stop.

→ Proceed to Step 2

#### Output

- Ordered list of un-reviewed issue IDs

---

### Step 2: Review each issue (loop, top to bottom)

#### Process

For each un-reviewed issue, in order:

1. Read the issue file and present a **compact, phone-readable summary** — do NOT dump the raw file.
   Include: `ISSUE-N` + title, `## 概要`, the core of `## 問題点`, and the `## 修正案` options with
   the 推奨 option marked. Keep it short.
2. Ask the decision with `AskUserQuestion`:
   - Question: `ISSUE-N: {title} — どうする?`
   - Options: **対応する** (accept) / **対応しない** (reject) / **後で** (skip / leave pending)
   - The user may type a reason in the free-input ("Other") field.
3. **If 後で (skip)** → leave the issue untouched (`decision` stays `pending`) and move to the next.
4. **If 対応する / 対応しない**:
   a. If the issue has a `## QA` section with unresolved entries, present each (batch up to 4 per
      `AskUserQuestion` call) using the QA's listed options, and collect the user's answer. Write the
      answer back: set the QA's `回答` and `状態: 解決`, and reflect the chosen option into
      `## 修正案` (採用案) or the relevant section.
   b. Set the frontmatter `decision` to `accept` or `reject`.
   c. If the user gave a reason / extra instructions (from the decision step or a follow-up), write
      them into the issue's `## 対応メモ` section (create the heading if absent; leave it out if empty).
5. Move to the next issue.

→ After the last issue, proceed to Step 3

#### Notes

- Do **not** create branches or change `status` here — that happens in `work:issue-resolve`.
- Keep each issue's interaction self-contained so the user can stop partway (remaining issues stay
  `pending` and reappear next run).

---

### Step 3: Commit the review results

#### Process

1. If any issue files were changed, commit them. Issue files are git-tracked; this triage commit is
   made on the current branch (typically `master`). The `master-commit-guard` hook may prompt once —
   that is expected for issue triage; proceed.
   ```bash
   git add .work/issues/
   git commit -m "chore: イシューをレビュー（decision/QA を記入）"
   ```
   (Follow `WORK_COMMIT_LANG` / `WORK_COMMIT_TYPE` for the message, like other work commits.)
2. `_index.yaml` is git-ignored — do not commit it. No `status` change is needed here.
3. Report a summary: how many accepted / rejected / skipped.

#### Notes

- The decisions must be **committed** so `work:issue-resolve` (which works in fresh worktrees) can
  see them. Leaving them uncommitted would hide them from new worktrees.
