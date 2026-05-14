---
name: rules-creator
description: |
  Create a new path-scoped rule under .claude/rules/ using the step-based structure.
  Trigger when the user says "新しいルール作って", "ルールを新規作成", "make a rule for X", or "create a rule for".
---

# rules-creator — Path-Scoped Rule Creator

Creates a new `.claude/rules/<name>.md` and its `.claude/rules-jp/<name>.md` mirror
using the step-based structure.

---

## Overview

A path-scoped rule groups related files into a domain and defines what must happen
when any of those files is read or edited. The rule loads automatically when Claude
reads a file matching the `paths:` pattern (not on shell-only commands like mv/rm).

---

## Tasks

### Step 0: Read background materials

#### Condition

- Always — before doing anything else

#### Process

1. Read the official Claude Code documentation on path-scoped rules:
   **https://code.claude.com/docs/en/memory**

2. Read the file-type usage reference (`references/file-types.md` in this plugin).
   Key points:

   **When rules load**: When Claude *reads* a matching file — NOT on shell-only commands (mv, rm)

   **What to put in rules (good)**:
   - Links to related files that must stay in sync when any one is edited
   - "When editing X, also check Y, Z (spec, test, config)"

   **What NOT to put in rules (bad)**:
   - Detailed documentation or descriptions of what a file does
   - Content that should be visible even when no matching file is being read
   - → Those belong in CLAUDE.md instead

→ Proceed to Step 1

---

### Step 1: Check existing coverage

#### Condition

- Always before creating a new rule file

#### Input

- The domain or folder the user wants to cover

#### Process

1. Glob `.claude/rules/**/*.md` and read each `paths:` pattern
2. Test whether the target files already match an existing rule
3. If covered: offer to extend the existing rule instead

→ Proceed to Step 2 only if no existing rule covers this domain

#### Output

- Confirmed: no existing rule covers this domain

#### Notes

##### Branching

- Existing rule covers the target → offer to extend it → if user agrees, skip to Step 4

---

### Step 2: Gather domain information

#### Condition

- No existing rule covers this domain

#### Input

- User's description of the domain

#### Process

1. Ask the user for:
   - **Domain name** — kebab-case identifier (e.g. `models`, `voice`, `assets-bgm`)
   - **Files in this domain** — help the user identify three categories:
     - Config / schema (YAML, JSON, constants that define the domain)
     - Source code (implementation files)
     - Docs (spec files, architecture docs)
   - **One-line description** — what this domain does and why these files must stay in sync
2. If the user describes a scenario, extract files from it without asking redundant questions

→ Proceed to Step 3

#### Output

- Domain name, file list (with globs), one-line description

---

### Step 3: Validate against file-type guide

#### Condition

- Step 2 complete

#### Input

- Domain file list collected in Step 2
- File-type guide (`references/file-types.md` in this plugin)

#### Process

1. Check whether `.claude/rules/` is truly the right choice:

   | If the files are… | Suggest |
   |---|---|
   | Spread across multiple different folders | ✅ Rules — correct choice for cross-path linking |
   | All within a single folder | ⚠️ CLAUDE.md (subfolder) may be simpler and clearer |
   | About a workflow or procedure | ⚠️ `.claude/skills/` may be more appropriate |
   | A mix | ⚠️ Consider splitting: rules for cross-path, CLAUDE.md for folder-local |

2. If rules is the right fit → confirm and proceed
3. If another file type fits better → explain the reasoning and offer to redirect

→ Proceed to Step 4 if rules is confirmed appropriate

#### Output

- Confirmed: the domain spans multiple paths and rules is appropriate

#### Notes

##### Branching

- All files in one folder → explain and offer to use a subfolder CLAUDE.md instead
- It's a workflow → offer to switch to `skill-creator`

---

### Step 4: Write the JP mirror first (`.claude/rules-jp/<name>.md`)

#### Condition

- Domain information gathered

#### Input

- Domain name, file list, description from Step 2

#### Process

1. Create `.claude/rules-jp/<name>.md` using the step-based structure (see §References)
2. Add the required JP mirror header at the top (after frontmatter, before H1)
3. Put the cross-reference table in `## 参考資料` at the bottom

→ Proceed to Step 5

#### Output

- \.claude/rules-jp/<name>.md` created

#### Notes

##### Prohibitions

- Do not write the body in English — this is the Japanese human reference
- Do not place this file inside `.claude/rules/` — use `.claude/rules-jp/` (the rules directory is scanned recursively and would auto-load the file)

---

### Step 5: Translate to the English rule (`.claude/rules/<name>.md`)

#### Condition

- JP mirror created

#### Input

- JP mirror content from Step 4

#### Process

1. Translate line-by-line to English
2. Create `.claude/rules/<name>.md` with the same step-based structure
3. Keep heading structure identical to the JP mirror

→ Proceed to Step 6

#### Output

- `.claude/rules/<name>.md` created

#### Notes

##### Prohibitions

- Do not write the body in Japanese — this file is auto-loaded by Claude as directives
- Keep heading structure and step numbering identical to the JP mirror

---

### Step 6: Final verification

#### Condition

- All files created

#### Process

1. Confirm all files exist with matching structure
2. Present the result to the user for review

#### Output

- User can review all files before committing

#### Notes

##### Checklist

- [ ] `.claude/rules/<name>.md` — English, auto-loaded on path match
- [ ] `.claude/rules-jp/<name>.md` — Japanese mirror with required header

---

## References

### Step-based structure for rule files

```markdown
---
paths:
  - "<glob pattern covering the domain>"
---

> ⚠️ **日本語ミラー** — Claude には読み込まれません。このファイルを更新したときは英語オリジナル `.claude/rules/<name>.md` を必ず同時に更新してください。

# (Rule title in Japanese)

## 概要
(What this rule governs — 1-2 sentences)

## 作業内容

### ステップN: (Action name)

#### 条件
(Preconditions to enter this step)

#### 入力
(Data, files, or context used in this step)

#### 処理内容
(Numbered list of actions. Include commands if applicable.)
1. Do X
→ Proceed to Step N+1

#### 出力
(What exists as a result of this step)

#### 補足

##### 禁止事項
(Hard constraints — what must never be done)

##### 条件分岐
("If X → go to Step N", "If Y → stop and ask the user")

##### 参照ドキュメント
(Files, URLs, or §References entries used in this step)

##### チェックリスト
(Items to verify before considering this step complete)

---

## 参考資料

### 対応表
(Cross-reference table — which files must be checked when any domain file changes)

| File / Pattern | Role | Update when |
|---|---|---|
| `<config>` | Config source | Values added / changed / removed |
| `src/<domain>/` | Implementation | Behavior must reflect config |
| `docs/specs/<doc>.md` | Design doc | Structure or behavior changes |
| `.claude/rules/<name>.md` | This rule | Domain files are added or removed |
```

### Official docs

- Path-scoped rules: **https://code.claude.com/docs/en/memory**
