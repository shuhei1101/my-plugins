---
name: rules-creator
description: |
  Create a new path-scoped rule under .claude/rules/ using the step-based structure.
  Trigger when the user says "新しいルール作って", "ルールを新規作成", "make a rule for X", or claude-kit dispatches here.
---

# rules-creator — New Rule Scaffold

Creates a path-scoped rule in the step-based structure.
A rule groups related files into a domain and ensures they stay in sync.

---

## Overview

A domain rule answers: "which files belong together, and what must happen when any of them changes?"

Example — "models" domain:
- Config: `config/models.yaml`
- Source: `src/models/*.py`
- Docs: `docs/specs/models.md`

When you edit any one of these, the rule reminds you to check the others.

---

## Tasks

### Step 1: Check existing coverage

#### Condition

- Before creating any new rule file

#### Input

- The domain or folder the user wants to cover

#### Process

1. Glob `.claude/rules/**/*.md` and scan `paths:` patterns
2. If an existing rule already covers the target files, offer to extend it instead
3. Only proceed with a new file if no existing rule covers this domain

#### Output

- Confirmed: no existing rule covers this domain

#### Notes

##### Branching

- Existing rule found → offer to extend it → skip to Step 4 if user agrees to extend

---

### Step 2: Gather domain information

#### Condition

- No existing rule covers this domain

#### Input

- User's description of the domain

#### Process

1. Ask for:
   - **Domain name** — short kebab-case identifier (e.g. `models`, `voice`, `assets-bgm`)
   - **Files in this domain** — help the user think in three categories:
     - Config / schema (YAML, JSON, constants)
     - Source code (implementation files)
     - Docs (spec files, architecture docs)
   - **One-line description** — what this domain does and why these files must stay in sync

2. If the user describes a scenario ("when I add X I need to update Y, Z"), extract the files from that description without asking redundant questions

#### Output

- Domain name, file list, one-line description

---

### Step 3: Write the JP mirror first (`.claude/rules-jp/<name>.md`)

#### Condition

- Domain information gathered

#### Input

- Domain name, file list, description

#### Process

1. Create `.claude/rules-jp/<name>.md` with this structure:

```markdown
---
paths:
  - "<config/schema glob>"
  - "<source glob>"
  - "<docs glob>"
---

> ⚠️ **日本語ミラー** — Claude には読み込まれません。このファイルを更新したときは英語オリジナル `.claude/rules/<name>.md` を必ず同時に更新してください。

# <ドメイン名> ルール

## 概要

<1〜2文でこのドメインが何を管理するか>

## 作業内容

### ステップ1: 編集前の確認

#### 条件

- このドメインのいずれかのファイルを編集するとき

#### 処理内容

1. 下記「参考資料」の対応表でファイルの役割を確認する
2. `docs/qa.md` に関連する未決定イシューがないか確認する

#### 補足

##### 参照ドキュメント

- → 参考資料 §対応表 を参照

---

### ステップ2: 編集する

#### 条件

- ステップ1の確認が完了していること

#### 処理内容

1. ファイルを編集する
2. 影響を受ける他のファイルをすべて更新する（対応表を参照）
3. このルール自体も変更が必要なら更新する

→ ステップ3へ進む

#### 補足

##### 禁止事項

- 1ファイルだけ更新して他は「後で」と先送りにしない

---

### ステップ3: 動作確認・コミット

#### 処理内容

1. 変更したファイル一覧を確認する
2. コミットする

#### 補足

##### チェックリスト

- [ ] 対応表のすべての関連ファイルを確認した
- [ ] JPミラーも更新した（ルール自体を変更した場合）

---

## 参考資料

### 対応表

このドメインのいずれかのファイルを編集するときは、以下を確認・更新すること:

| ファイル / パターン | 役割 | いつ更新するか |
|---|---|---|
| `<config file>` | 設定の正規ソース | 値・フィールド・エントリを追加・変更・削除したとき |
| `src/<domain>/` | 実装コード | 設定に合わせて挙動を変更するとき |
| `docs/specs/<doc>.md` | 設計ドキュメント | 構造・挙動が変わるとき |
| `.claude/rules/<name>.md` | このルール自体 | ドメインのファイルが増減したとき |
```

#### Output

- `.claude/rules-jp/<name>.md` created

---

### Step 4: Translate to the English rule (`.claude/rules/<name>.md`)

#### Condition

- JP mirror created

#### Input

- JP mirror content

#### Process

1. Translate the JP mirror to English
2. Create `.claude/rules/<name>.md` with this structure:

```markdown
---
paths:
  - "<config/schema glob>"
  - "<source glob>"
  - "<docs glob>"
---

# <Domain> Rule

## Overview

<1-2 sentence description>

## Tasks

### Step 1: Pre-edit check

#### Condition

- When editing any file in this domain

#### Process

1. Check the cross-reference table in §References to understand each file's role
2. Check `docs/qa.md` for open issues related to this domain

#### Notes

##### References

- → See References §Cross-reference table

---

### Step 2: Edit

#### Condition

- Step 1 check complete

#### Process

1. Edit the target file
2. Update all affected files listed in the cross-reference table
3. Update this rule itself if the domain's file list has changed

→ Proceed to Step 3

#### Notes

##### Prohibitions

- Do not update one file and defer the rest — do them all in the same PR/commit

---

### Step 3: Verify and commit

#### Process

1. Review the list of changed files
2. Commit

#### Notes

##### Checklist

- [ ] Checked all related files in the cross-reference table
- [ ] Updated the JP mirror if the rule itself changed

---

## References

### Cross-reference table

When editing any file in this domain, check and update ALL of the following:

| File / Pattern | Role | Update when |
|---|---|---|
| `<config file>` | Canonical config source | A value, field, or entry is added / renamed / removed |
| `src/<domain>/` | Implementation | Behavior must reflect the config change |
| `docs/specs/<doc>.md` | Design doc | Structure or behavior changes |
| `.claude/rules/<name>.md` | This rule | Domain files are added or removed |
```

#### Output

- `.claude/rules/<name>.md` created

---

### Step 5: Update `CLAUDE.md` and commit

#### Condition

- Both rule files created

#### Process

1. If the project's `CLAUDE.md` has a `Folder-scoped rules` table, append:
   ```
   | `<name>.md` | `<path-pattern>` — <domain description> |
   ```
2. Also update `CLAUDE.jp.md` if it has a matching table
3. Commit all four files together: EN rule + JP mirror + CLAUDE.md + CLAUDE.jp.md

→ Done

#### Notes

##### Checklist

- [ ] `.claude/rules/<name>.md` — English rule
- [ ] `.claude/rules-jp/<name>.md` — Japanese mirror
- [ ] `CLAUDE.md` — updated (if table present)
- [ ] `CLAUDE.jp.md` — updated (if updated CLAUDE.md)

Commit message: `docs(rules): <name> ルール追加`
