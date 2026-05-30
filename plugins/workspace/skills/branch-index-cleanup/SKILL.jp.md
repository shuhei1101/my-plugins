---
name: branch-index-cleanup
description: |
  git ブランチと index.yaml / index.archive.yaml を照合し、未登録ブランチを整理する。
  各ブランチを A（削除）/ B（archive 追記 → 削除）/ C（index 追記）に分類して実行。
  「ブランチを整理して」「未登録ブランチを片付けて」「branch-index-cleanup して」
  または `/workspace:branch-index-cleanup` で起動。
disable-model-invocation: true
---
<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# workspace:branch-index-cleanup — 未登録ブランチの整理

ローカルブランチと `index.yaml` / `index.archive.yaml` を比較し、
未登録ブランチをインタラクティブに分類・整理する。

---

## タスク

### Step 1: 未登録ブランチの収集

#### 条件

- 常に最初に実行

#### 処理

1. ローカルブランチを一覧取得
2. `index.yaml` と `index.archive.yaml` から登録済み PR ID を収集
3. どちらにも登録されていないブランチを「未登録ブランチ」として列挙

→ Step 2 へ

---

### Step 2: 分類

#### 条件

- Step 1 完了・未登録ブランチが 1 件以上

#### 処理

1. 未登録ブランチをブランチ名から自動推定（id・title・type）して表形式で表示
2. ユーザーに各ブランチを A / B / C に分類してもらう:
   - **A** — 完了済み・不要（削除のみ）
   - **B** — 完了済み・記録したい（archive 追記 → 削除）
   - **C** — 作業継続（index.yaml に追記）
3. B / C のメタデータをユーザーが修正できる

→ Step 3 へ

---

### Step 3: 処置の実行

#### 条件

- Step 2 完了・ユーザーが全分類を確認済み

#### 処理

B → C → A の順で実行:

- **B**: `index.archive.yaml` にエントリ追記 → `git branch -d`
- **C**: `index-tool.py add` で `index.yaml` に追記
- **A**: `git branch -d`

`-d` で削除できない場合（未マージ）はユーザーに強制削除（`-D`）を確認する。

→ Step 4 へ

---

### Step 4: 結果報告

分類ごとの件数・ブランチ名を表形式で報告し、残存ブランチを確認する。

---

### Step 5: 整理不要

#### 条件

- Step 1 で未登録ブランチが 0 件

#### 処理

「すべてのブランチが登録済み」と報告して終了。
