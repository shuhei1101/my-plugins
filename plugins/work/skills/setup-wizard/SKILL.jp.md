<!-- This file is a Japanese mirror of SKILL.md. Do not edit directly — update SKILL.md first, then sync here. -->

---
name: setup-wizard
description: |
  `SessionStart` でトリガー（`setup_done` 未設定時にフックが自動起動）するか、
  ユーザーが `/work:setup-wizard` を明示的に呼び出したとき。
  work プラグインの env 設定とユースケース紹介を行い、セットアップ完了をマークする。
  このスキル内では AskUserQuestion の使用が明示的に許可されている。
---

# work:setup-wizard — 初回オンボーディング

work プラグインの初回オンボーディングを行うスキル。
env トグルの設定とキーワークフローの紹介を案内し、セットアップ完了をマークする。

AskUserQuestion はこのスキル内で使用する（明示的に許可済み）。

---

## Tasks

### Step 1: 既存のセットアップ状態を確認する

#### 条件

- 常時 — 最初に実行する

#### 処理

1. `.claude/work.local.md` の YAML frontmatter を読み込む
2. `setup_done: true` が存在する場合 → `AskUserQuestion` で確認する:
   - `再実行する` — Step 2 に進む
   - `中断する` — ここで終了
3. false または存在しない場合 → Step 2 に進む

→ Step 2 へ

---

### Step 2: env 設定 — plugin-config に委任する

#### 条件

- Step 1 完了

#### 処理

1. `AskUserQuestion` で質問する:

   **質問**: "work プラグインの env 設定を行いますか？"

   | オプション | アクション |
   |---|---|
   | すべて設定する（`/work:plugin-config` を起動） | `/work:plugin-config` を呼び出してすべてのトグルを設定する |
   | スキップ（あとで設定する） | スキップ; あとから `/work:plugin-config` を実行できることを伝える |

2. 選択されたアクションを実行する

→ Step 3 へ

---

### Step 3: ユースケース紹介

#### 条件

- Step 2 完了

#### 処理

1. `AskUserQuestion` で質問する（`multiSelect: true`）:

   **質問**: "work プラグインをどのような用途で使いますか？（複数選択可）"

   | オプション | 説明 |
   |---|---|
   | ブランチ・タスク管理 | `/work:start` でブランチを切り、`.work/tasks/` でタスクを管理する |
   | マージワークフロー | `/work:merge` でレビュー・QA・マージを一連の流れで実施する |
   | イシュー管理 | `/work:issue-scan` でコード上の問題を自動検出し `.work/issues/` に記録する |
   | ワークスペース設定 | `WORK_*` env トグルを `/work:plugin-config` で設定する |

2. 選択された各ユースケースについて 3〜5 行で説明し、対応するスキルドキュメントへのリンクを案内する

→ Step 4 へ

---

### Step 4: セットアップ完了をマークする

#### 条件

- Step 3 完了

#### 処理

1. `.claude/work.local.md` に `setup_done: true` を YAML frontmatter に書き込む（または更新する）:

   ```markdown
   ---
   setup_done: true
   ---

   # work setup notes

   (ここに自由にメモを追記できます)
   ```

2. ユーザーに伝える:
   - セットアップが完了した
   - `/work:setup-wizard` でいつでも再実行できる
   - env トグルは `/work:plugin-config` でいつでも変更できる
