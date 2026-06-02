---
name: work:issue-review
description: |
  Review un-reviewed issues one by one by recording answers in their "ユーザー回答欄" (user answer
  section): check one `## 意思` option (対応する（自動マージ）/ 対応する（マージはAIに任せる）/ 対応しない)
  and answer the issue's `## QA` (check one option for choice-type entries, fill in `**回答**:` for
  input-type entries). Mobile-first: presents a readable summary of
  each issue and collects answers via AskUserQuestion (tap-friendly), walking through every
  un-reviewed issue in one run. Trigger when the user says "イシューをレビューして",
  "イシューを捌きたい", "review issues", "issue-review", or invokes `/work:issue-review` explicitly.
---

# work:issue-review — Triage Issues (mobile-first)

Walks every un-reviewed issue in `.work/issues/`, top to bottom, and lets the user decide
**対応する（自動マージ） / 対応する（マージはAIに任せる） / 対応しない (skip) / 後で (later)** for each —
plus answer the issue's `## QA`. Built for phones: on a phone SSH session you can't comfortably open
issue files, so this skill presents a compact summary and collects answers with `AskUserQuestion`
(tap targets), not raw file viewing.

The result is written into each issue's **`# ユーザー回答欄`** by checking one `## 意思` checkbox and
answering each `## QA` entry — choice-type entries by checking one box (`[ ]` → `[x]`), input-type
entries by filling in the `**回答**:` line. Any free-form note is appended as a comment below the
checked 意思 line (there is no `## 自由記述` section). `work:issue-resolve` later acts on it.

> `AskUserQuestion` use is intentional and required for this skill (see the global AskUserQuestion
> restriction — skills that define its use are exempt).

---

## Overview

- **Prerequisite**: `.work/issues/` exists (run `/work:setup` if not).
- **Un-reviewed** = an issue whose `## 意思` checkboxes are all still unchecked (`- [ ]`). Issues
  with one checkbox checked (`- [x]`) are skipped; `closed/` is ignored.
- The issue file format (no frontmatter, answer section at the top) is governed by `work-dir/イシュー.md`
  (auto-injected when you edit a `.work/issues/` file) — follow it.

---

## Tasks

### Step 1: Collect un-reviewed issues

#### Process

1. If `.work/issues/` does not exist → tell the user to run `/work:setup`, then stop.
2. Glob `.work/issues/ISSUE-*.md` (exclude `closed/`). For each, read the `## 意思` checkboxes.
   Keep those with all checkboxes still unchecked (`- [ ]`).
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
   Include: `ISSUE-N` + title, `## 概要`, the core of `## 現状`, and the `## 対応案` options with the
   推奨 option marked (if any). Keep it short.
2. Ask the 意思 with `AskUserQuestion` (4 options, tap-friendly):
   - Question: `ISSUE-N: {title} — どうする?`
   - Options:
     - **対応する（自動マージ）** → maps to `- [x] 対応する（自動マージ）` (Claude merges to master after finishing)
     - **対応する（マージはAIに任せる）** → maps to `- [x] 対応する（マージはAIに任せる）` (AI decides whether to auto-merge or stop merge-waiting)
     - **対応しない** → maps to `- [x] 対応しない`
     - **後で** → leave un-answered
   - The user may type a reason / instruction in the free-input ("Other") field.
3. **If 後で (later)** → leave the issue untouched (`## 意思` keeps all boxes unchecked) and move to the next.
4. **If any 対応する variant / 対応しない**:
   a. If the issue has a `## QA` with unanswered entries, present each (batch up to 4 per
      `AskUserQuestion` call) and collect the answer. Write it back per the entry's type:
      - **Choice-type** (has `- [ ]` option checkboxes) → **check the chosen option** (`[ ]` → `[x]`),
        using that entry's options as the AskUserQuestion choices. When `## 対応案` has multiple
        options, settle the adopted one here.
      - **Input-type** (has a `**回答**:` line, no checkboxes) → write the user's answer onto the
        `**回答**:` line (e.g. `**回答**: 公開APIのみ対象`).
   b. Check the chosen `## 意思` checkbox (`[ ]` → `[x]`) — exactly one of the three.
   c. If the user gave a free-form handling instruction / reason (from the 意思 step's free-input or a
      follow-up), append it as a note below the checked 意思 line (e.g. `> 公開APIのみ`).
5. Move to the next issue.

→ After the last issue, proceed to Step 3

#### Notes

- Do **not** create branches or change the `_index.yaml` `status` here — that happens in
  `work:issue-resolve`.
- Keep each issue's interaction self-contained so the user can stop partway (remaining issues stay
  un-answered and reappear next run).

---

### Step 3: Commit the review results

#### Process

1. If any issue files were changed, commit them. Issue files are git-tracked; this triage commit is
   made on the current branch (typically `master`). The `master-commit-guard` hook may prompt once —
   that is expected for issue triage; proceed.
   ```bash
   git add .work/issues/
   git commit -m "chore: イシューをレビュー（意思/QA を記入）"
   ```
   (Follow `${WORK_COMMIT_LANG}` / `${WORK_COMMIT_TYPE}` for the message, like other work commits.)
2. `_index.yaml` is git-ignored — do not commit it. No `status` change is needed here.
3. Report a summary: how many 対応する / 対応しない / 後で.

#### Notes

- The decisions must be **committed** so `work:issue-resolve` (which works in fresh worktrees) can
  see them. Leaving them uncommitted would hide them from new worktrees.
