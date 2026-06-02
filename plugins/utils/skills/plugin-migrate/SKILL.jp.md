---
name: plugin-migrate
description: |
  utils プラグインによって作成されたファイルを現行の規約に合わせる。
  以下の場合にトリガーする: 「utils を更新して」「utils:plugin-migrate」と明示的に呼び出された場合。
---
<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# utils:plugin-migrate — プラグイン移行

utils プラグインのバージョンアップに伴う規約変更を既存ファイルへ適用する。

---

## タスク

### ステップ 1: 前提条件確認

#### 処理

1. 現在のブランチが `master` / `main` でないことを確認する
   - `master` / `main` の場合は中断してブランチ作成を依頼する

→ ステップ 2 へ進む

---

### ステップ 2: インストール済みバージョン確認

#### 処理

1. `plugins/utils/.claude-plugin/plugin.json` を読んでインストール済みバージョンを取得する
2. 移行が必要な変更点をバージョンごとに確認する

→ ステップ 3 へ進む

---

### ステップ 3: 規約チェックと修正

#### 処理

現時点（v1.0.0）では静的テンプレートなし。今後のバージョンで規約が変わった場合、
このスキルに移行手順を追記する。

確認項目:
- `agents/jp-mirror-translator.md` に `model: sonnet` が設定されているか
- `skills/jp-mirror-sync/SKILL.md` にサブエージェント起動の手順が含まれているか

→ ステップ 4 へ進む

---

### ステップ 4: 完了レポート

#### 処理

1. 確認・修正した項目をレポートする
2. 変更があればコミットをユーザーに依頼する
