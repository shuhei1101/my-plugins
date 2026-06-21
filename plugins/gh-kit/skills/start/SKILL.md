---
name: gh-kit:start
description: ブランチを作成してワークツリーで作業を開始する。実装に入るときに起動する。
---

## タスク

### ステップ 1: ブランチ名を決定

`{type}/{title}`（例: `feat/test-update`）。`type` は `feat / fix / docs / chore / refactor / test` のいずれか。

### ステップ 2: ワークツリーを作成

`worktree_create` MCP ツール（`gh-kit-tools` サーバー）を実行する:

- branch_type: `{type}` / title: `{title}`
- ワークツリー: `{リポジトリ}/.claude/worktrees/{type}-{title}` に作成
- Stop リマインダー用のセッショントークンも自動で書き込まれる

### ステップ 3: 実装を開始

ワークツリー内で実装を進める。コミットは細かく刻んでよい。

### ステップ 4: 完了後の流れ

| 状況 | 次のアクション |
|---|---|
| GitHub Issue 駆動の作業 | `/gh-kit:pr-draft-create-auto` 経由で Draft PR にコミットを積み、ready 化後 `/gh-kit:pr-review-auto` でマージ |
| ローカル単独作業 | `/gh-kit:merge {ブランチ名}` を提案 |

仕様スナップショットは GitHub Wiki（`/gh-kit:wiki-create`）に書く。
