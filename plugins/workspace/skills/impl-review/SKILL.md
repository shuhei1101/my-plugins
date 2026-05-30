---
name: impl-review
description: |
  When /workspace:impl-review is invoked.
  Or when the user says "review the implementation", "check what was implemented", or "walk me through the changes".
---

# workspace:impl-review — Interactive Implementation Review

Analyzes commits on the current working branch and walks the user through each change area interactively using the `AskUserQuestion` tool. Items are presented in **batches of up to 4 per call** so the user only needs a few confirmation round-trips even for multi-feature branches. Designed for mobile or SSH contexts where reading code diffs directly is impractical.

---

## Overview

The skill builds an internal "overview list" of change areas and presents them in batches via `AskUserQuestion` — without showing the full list preview to the user. Each batch packs up to 4 items into a single `AskUserQuestion` call, the user answers all 4 at once, and any items marked "もっと詳しく" (deep dive) are spiralled into individually after the batch returns. Then the next batch is presented.

---

## Tasks

### Step 1: Identify the target branch

#### Condition

- Always — run first

#### Process

1. If there is an in-progress branch in the current conversation session, use that branch as the first priority
2. If a branch name (or fragment) is explicitly provided as an argument (e.g. `refactor/rename-pr-to-branch`, or a legacy `PR139` form), use it to find the branch:
   ```bash
   git branch --list "*{argument}*"
   ```
3. If neither applies, fall back to the current branch
4. Confirm the base branch (default: `master`)

→ Proceed to Step 2

#### Output

- Target branch and base branch confirmed

---

### Step 2: Analyze commits and diffs

#### Condition

- Step 1 complete

#### Process

1. Retrieve commit history:
   ```bash
   git log {base}..{branch} --oneline
   ```
2. Retrieve changed files summary:
   ```bash
   git diff {base}..{branch} --stat
   ```
3. If no commits exist beyond base → report "実装コミットがありません" and finish

→ Proceed to Step 3

#### Output

- Commit list and file change summary

---

### Step 3: Build the overview list internally

#### Condition

- Step 2 complete

#### Process

1. Analyze the commit messages and changed files autonomously
2. Group related changes into "change areas" (aim for 2–8 items):
   - Group by feature/purpose, not by file type (e.g. "新スキル qa-review の追加", "plugin.json バージョン更新")
3. For each area, prepare:
   - A one-line title (used as the `question` header)
   - A 2–3 sentence explanation of what changed and why
   - The key files involved

→ Proceed to Step 4 (do NOT show the full list to the user)

#### Output

- Overview list with 2–8 change areas (held internally)

#### Notes

- Decide what to show autonomously based on changed files — no fixed template
- Backend changes: focus on API surface changes, side effects, data model impact
- Frontend changes: focus on affected screens, user-visible behavior changes
- Config/infra changes: focus on what was enabled/disabled and the blast radius
- Adjust granularity to change size: a one-file fix needs 1 item; a multi-feature branch may need 6–8

---

### Step 4: Batched interactive review

#### Condition

- Step 3 complete

#### Process

Split the overview list into **batches of up to 4 items** and present each batch. `AskUserQuestion` accepts up to 4 questions per call, so batching minimizes confirmation round-trips (e.g. 5 items → 4 + 1, 8 items → 4 + 4).

For each batch, do the following:

1. Call `AskUserQuestion` **once**, packing the batch's items into the `questions` array. For each question:
   - **question**: The item's 2–3 sentence explanation
   - **header**: Item number and short title (max 12 chars) — e.g. `1/8 qa-review`
   - **options**:
     - `OK / 次へ` — Understood
     - `もっと詳しく` — Explain this area in more depth
     - `問題あり` — Flag this area for follow-up
   - **multiSelect**: false

2. When the batch result returns, classify each answer:
   - `OK / 次へ` → no action
   - `もっと詳しく` → enqueue for deep-dive after this batch finishes
   - `問題あり` → record as flagged

3. If any items were enqueued for deep-dive, run the deep-dive loop on each one in order (deep-dive cannot be batched — one item at a time):
   - Present detailed information: specific code changes, the reason for the approach, potential risks
   - Call `AskUserQuestion`:
     - **question**: 「さらに深掘りしますか？」
     - **options**: `OK / 終わり` / `別の角度から説明して` / `問題あり`
   - Continue until the user selects `OK / 終わり` or `問題あり`

4. Once all deep-dives for the current batch are done, proceed to the next batch.

→ Proceed to Step 5

#### Notes

##### Why batched

The old design called `AskUserQuestion` once per item, so 8 areas cost 8 confirmation round-trips — painful on mobile or SSH. `AskUserQuestion` supports up to 4 questions per call, so 8 areas finish in 2 round-trips (4 + 4) plus deep-dive turns.

##### Batch size selection

- Total ≤ 4 → one batch with all items
- 5–8 → 4 + remainder, or split evenly
- 9+ → split into batches of 4
- There is no reason to deliberately under-fill a batch (deep-dives are a separate loop, so packing all 4 questions is always fine)

---

### Step 5: Completion report

#### Condition

- All items reviewed (Step 4 complete)

#### Process

1. Output a summary:
   - Total items reviewed
   - Flagged items (if any) with their titles
2. If items were flagged → suggest next actions (fix, add QA entry, etc.)
3. If no items flagged → "すべての実装内容を確認しました。"

→ Done
