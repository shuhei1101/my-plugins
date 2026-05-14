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
   - **`disable-model-invocation`** — set to `true` if the skill should only fire on explicit `/skill-name` invocation, never auto-triggered

2. Map the workflow into steps using the structure:
   - Each step has: Condition, Input, Process, Output, Notes

#### Output

- Skill name, trigger description, step list

---

### Step 2: Write the JP mirror first (`SKILL.jp.md`)

#### Condition

- Step 1 complete

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

### Step 3: Translate to the English skill (`SKILL.md`)

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

##### Branching

- If `disable-model-invocation: true` needed → add it to the frontmatter (skill will only fire on explicit `/skill-name`, never auto-triggered)

---

### Step 4: Commit

#### Condition

- Both SKILL.md and SKILL.jp.md created

#### Process

1. Commit both files together

→ Done

#### Notes

##### Checklist

- [ ] `.claude/skills/<name>/SKILL.md` — English skill
- [ ] `.claude/skills/<name>/SKILL.jp.md` — Japanese mirror
- [ ] Both committed in the same commit

Commit message: `feat(skills): <name> スキル追加`
