---
name: claude-creator
description: |
  Create or overhaul a CLAUDE.md (and its CLAUDE.jp.md mirror) for a project.
  Trigger when the user says "CLAUDE.md を作って", "CLAUDE.md を書いて", "create a CLAUDE.md",
  "クロードのガイドを作りたい", or asks to set up Claude Code instructions for a project.
---

# claude-creator — CLAUDE.md Authoring

Creates a CLAUDE.md and its paired CLAUDE.jp.md mirror for a project.

---

## Overview

CLAUDE.md is the top-level instruction file that Claude Code loads at the start of every session.
It defines the project workflow, commit rules, server management, and folder-scoped rule table.

---

## Tasks

### Step 0: Read the official docs

#### Condition

- Always — before doing anything else

#### Process

1. Read the official Claude Code documentation on CLAUDE.md:
   **https://code.claude.com/docs/en/memory**
2. Confirm understanding of CLAUDE.md placement, scope, and loading behavior before writing

→ Proceed to Step 1

---

### Step 1: Gather project information

#### Condition

- Step 0 complete

#### Input

- User's description of the project

#### Process

1. Ask the user for:
   - **Project name and overview** — one-line description of what this project does
   - **Workflow steps** — walk through each phase:
     - How does a new task start? (e.g., create worktree, create PR doc)
     - How is implementation done?
     - How is it verified? (e.g., start dev server, show URL)
     - How is it completed? (e.g., user confirms merge)
   - **Key prohibitions** — what must never happen
   - **Folder-scoped rules** — are there `.claude/rules/` files? List names and paths

2. Map each workflow phase into a numbered step

→ Proceed to Step 2

#### Output

- Project overview, workflow step list, prohibitions, rule table entries

---

### Step 2: Write CLAUDE.jp.md first

#### Condition

- Step 1 complete

#### Input

- Project info from Step 1

#### Process

1. Write `CLAUDE.jp.md` in Japanese using the step-based structure (see §References)
2. Put shared tables and cross-references in `## 参考資料` at the bottom
3. Keep the file under ~200 lines — if it grows too large, move domain-specific content to `.claude/rules/`

→ Proceed to Step 3

#### Output

- `CLAUDE.jp.md` written

#### Notes

##### Prohibitions

- Do not write the body in English — CLAUDE.jp.md is the Japanese human reference
- Do not exceed ~200 lines — split into path-scoped rules if needed

---

### Step 3: Translate to CLAUDE.md (English)

#### Condition

- CLAUDE.jp.md written

#### Input

- CLAUDE.jp.md content

#### Process

1. Translate line-by-line to English
2. Write `CLAUDE.md` — this is the file Claude Code actually reads as directives
3. Keep heading structure identical to CLAUDE.jp.md

→ Proceed to Step 4

#### Output

- `CLAUDE.md` written

#### Notes

##### Prohibitions

- Do not write the body in Japanese — CLAUDE.md is read by Claude as directives
- Keep heading structure and step numbering identical to CLAUDE.jp.md

---

### Step 4: Final verification

#### Condition

- Both CLAUDE.md and CLAUDE.jp.md written

#### Process

1. Check that both files exist and have matching structure
2. Confirm the file is under ~200 lines
3. Present the result to the user for review

#### Output

- User can review both files before committing

#### Notes

##### Checklist

- [ ] `CLAUDE.md` — English, will be auto-loaded by Claude Code
- [ ] `CLAUDE.jp.md` — Japanese mirror, human reference only
- [ ] Both files have matching heading structure
- [ ] File is under ~200 lines

---

## References

### Step-based structure for CLAUDE.md

Every section in CLAUDE.md follows this pattern:

```markdown
## 概要
(What this project does and how AI should work here — 1-3 sentences)

## 作業内容

### ステップN: (Action name)

#### 条件
(When to enter this step — preconditions that must be true. If not met, stop or branch.)

#### 入力
(Data, files, or context this step uses — from the user, previous steps, or existing files)

#### 処理内容
(Numbered list of concrete actions. Include commands if applicable.)
1. Do X
2. Do Y
   ```bash
   command here
   ```
→ Proceed to Step N+1 (or → Step N if <condition>)

#### 出力
(What exists as a result of completing this step — files created, server running, etc.)

#### 補足
(Optional. Use only the sub-sections that apply.)

##### 禁止事項
(Things that must never be done in this step — hard constraints)

##### 条件分岐
(Branching: "if X → go to Step N", "if Y → stop and ask the user")

##### 参照ドキュメント
(Files, URLs, or §References entries used in this step)

##### チェックリスト
(Items to verify before considering this step complete)

---

## 参考資料
(Shared tables, definitions, or reference material used across multiple steps.
Put cross-reference tables, schema definitions, and link lists here.)
```

### CLAUDE.md vs `.claude/rules/` — what goes where

| Content | Where |
|---|---|
| Applies every session, any file | `CLAUDE.md` |
| Project meta-workflow (worktree, commit, server) | `CLAUDE.md` |
| Applies only when editing a specific folder | `.claude/rules/<name>.md` with `paths:` |
| Domain-specific spec references | `.claude/rules/<name>.md` with `paths:` |

### Official docs

- CLAUDE.md structure and placement: **https://code.claude.com/docs/en/memory**
