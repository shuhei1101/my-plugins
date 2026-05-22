---
name: skill-creator
description: |
  Create a new Claude Code skill under .claude/skills/ using the step-based structure.
  Trigger when the user says "スキルを作りたい", "新しいスキル作って", "create a skill", "make a skill for X", or claude-kit dispatches here.
---

# skill-creator — New Skill Scaffold

Creates a skill in the step-based structure.
A skill is an on-demand workflow — invoked explicitly or auto-triggered via `description` frontmatter.

---

## Overview

Skill files live at `.claude/skills/<name>/SKILL.md`.
Paired with a JP mirror at `.claude/skills/<name>/SKILL.jp.md`.

The `description` frontmatter is the auto-trigger — write it precisely to control when the skill fires.

---

## Tasks

### Step 0: Read background materials

#### Condition

- Always — before doing anything else

#### Process

1. Read the official Claude Code documentation on skills:
   **https://code.claude.com/docs/en/skills**

2. Read the common guide (`references/common.md`) and the skills design guide (`references/skills.md`) in this plugin.
   `common.md` contains: file type decision criteria and JP/EN mirror rules.
   `skills.md` contains: when to use skills, `description` frontmatter, step structure, reference placement.

→ Proceed to Step 1

---

### Step 1: Gather skill information

#### Condition

- User wants to create a new skill

#### Input

- User's description of what the skill should do

#### Process

1. Ask for:
   - **Skill name** — kebab-case identifier (e.g. `pr-pick`, `topic-generate`, `notify`)
   - **Trigger conditions** — when should this skill auto-fire? Be specific: "when the user says X", "when editing Y file", "when Z condition is met"
   - **What it does** — the workflow steps at a high level

2. Map the workflow into steps using the structure:
   - Each step has: Condition, Input, Process, Output, Notes

#### Output

- Skill name, trigger description, step list

---

### Step 2: Validate gathered information

#### Condition

- Step 1 complete

#### Input

- Skill description and workflow collected in Step 1
- File-type guide (`references/file-types.md` in this plugin)

#### Process

1. Check whether `.claude/skills/` is truly the right choice:

   | If the content is… | Suggest |
   |---|---|
   | Multi-step workflow with user interaction or branching | ✅ Skill — correct choice |
   | Repeated routine that needs user confirmation points | ✅ Skill — correct choice |
   | 1-2 simple rules or conventions | ⚠️ CLAUDE.md or `.claude/rules/` is simpler |
   | Cross-path file sync ("edit X → also update Y, Z") | ⚠️ `.claude/rules/` is more appropriate |
   | Mix of workflow + sync rules | ⚠️ Consider splitting: skill for the workflow, rules for the sync |

2. If skill is the right fit → confirm and proceed
3. If another file type fits better → explain why and offer to redirect

→ Proceed to Step 3 if skill is confirmed appropriate

#### Output

- Confirmed: the content is a multi-step workflow appropriate for a skill

#### Notes

##### Branching

- Simple rule → explain and offer to create in CLAUDE.md or rules instead
- Primarily file-sync → offer to switch to `rule-creator`
- Mixed → suggest splitting and confirm scope of what the skill will cover

---

### Step 3: Check for similar existing skills

#### Condition

- Step 2 complete (skill confirmed appropriate)

#### Input

- Skill description and workflow from Step 1
- Existing skills in `.claude/skills/`

#### Process

1. Glob `.claude/skills/**/SKILL.md` and read the `description` and overview of each
2. Check whether any existing skill has overlapping triggers or similar workflow steps
3. If overlap or similarity found:
   - Explain the overlap to the user
   - Propose options:
     - **Merge**: extend the existing skill to cover this use case too
     - **Keep separate**: explain the clear boundary that justifies splitting (e.g., different trigger conditions, distinct user flows)
   - Let the user decide before proceeding
4. If no overlap → proceed directly

→ Proceed to Step 4

#### Output

- Confirmed approach: new skill, merge with existing, or justified separation

#### Notes

##### Branching

- User chooses to merge → apply changes to the existing skill instead of creating new files → skip to Step 6 (final verification)

---

### Step 4: Write the JP mirror first (`SKILL.jp.md`)

#### Condition

- Step 3 complete (skill confirmed appropriate, no blocking similarity)

#### Input

- Skill name, trigger conditions, step list

#### Process

1. Create `.claude/skills/<name>/SKILL.jp.md` using this structure:

   ```markdown
   ---
   name: <スキル名>
   description: |
     このスキルが自動起動する条件を具体的に書く。
     例: ユーザーが「〜したい」「〜して」と言ったとき。
   ---

   # <スキル名> — 概要一行

   <このスキルが何をするかを1〜2文で>

   ---

   ## 概要

   <背景・目的・このスキルが存在する理由>

   ---

   ## 作業内容

   ### ステップN: <アクション名>

   #### 条件
   （前提条件）

   #### 入力
   （データ・ファイル・ユーザー入力）

   #### 処理内容
   1. 具体的にやること
   → ステップN+1へ進む

   #### 出力
   （このステップが完了した状態）

   #### 補足
   （必要なサブセクションだけ使う）

   ##### チェックリスト / 条件分岐 / 参照ドキュメント

   ---

   ## 参考資料
   （複数ステップから参照される共通の表・定義・リンク集のみ。
     単一ステップのみで使う内容はそのステップに書く。）
   ```

   `description` frontmatter format:
   ```yaml
   ---
   name: {skill-name}
   description: |
     Precise trigger conditions.
     "When the user says X", "when editing Y".
   ---
   ```
   Only `name` and `description` are needed. Do not add `allowed-tools`.
   Do not use `disable-model-invocation: true` by default — only for skills that must never be AI-invoked (merge, deploy, destructive ops).

2. Write `description` frontmatter with precise trigger conditions
3. Put shared content in `## 参考資料` **only if used by multiple steps** — content used by a single step belongs inside that step

→ Proceed to Step 5

#### Output

- `SKILL.jp.md` created

#### Notes

##### Prohibitions

- Do not write vague `description` — auto-trigger accuracy depends on it
- Do not write in English (this is the human-readable Japanese reference)
- Do not put single-step-only content in `## 参考資料` — keep it inside the step

---

### Step 5: Translate to the English skill (`SKILL.md`)

#### Condition

- JP mirror created

#### Input

- JP mirror content

#### Process

1. Translate to English, keeping the same structure as SKILL.jp.md:

   ```markdown
   ---
   name: <skill-name>
   description: |
     Precise trigger conditions in English.
     "When the user says X", "when editing Y", "when Z".
   ---

   # <Skill Name> — One-line summary

   <What this skill does in 1-2 sentences>

   ---

   ## Overview

   <Background, purpose, why this skill exists>

   ---

   ## Tasks

   ### Step N: <Action name>

   #### Condition
   (Preconditions)

   #### Input
   (Data, files, user input)

   #### Process
   1. Concrete action
   → Proceed to Step N+1

   #### Output
   (What exists as a result of this step)

   #### Notes
   (Use only the subsections you need)

   ##### Checklist / Branching / References

   ---

   ## References
   (Shared tables, definitions, or links used across multiple steps only.
    Content used by a single step belongs inside that step.)
   ```

→ Proceed to Step 6

#### Output

- `SKILL.md` created

---

### Step 6: Final verification

#### Condition

- Both SKILL.md and SKILL.jp.md created

#### Process

1. Confirm both files exist with matching structure
2. Present result to the user for review

#### Output

- User can review both files before committing

#### Notes

##### Checklist

- [ ] `.claude/skills/<name>/SKILL.md` — English, Claude Code reads this
- [ ] `.claude/skills/<name>/SKILL.jp.md` — Japanese mirror, human reference
- [ ] Both files have matching heading structure
- [ ] `description` frontmatter has precise trigger conditions

