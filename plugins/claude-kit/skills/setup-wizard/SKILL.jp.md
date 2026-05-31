<!-- This file is a Japanese mirror of SKILL.md. Do not edit directly — update SKILL.md first, then sync here. -->

---
name: setup-wizard
description: |
  `SessionStart` でトリガー（`setup_done` 未設定時にフックが自動起動）するか、
  ユーザーが `/claude-kit:setup-wizard` を明示的に呼び出したとき。
  claude-kit プラグインの JP ミラー・注入言語等の設定を案内し、セットアップ完了をマークする。
  このスキル内では AskUserQuestion の使用が明示的に許可されている。
---

# claude-kit:setup-wizard — 初回オンボーディング

claude-kit プラグインの初回オンボーディングを行うスキル。
JP ミラー作成フラグや注入言語などの env 設定を案内し、
主要ユースケースを紹介してからセットアップ完了をマークする。

AskUserQuestion はこのスキル内で使用する（明示的に許可済み）。

---

## Tasks

### Step 1: 既存のセットアップ状態を確認する

#### 条件

- 常時 — 最初に実行する

#### 処理

1. `.claude/claude-kit.local.md` の YAML frontmatter を読み込む
2. `setup_done: true` が存在する場合 → `AskUserQuestion` で確認する:
   - `再実行する` — Step 2 に進む
   - `中断する` — ここで終了
3. false または存在しない場合 → Step 2 に進む

→ Step 2 へ

---

### Step 2: env 設定 — config スキルに委任する

#### 条件

- Step 1 完了

#### 処理

1. `AskUserQuestion` で質問する:

   **質問**: "claude-kit の env 設定を行いますか？（JP ミラー作成・注入言語など）"

   | オプション | アクション |
   |---|---|
   | すべて設定する（`/claude-kit:config` を起動） | `/claude-kit:config` を呼び出してすべての変数を設定する |
   | スキップ（あとで設定する） | スキップ; あとから `/claude-kit:config` を実行できることを伝える |

2. 選択されたアクションを実行する

→ Step 3 へ

---

### Step 3: ユースケース紹介

#### 条件

- Step 2 完了

#### 処理

1. `AskUserQuestion` で質問する（`multiSelect: true`）:

   **質問**: "claude-kit をどのような用途で使いますか？（複数選択可）"

   | オプション | 説明 |
   |---|---|
   | スキル・ルール作成 | `/claude-kit:skill-creator` や `/claude-kit:rule-creator` でスキル・ルールを作成する |
   | フック作成 | `/claude-kit:hook-creator` でプロンプト注入フックを作成する |
   | プラグイン作成 | `/claude-kit:plugin-creator` で新しいプラグインを作成する |
   | env 設定管理 | `/claude-kit:config` で JP ミラー・注入言語などの env 変数を管理する |

2. 選択された各ユースケースについて 3〜5 行で説明し、対応するスキルのドキュメントへのリンクを案内する

→ Step 4 へ

---

### Step 4: セットアップ完了をマークする

#### 条件

- Step 3 完了

#### 処理

1. `.claude/claude-kit.local.md` に `setup_done: true` を YAML frontmatter に書き込む（または更新する）:

   ```markdown
   ---
   setup_done: true
   ---

   # claude-kit setup notes

   (ここに自由にメモを追記できます)
   ```

2. ユーザーに伝える:
   - セットアップが完了した
   - `/claude-kit:setup-wizard` でいつでも再実行できる
   - env 設定は `/claude-kit:config` でいつでも変更できる
