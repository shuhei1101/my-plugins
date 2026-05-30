---
name: pr-handoff
description: |
  Reserve the next branch using the same flow as work-start, after the current branch is complete.
  Reads the "Next branch candidates" section from the current branch document to determine what to
  work on, then records relevant background context in the new branch document.
  Candidates with a serial dependency (only doable after a preceding branch is merged) are NOT
  reserved now — they are embedded into the reserved preceding branch's "Next branch candidates"
  so the chain is carried forward.
  Trigger when the user says "引き継ぎ書を作って", "次のブランチをセットアップして", "ハンドオフして",
  "handoff して", "pr-handoff して", or calls `/workspace:pr-handoff` explicitly.
---

# workspace:pr-handoff — Reserve the Next Branch with Context

Reads the "Next branch candidates" from the current branch document and runs the same flow
as `work-start` to create the branch and work folder. Records relevant background
context in the new branch document to improve handoff quality.

When a serial dependency exists (a successor branch can only start after a preceding branch is
merged), reserve only the immediately-actionable candidates; embed the dependent
candidates into the reserved preceding branch's `## 次ブランチ候補` section.

> The skill name remains `pr-handoff` for historical and CLI compatibility, but the workflow now
> operates in branch terms — no `PR{N}` semantics. The "next branch candidates" table lives in the
> `## 次ブランチ候補` section of every branch document.

---

## Overview

After a branch is complete, the next session's Claude has zero context about what was done.
This skill runs the work-start reservation flow while writing background information
(why this branch is needed, decisions made in the previous branch) into the new branch document.

Additionally, when a successor branch can only be implemented after a preceding branch is merged
(serial dependency), reserving all candidates at once would create the successor's worktree
on a stale master base. To avoid this, dependent candidates are not reserved now — they are
transcribed into the preceding branch's `## 次ブランチ候補`, so when that branch completes and
pr-handoff runs again, the dependent candidate becomes the next immediate target.

---

## Tasks

### Step 1: Confirm and classify next branch candidates

#### Condition

- Always — run first

#### Process

1. Read the current branch document:
   ```
   .work/tasks/{task_folder}/{branch-hyphenated}.md
   ```

2. Read its `## 次ブランチ候補` table (columns: title / summary / 実施条件):
   - No candidates (placeholder text) → ask the user for the next branch details
   - Candidates present → inspect each row's `実施条件` column and classify as follows:

   | 実施条件 content | Classification |
   |---|---|
   | Empty, `-`, "即時実施可" or similar (no dependency) | **Immediately reservable** |
   | References a branch / candidate that is already merged (verifiable from history) | **Immediately reservable** |
   | Depends on another candidate in the same table (e.g. "{other candidate title} が完了したら") | **Dependent candidate (embed into preceding branch)** |

3. **Build a dependency graph and decide reservation order:**
   - Candidates with no dependency (roots) are **immediately reservable**
   - Candidates with dependencies are transcribed into the dependent root's "Next branch candidates" once that root is reserved
   - When a single root has multiple successors, preserve the successor-to-successor dependencies in the transcribed table

→ Proceed to Step 2

#### Output

- List of immediately reservable candidates
- List of dependent successor candidates attached to each immediately reservable candidate (if any)

#### Notes

##### Examples of 実施条件 phrasing

| Phrasing | Interpretation |
|---|---|
| Empty / `-` / `即時実施可` | Immediately reservable |
| `{merged branch name} がマージされたら` | Depends on an existing branch. If already merged → immediately reservable; if not → dependent |
| `「{other candidate title}」が完了したら` | Depends on another candidate in the same table. Treat as dependent |

##### Common misclassifications

- If a candidate title could match both an in-table candidate and a recently merged branch, prefer the in-table candidate (treat as serial dependency)
- If 実施条件 is ambiguous and undecidable, ask the user

---

### Step 2: Extract relevant background context

#### Condition

- Step 1 complete

#### Process

1. Review the current conversation and, for each immediately reservable candidate, select only the work **directly related** to it:
   - Why this candidate is needed
   - Design decisions or constraints decided in the current branch
   - Implementation notes that affect this candidate

2. Keep background context separate per candidate (do not merge across candidates if there are multiple)

3. For each immediately reservable candidate that has attached dependent successors, also note their title / summary / 実施条件 (these will be transcribed in Step 3)

→ Proceed to Step 3

#### Output

- Background context for each immediately reservable candidate
- Transcription data for dependent successor candidates

#### Notes

##### What to focus on

- Do not summarize the entire session — only extract what matters for the next branch
- The "why" and "we decided X in the last branch" relationships are what count
- If there is no relevant context, skip this extraction

---

### Step 3: Call work-start to reserve the next branch

#### Condition

- Step 2 complete

#### Process

1. Reserve each **immediately reservable** candidate one by one using `/workspace:work-start`:

   > Call `/workspace:work-start` for each candidate with its title and type.
   > Repeat until every immediately reservable candidate is reserved.

2. During each work-start's branch-document fill-in step (Step 7), fill in the following:
   - Append the background context from Step 2 to `## 概要`
   - Include "why this branch is needed" and "relationship to the previous branch"
   - **If this candidate has attached dependent successors, transcribe them into `## 次ブランチ候補`** (all three columns: title / summary / 実施条件)

→ Done

#### Output

- All immediately reservable candidates have their branch and work folder created
- Each new branch document contains background context
- Dependent successor candidates are transcribed into the preceding branch's `## 次ブランチ候補` and will be reserved by the next pr-handoff run

#### Notes

##### Difference from work-start

The differences from a plain `work-start` are these two points:

1. **The `## 概要` section of the new branch document is pre-filled with background context.**
2. **Dependent successor candidates are transcribed into the new branch's `## 次ブランチ候補` to carry forward the chain.**

Everything else (branch creation, folder creation, `## QA` section) follows work-start's standard flow.

##### Chained handoff example

A current branch's `## 次ブランチ候補`:

| Title | Summary | 実施条件 |
|---|---|---|
| feature-A | Add feature A | 即時実施可 |
| feature-B | Add feature B | feature-A が完了したら |
| feature-C | Add feature C | feature-B が完了したら |

→ After pr-handoff runs:

- Only `feat/feature-A` is reserved
- That branch's `## 次ブランチ候補` is populated with feature-B (実施条件: 即時実施可) and feature-C (実施条件: feature-B が完了したら)
- When `feat/feature-A` completes and pr-handoff runs again, feature-B becomes the next reserved branch, and feature-C is transcribed forward into its `## 次ブランチ候補`
