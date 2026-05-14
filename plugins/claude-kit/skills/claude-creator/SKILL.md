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

Structure to produce:

```
## 概要          (Overview — what this project does and how AI should work here)
## 作業内容      (Tasks — step-by-step workflow)
  ### ステップN
    #### 条件
    #### 入力
    #### 処理内容
    #### 出力
    #### 補足
      ##### 禁止事項
      ##### 条件分岐
      ##### 参照ドキュメント
      ##### チェックリスト
## 参考資料      (References — shared tables / definitions used across steps)
```

---

## Tasks

### Step 1: Gather project information

#### Condition

- User wants to create or overhaul a CLAUDE.md

#### Input

- User's description of the project

#### Process

1. Ask the user for:
   - **Project name** — one-line description of what the project is
   - **Workflow steps** — what does AI do in this project? Walk through:
     - How does a new task start? (e.g., create worktree, create PR doc)
     - How is implementation done?
     - How is it verified?
     - How is it merged / completed?
   - **Key prohibitions** — what must never happen? (e.g., "never merge without user confirmation")
   - **Folder-scoped rules** — are there `.claude/rules/` files? List them for the table

2. Map each workflow phase into a step using this pattern:
   - Step name = the action being taken (e.g., "設計・PR ドキュメント作成")
   - Each step has: 条件, 入力, 処理内容, 出力, 補足

→ Proceed to Step 2

#### Output

- Project name, list of workflow steps, prohibitions, rule table entries

---

### Step 2: Write CLAUDE.jp.md first

#### Condition

- Step 1 complete

#### Input

- Project info from Step 1

#### Process

1. Write `CLAUDE.jp.md` in Japanese using the structure above
2. Use `### ステップN:` headings with `#### 条件 / 入力 / 処理内容 / 出力 / 補足` under each
3. Put shared tables and cross-references in `## 参考資料` at the bottom
4. Keep the file under ~200 lines — move domain-specific content to `.claude/rules/` if it grows too large

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
2. Write `CLAUDE.md` — this is the file Claude Code actually reads
3. Use `### Step N:` headings with `#### Condition / Input / Process / Output / Notes` under each
4. Put shared tables in `## References` at the bottom

→ Proceed to Step 4

#### Output

- `CLAUDE.md` written

#### Notes

##### Prohibitions

- Do not write the body in Japanese — CLAUDE.md is read by Claude as directives
- Keep heading structure identical to CLAUDE.jp.md

---

### Step 4: Verify and commit

#### Condition

- Both CLAUDE.md and CLAUDE.jp.md written

#### Process

1. Confirm both files exist and structure matches
2. Commit both together

→ Done

#### Notes

##### Checklist

- [ ] `CLAUDE.md` — English, auto-loaded by Claude Code
- [ ] `CLAUDE.jp.md` — Japanese mirror, human reference
- [ ] Both committed in the same commit
- [ ] File is under ~200 lines

Commit message: `docs: CLAUDE.md 作成`

---

## References

### CLAUDE.md vs `.claude/rules/` — what goes where

| Content | Where |
|---|---|
| Applies every session, any file | `CLAUDE.md` |
| Project meta-workflow (worktree, commit, server) | `CLAUDE.md` |
| Applies only when editing a specific folder | `.claude/rules/<name>.md` with `paths:` |
| Domain-specific spec references | `.claude/rules/<name>.md` with `paths:` |

### Folder-scoped rule table (include in CLAUDE.md if rules exist)

```markdown
## Folder-scoped rules (`.claude/rules/`)

| Rule | Scope | Description |
|---|---|---|
| `<name>.md` | `src/**/*.py` | Python implementation conventions |
| `<name>.md` | `docs/specs/**/*.md` | Spec editing workflow |
```
