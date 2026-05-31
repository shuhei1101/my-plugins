<!-- This file is a Japanese mirror of SKILL.md. Do not edit directly — update SKILL.md first, then sync here. -->

---
name: setup-wizard
description: |
  `SessionStart` でトリガー（`setup_done` 未設定時にフックが自動起動）するか、
  ユーザーが `/ref-inject:setup-wizard` を明示的に呼び出したとき。
  ref-inject プラグインのユースケースを紹介し、セットアップ完了をマークする。
  このスキル内では AskUserQuestion の使用が明示的に許可されている。
---

# ref-inject:setup-wizard — 初回オンボーディング

ref-inject プラグインの初回オンボーディングを行うスキル。
ref-inject の主要なユースケースを紹介してからセットアップ完了をマークする。

ref-inject はユーザー向けの env トグルを持たないため、env 設定ステップはスキップする。

AskUserQuestion はこのスキル内で使用する（明示的に許可済み）。

---

## Tasks

### Step 1: 既存のセットアップ状態を確認する

#### 条件

- 常時 — 最初に実行する

#### 処理

1. `.claude/ref-inject.local.md` の YAML frontmatter を読み込む
2. `setup_done: true` が存在する場合 → `AskUserQuestion` で確認する:
   - `再実行する` — Step 2 に進む
   - `中断する` — ここで終了
3. false または存在しない場合 → Step 2 に進む

→ Step 2 へ

---

### Step 2: ユースケース紹介

#### 条件

- Step 1 完了

#### 処理

1. `AskUserQuestion` で質問する（`multiSelect: true`）:

   **質問**: "ref-inject をどのような場面で使いますか？（複数選択可）"

   | オプション | 説明 |
   |---|---|
   | 新規プラグインへの注入機能追加 | `/ref-inject:apply` で新規プラグインに参照注入機能を追加する |
   | 既存プラグインへの注入機能追加 | `/ref-inject:apply` で既存プラグインに参照注入機能を後付けする |
   | 注入ファイルの更新 | `/ref-inject:plugin-migrate` で全消費者の注入ファイルを最新テンプレートに同期する |

2. 選択された各ユースケースについて 3〜5 行で説明し、対応するスキルドキュメントへのリンクを案内する

→ Step 3 へ

---

### Step 3: セットアップ完了をマークする

#### 条件

- Step 2 完了

#### 処理

1. `.claude/ref-inject.local.md` に `setup_done: true` を YAML frontmatter に書き込む（または更新する）:

   ```markdown
   ---
   setup_done: true
   ---

   # ref-inject setup notes

   (ここに自由にメモを追記できます)
   ```

2. ユーザーに伝える:
   - セットアップが完了した
   - `/ref-inject:setup-wizard` でいつでも再実行できる
