<!-- This file is a Japanese mirror of SKILL.md. Do not edit directly — update SKILL.md first, then sync here. -->

---
name: setup-wizard
description: |
  `SessionStart` でトリガー（`setup_done` 未設定時にフックが自動起動）するか、
  ユーザーが `/dev-kit:setup-wizard` を明示的に呼び出したとき。
  dev-kit プラグインの言語 opt-in と機能トグルの設定を案内し、セットアップ完了をマークする。
  このスキル内では AskUserQuestion の使用が明示的に許可されている。
---

# dev-kit:setup-wizard — 初回オンボーディング

dev-kit プラグインの初回オンボーディングを行うスキル。
使用する言語の opt-in（Python / HTML / Next.js / Markdown）を設定し、
プラグインの主要ユースケースを紹介してからセットアップ完了をマークする。

AskUserQuestion はこのスキル内で使用する（明示的に許可済み）。

---

## Tasks

### Step 1: 既存のセットアップ状態を確認する

#### 条件

- 常時 — 最初に実行する

#### 処理

1. `.claude/dev-kit.local.md` の YAML frontmatter を読み込む
2. `setup_done: true` が存在する場合 → `AskUserQuestion` で確認する:
   - `再実行する` — Step 2 に進む
   - `中断する` — ここで終了
3. false または存在しない場合 → Step 2 に進む

→ Step 2 へ

---

### Step 2: 言語・機能設定 — plugin-config に委任する

#### 条件

- Step 1 完了

#### 処理

1. `AskUserQuestion` で質問する:

   **質問**: "dev-kit の参照注入を設定しますか？（使用する言語を有効化します）"

   | オプション | アクション |
   |---|---|
   | すべて設定する（`/dev-kit:plugin-config` を起動） | `/dev-kit:plugin-config` を呼び出してすべてのトグルを設定する |
   | スキップ（あとで設定する） | スキップ; あとから `/dev-kit:plugin-config` を実行できることを伝える |

2. 選択されたアクションを実行する

→ Step 3 へ

---

### Step 3: ユースケース紹介

#### 条件

- Step 2 完了

#### 処理

1. `AskUserQuestion` で質問する（`multiSelect: true`）:

   **質問**: "どの言語・フレームワークの開発に dev-kit を使いますか？（複数選択可）"

   | オプション | 説明 |
   |---|---|
   | Python | `DEV_KIT_PYTHON=true` を設定; `.py` 編集時に Python 規約リファレンスを自動注入 |
   | HTML / CSS / JS | `DEV_KIT_HTML=true` を設定; フロントエンド開発時にデザイントークン・FLOCSS 規約を注入 |
   | Next.js | `DEV_KIT_NEXT=true` を設定; TypeScript/TSX 編集時に App Router 規約を注入 |
   | Markdown | `DEV_KIT_MARKDOWN=true` を設定; `.md` 編集時に Markdown フォーマット規約を注入 |

2. 選択された各ユースケースについて 3〜5 行で説明し、有効化に必要な env 変数を案内する

→ Step 4 へ

---

### Step 4: セットアップ完了をマークする

#### 条件

- Step 3 完了

#### 処理

1. `.claude/dev-kit.local.md` に `setup_done: true` を YAML frontmatter に書き込む（または更新する）:

   ```markdown
   ---
   setup_done: true
   ---

   # dev-kit setup notes

   (ここに自由にメモを追記できます)
   ```

2. ユーザーに伝える:
   - セットアップが完了した
   - `/dev-kit:setup-wizard` でいつでも再実行できる
   - 言語トグルは `/dev-kit:plugin-config` でいつでも変更できる
