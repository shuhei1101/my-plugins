---
name: issue-save
description: |
  イシュー1件を `.work/issues/` に保存する共有サブスキル。
  `_index.yaml` を読んで `last_id` をインクリメントし、ISSUE-{N}.md を作成して index を更新する。
  issue-scan・issue-create から呼び出されることを想定。直接ユーザーが呼ぶ用途は想定しない。
disable-model-invocation: true
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

---

# work:issue-save — イシューを保存する

1件のイシューを `.work/issues/` に保存する共有サブスキル。
`issue-scan` や `issue-create` から、記録したいイシューの情報とともに呼び出される。

---

## 概要

**受け取る情報**:
- タイトル（必須）: イシューの内容を端的に表す1文
- タイプ（必須）: `refactor` / `rule-violation` / `ui` / `backend` のいずれか — `_index.yaml` のみに記録
- 優先度（必須）: `high` / `medium` / `low` のいずれか — `_index.yaml` のみに記録
- タグ（任意）: 関連キーワードのリスト — `_index.yaml` のみに記録
- スキャンスコープ（任意）: どのファイル・レイヤーが対象か（issue-scan が提供）— `_index.yaml` のみに記録
- 問題の説明（必須）: 何が問題かの説明文
- 修正案（任意）: 改善の方向性（不明なら省略）
- 水平展開（任意）: 同じ問題がコードベース他所にも存在するかのメモ（issue-scan が提供）
- 関連ドキュメント（任意）: 関連リファレンス・ノートへのリンク

**戻り値**: 作成したイシュー ID（例: `ISSUE-003`）を呼び出し元に返す

---

## タスク

### ステップ1: 受け取った情報を確認する

#### 条件

- 常に — 最初に実行する

#### 処理

1. 呼び出し元から渡されたイシュー情報を確認する
2. 必須項目（タイトル・タイプ・優先度・問題の説明）が揃っているか確認する
   - 欠けていれば呼び出し元にエラーを返して停止する

→ ステップ2へ進む

#### 出力

- 保存に必要なイシュー情報が確定

---

### ステップ2: 次の ID を決める

#### 条件

- 常に — ステップ1の後に実行する

#### 処理

1. `.work/issues/_index.yaml` を読み込む（なければ `last_id: 0, issues: []` として扱う）
2. `last_id` に 1 を加える
3. イシュー ID を決める: `ISSUE-{last_id:03d}`（3桁ゼロ埋め）

→ ステップ3へ進む

#### 出力

- 新しい `last_id` と イシュー ID

---

### ステップ3: イシューファイルを作成する

#### 条件

- 常に — ステップ2の後に実行する

#### 処理

1. `.work/issues/ISSUE-{N}.md` を `Write` する。イシューファイルの構造は、`.work/issues/` 配下の
   ファイルを書き込んだ瞬間に `references/work-dir/イシュー.md` から**自動注入**される（最初の
   書き込みが一度ブロックされ、テンプレートが出てくる）。注入されたテンプレートを元に、呼び出し元
   から渡された項目を埋めて作成する。データが渡されなかった `## 修正案` / `## 水平展開` /
   `## 関連ドキュメント` のセクションは省略する。Type / Priority / Tags / Scan scope は
   `_index.yaml` にのみ記録し、イシューファイルには書かない。

→ ステップ4へ進む

#### 出力

- `.work/issues/ISSUE-{N}.md` が作成済み

---

### ステップ4: _index.yaml を更新する

#### 条件

- 常に — ステップ3の後に実行する

#### 処理

1. `_index.yaml` に以下のエントリを追記する:
   ```yaml
   - id: ISSUE-{N}
     title: "{タイトル}"
     created: {YYYY-MM-DD}
     type: {タイプ}
     scan_scope:
       - "{スコープ}"   ← スコープが提供されなかった場合は scan_scope: [] とする
     priority: {優先度}
     tags: [{タグ}]
   ```
2. `last_id` を新しい値に更新して `_index.yaml` を書き込む

→ 完了

#### 出力

- 作成したイシュー ID（例: `ISSUE-003`）を呼び出し元に返す
