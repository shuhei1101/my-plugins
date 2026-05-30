---
name: pr-handoff
description: |
  Reserve the next PR using the same flow as work-start, after the current PR is complete.
  Reads the "Next PR candidates" section from the current PR document to determine what to work on,
  then records relevant background context in the new PR document.
  Candidates with a serial dependency (only doable after a preceding PR is merged) are NOT
  reserved now — they are embedded into the reserved preceding PR's "Next PR candidates"
  so the chain is carried forward.
  Trigger when the user says "引き継ぎ書を作って", "次のPRをセットアップして", "ハンドオフして",
  "handoff して", "pr-handoff して", or calls `/work:pr-handoff` explicitly.
---

# work:pr-handoff — Reserve the Next PR with Context

Reads the "Next PR candidates" from the current PR document and runs the same flow
as `work-start` to create the branch and work folder. Records relevant background
context in the new PR document to improve handoff quality.

When a serial dependency exists (a successor PR can only start after a preceding PR is
merged), reserve only the immediately-actionable candidates; embed the dependent
candidates into the reserved preceding PR's `## 次PR候補` section.

---

## Overview

After a PR is complete, the next session's Claude has zero context about what was done.
This skill runs the work-start reservation flow while writing background information
(why this PR is needed, decisions made in the previous PR) into the new PR document.

Additionally, when a successor PR can only be implemented after a preceding PR is merged
(serial dependency), reserving all candidates at once would create the successor's worktree
on a stale master base. To avoid this, dependent candidates are not reserved now — they are
transcribed into the preceding PR's `## 次PR候補`, so when that PR completes and pr-handoff
runs again, the dependent candidate becomes the next immediate target.

---

## Tasks

### Step 1: Confirm and classify next PR candidates

#### Condition

- Always — run first

#### Process

1. Read the current PR document:
   ```
   .work/tasks/{task_folder}/{branch-hyphenated}.md
   ```

2. Read its `## 次PR候補` table (columns: title / summary / 実施条件):
   - No candidates (placeholder text) → ask the user for the next PR details
   - Candidates present → inspect each row's `実施条件` column and classify as follows:

   | 実施条件 content | Classification |
   |---|---|
   | Empty, `-`, "即時実施可" or similar (no dependency) | **Immediately reservable** |
   | References a PR number that is already merged (verifiable from history) | **Immediately reservable** |
   | Depends on another candidate in the same table (e.g. "{other candidate title} が完了したら") | **Dependent candidate (embed into preceding PR)** |

3. **Build a dependency graph and decide reservation order:**
   - Candidates with no dependency (roots) are **immediately reservable**
   - Candidates with dependencies are transcribed into the dependent root's "Next PR candidates" once that root is reserved
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
| `PR10 がマージされたら` | Depends on PR10 (existing). If PR10 is already merged → immediately reservable; if not → dependent |
| `「{other candidate title}」が完了したら` | Depends on another candidate in the same table. Treat as dependent |

##### Common misclassifications

- If a PR number could match both a candidate title and a past PR number, prefer the in-table candidate (treat as serial dependency)
- If 実施条件 is ambiguous and undecidable, ask the user

---

### Step 2: Extract relevant background context

#### Condition

- Step 1 complete

#### Process

1. Review the current conversation and, for each immediately reservable candidate, select only the work **directly related** to it:
   - Why this candidate is needed
   - Design decisions or constraints decided in the current PR
   - Implementation notes that affect this candidate

2. Keep background context separate per candidate (do not merge across candidates if there are multiple)

3. For each immediately reservable candidate that has attached dependent successors, also note their title / summary / 実施条件 (these will be transcribed in Step 3)

→ Proceed to Step 3

#### Output

- Background context for each immediately reservable candidate
- Transcription data for dependent successor candidates

#### Notes

##### What to focus on

- Do not summarize the entire session — only extract what matters for the next PR
- The "why" and "we decided X in the last PR" relationships are what count
- If there is no relevant context, skip this extraction

---

### Step 3: Call work-start to reserve the next PR

#### Condition

- Step 2 complete

#### Process

1. Reserve each **immediately reservable** candidate one by one using `/work:start`:

   > Call `/work:start` for each candidate with its title and type.
   > Repeat until every immediately reservable candidate is reserved.

2. During each work-start's PR-document fill-in step (Step 7), fill in the following:
   - Append the background context from Step 2 to `## 概要`
   - Include "why this PR is needed" and "relationship to the previous PR"
   - **If this candidate has attached dependent successors, transcribe them into `## 次PR候補`** (all three columns: title / summary / 実施条件)

→ Done

#### Output

- All immediately reservable candidates have their branch and work folder created
- Each new PR document contains background context
- Dependent successor candidates are transcribed into the preceding PR's `## 次PR候補` and will be reserved by the next pr-handoff run

#### Notes

##### Difference from work-start

The differences from a plain `work-start` are these two points:

1. **The `## 概要` section of the new PR document is pre-filled with background context.**
2. **Dependent successor candidates are transcribed into the new PR's `## 次PR候補` to carry forward the chain.**

Everything else (branch creation, folder creation, `## QA` section) follows work-start's standard flow.

##### Chained handoff example

The current PR99's `## 次PR候補`:

| Title | Summary | 実施条件 |
|---|---|---|
| feature-A | Add feature A | 即時実施可 |
| feature-B | Add feature B | feature-A が完了したら |
| feature-C | Add feature C | feature-B が完了したら |

→ After pr-handoff runs:

- Only feature-A is reserved as PR100
- PR100's `## 次PR候補` is populated with feature-B (実施条件: 即時実施可) and feature-C (実施条件: feature-B が完了したら)
- When PR100 completes and pr-handoff runs again, feature-B becomes PR101, and feature-C is transcribed forward into PR101's `## 次PR候補`