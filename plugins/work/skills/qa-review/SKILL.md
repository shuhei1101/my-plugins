---
name: qa-review
description: |
  When /work:qa-review is invoked.
  Or when the user says "review QA", "check QA items", or "answer the QA".
---

# work:qa-review — Interactive QA Review

Reads the `## QA` section of a branch document and presents unresolved items via the `AskUserQuestion` tool, batching up to 4 questions per call. After all responses are collected, updates the branch document in a single pass.

---

## Tasks

### Step 1: Resolve the target branch document

#### Condition

- Always — run first

#### Process

1. If there is an in-progress branch in the current conversation session, use its branch document as the first priority
2. If a branch name (or fragment) is explicitly provided as an argument, use it to find the matching branch document
3. If neither applies:
   - Search for branch documents: `find .work/tasks -type f -name "*.md" -not -name ".*"`
   - If only one is found, use it automatically
   - If multiple exist, use `AskUserQuestion` to ask the user which branch document to review
4. Also check git worktrees in case the target is in a sibling worktree:
   ```bash
   git worktree list
   ```
5. Confirm the branch document path (pattern: `.work/tasks/{YYMMDD}_{title}/{YYMMDD}-{日本語タイトル}.md`)

→ Proceed to Step 2

#### Output

- Branch document path confirmed

---

### Step 2: Parse unresolved QA items

#### Condition

- Step 1 complete

#### Process

1. Read the branch document and locate its `## QA` section
2. Extract all `### QA-XXX` subsections where the **状態** line does NOT contain「解決済み」or「却下」
3. If no unresolved items exist → report "QAに未決定事項はありません" and finish
4. Build a list: each item has its ID, title, and a body summary

→ Proceed to Step 3

#### Output

- List of unresolved QA items

---

### Step 3: Present items in batches

#### Condition

- Step 2 complete (at least one unresolved item)

#### Process

Batch unresolved items into groups of up to 4 (the `AskUserQuestion` maximum) and present each batch in a single call:

1. Split unresolved items into batches of at most 4 (fewer if less remain)
2. For each batch, make one `AskUserQuestion` call:
   - Each QA item becomes one **question** entry (up to 4 per call)
   - **question**: The QA item's title plus a concise 1–2 sentence summary of the decision needed
   - **header**: The QA item ID (e.g. `QA-001`)
   - **options** (same for each question):
     - `解決済み（採用）` — A decision has been made
     - `保留（後で判断）` — Skip for now
     - `却下（対応しない）` — Won't fix
   - **multiSelect**: false
3. Repeat for the next batch until all items are presented

→ Proceed to Step 4

#### Notes

- If the item body is long, summarize to the essential question in the `question` field
- Answers are retained in the prompt history, so no intermediate document update is needed between batches

---

### Step 4: Update the branch document's `## QA` section with all decisions at once

#### Condition

- Step 3 complete (all batches answered)

#### Process

1. Apply all responses collected in Step 3 to the branch document's `## QA` section in a single pass:
   - Resolved: `**状態**: 解決済み — {decision note or free-text input}`
   - Closed: `**状態**: 却下 — {reason or free-text input}`
   - On hold: leave the line unchanged
2. Write the updated branch document

→ Proceed to Step 5

---

### Step 5: Report summary

#### Condition

- Step 4 complete

#### Process

1. Output a summary table:

   | QA ID | 状態 |
   |---|---|
   | QA-001 | 解決済み |
   | QA-002 | 保留 |

2. If all items are now resolved → "すべての QA が解決しました。実装を進められます。"
3. If unresolved items remain → state how many are still pending

→ Done
