---
name: work:start
description: ブランチを作成してワークツリーで作業を開始する。実装に入るときに起動する。
---

## タスク

### ステップ 1: ブランチ名を決定

`{type}/{title}`（例: `feat/test-update`）。`type` は `feat / fix / docs / chore / refactor / test` のいずれか。

### ステップ 2: ワークツリーを作成

`worktree_create` MCP ツール（work-tools サーバー）を実行する:

- branch_type: `{type}` / title: `{title}`
- ワークツリー: `{リポジトリ}/.claude/worktrees/{type}-{title}` に作成
- Stop リマインダー用のセッショントークンも自動で書き込まれる

### ステップ 3: 実装を開始

ワークツリー内で実装を進める。コミットは細かく刻んでよい。

### ステップ 4: ノートを更新（実装完了後）

ワークツリーの `.work/notes/` で関連ノートを確認:

- 見つかった場合 → 現在の状態を反映するように更新
- 見つからない場合 → 新規作成
- `.work/notes/_index.md` を同コミットで更新

### ステップ 5: 完了後の流れ

| 状況 | 次のアクション |
|---|---|
| GitHub Issue 駆動の作業 | `/gh:pr-wip-create` で Draft PR にコミットを積み、ready 化後 `/gh:pr-review-auto` でマージ |
| ローカル単独作業 | `/work:merge {ブランチ名}` を提案 |

タスクドキュメント・タスクインデックスは廃止された。GitHub Issue/PR が真実のソース。
