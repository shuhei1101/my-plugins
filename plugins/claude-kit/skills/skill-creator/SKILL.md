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

2. Read the file-type usage reference (`references/file-types.md` in this plugin).
   Key points:

   **Skills are for**: Multi-step workflows and procedures that involve user interaction
   or complex decision-making across multiple steps.

   **Skills vs other file types**:
   - Use a skill when the task has 3+ steps, involves user confirmation points, or needs
     branching logic — not for simple 1-2 line rules
   - Simple rules → CLAUDE.md or `.claude/rules/`
   - File-edit-triggered sync reminders → `.claude/rules/`

   **`description` frontmatter**: This is the auto-trigger. Write it precisely —
   "when the user says X", "when editing Y file". Vague descriptions cause false positives.

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

1. Create `.claude/skills/<name>/SKILL.jp.md`:

```markdown
---
name: <スキル名>
description: |
  このスキルが自動起動する条件を具体的に書く。
  例: ユーザーが「〜したい」「〜して」と言ったとき。
  または `/skill-name` で明示的に呼ばれたとき。
---

# <スキル名> — 概要一行

<このスキルが何をするかを1〜2文で>

---

## 概要

<背景・目的・このスキルが存在する理由>

---

## 作業内容

### ステップ1: <最初にやること>

#### 条件

- このステップに進む条件

#### 入力

- このステップで使うデータ・ファイル・ユーザー入力

#### 処理内容

1. 具体的にやること
2. コマンドがあれば記載
   ```bash
   command here
   ```

→ ステップ2へ進む（または <条件> の場合はステップNへ）

#### 出力

- このステップの結果として何が存在するか

#### 補足

##### 禁止事項

- やってはいけないこと（あれば）

##### 条件分岐

- もし〜なら → ステップNへ

##### 参照ドキュメント

- 関連ファイルへのリンク（あれば）

##### チェックリスト

- [ ] 確認項目（あれば）

---

### ステップ2: <次にやること>

(同じ構造で続ける)

---

## 参考資料

### <共通資料の見出し>

複数ステップから参照される表・定義など
```

#### Output

- `SKILL.jp.md` created

---

### Step 5: Translate to the English skill (`SKILL.md`)

#### Condition

- JP mirror created

#### Input

- JP mirror content

#### Process

1. Translate to English, keeping the same structure:

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

### Step 1: <First action>

#### Condition

- When to enter this step

#### Input

- Data, files, or user input used in this step

#### Process

1. Concrete action
2. Include commands if applicable
   ```bash
   command here
   ```

→ Proceed to Step 2 (or Step N if <condition>)

#### Output

- What exists as a result of this step

#### Notes

##### Prohibitions

- What not to do (if any)

##### Branching

- If X → go to Step N
- If Y → stop and ask the user

##### References

- Links to related files (if any)

##### Checklist

- [ ] Verification item (if any)

---

### Step 2: <Next action>

(same structure continues)

---

## References

### <Shared resource heading>

Tables or definitions referenced by multiple steps
```

#### Output

- `SKILL.md` created

#### Notes


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

---

## References

### Step-based structure for skill files

Each section follows this pattern:

```markdown
---
name: <skill-name>
description: |
  Precise trigger conditions in English.
  "When the user says X", "when editing Y", "when Z".
---

# Skill Name — One-line summary

What this skill does in 1-2 sentences.

---

## Overview

Background, purpose, why this skill exists.

---

## Tasks

### Step N: (Action name)

#### Condition
(Preconditions to enter this step. Stop or branch if not met.)

#### Input
(Data, files, prior step output, or user input used in this step)

#### Process
(Numbered list of concrete actions. Include commands if applicable.)
1. Do X
→ Proceed to Step N+1 (or → Step N if <condition>)

#### Output
(What exists as a result of completing this step)

#### Notes
(Use only the subsections you need)

##### Checklist
- [ ] Item is done

##### Branching
("If X → go to Step N", "If Y → stop and ask the user")

##### References
(Files, URLs, or §References entries used in this step)

---

## References
(Shared tables, definitions, or reference material used across multiple steps)
```

### Frontmatter basics

```yaml
---
name: {skill-name}
description: |
  Precise trigger conditions in English.
  "When the user says X", "when editing Y", "when Z".
---
```

Only `name` and `description` are needed. Do not add `allowed-tools`.

Do not use `disable-model-invocation: true` by default. **Exception**: add it for skills that must only be run by a human explicitly — merge, deploy, destructive operations — where AI self-invocation is unacceptable.

### Official docs

- Skills: **https://code.claude.com/docs/en/skills**
