---
name: gh:issue-resolve
description: Draft PR を 1 件拾って実装を完了させる（ready 化 + auto-review ラベル付与まで）
---

# issue-resolve — Draft PR の中身を実装する

`/gh:pr-wip-create` で作られた Draft PR を拾い、実装を完了させて ready 化する。**ブランチ・PR の作成は行わない**（それは pr-wip-create の責務）。

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| PR 番号 | 必須 | 例: `#42`。省略時は `wip` ラベル付き Draft PR を一覧してユーザーに選ばせる |

## タスク

### ステップ 1: Draft PR を読み込む

| No | MCP ツール | 用途 |
|---|---|---|
| 1 | `get_pull_request` | PR メタ情報・ブランチ名・base/head |
| 2 | `get_pull_request_files` | 既存差分（雛形コミット内容） |
| 3 | 紐づく Issue（PR 本文の `Refs #N` から特定） | `get_issue` + `get_issue_comments` で議論経緯を把握 |

`draft: false` の PR が指定された場合は「Draft ではない」と報告して停止。

### ステップ 2: 実装方針を確定

Issue コメント（特に `issue-review` の AI 提案）と PR 本文のスコープ説明から実装方針を抽出。曖昧な点が残っていれば `AskUserQuestion` で確認（議論は本来 Issue 上で完結している前提）。

### ステップ 3: 実装を委譲

[サブエージェントで実行・完了を待つ] `issue-resolver` サブエージェントに以下を渡す。
（戻り値: `{branch, pr_number, status, commits_added}`）

入力:
- PR 番号 / PR ブランチ名 / base ブランチ
- Issue 番号 / 採用方針 / 分割スコープ
- ワークツリーパス（既存 worktree が `.claude/worktrees/{type}-{title}` にあれば再利用、なければ `worktree_create`）

サブエージェントは worktree でコミットを積み、`git push` して PR を更新する。

### ステップ 4: PR を Ready 化

| No | 動作 |
|---|---|
| 1 | `wip` ラベルを外す |
| 2 | `auto-review` ラベルを付与（`/gh:pr-review-auto` の対象になる） |
| 3 | PR の draft 状態を解除（`mark_pull_request_ready_for_review` 相当）→ `update_pull_request` で `draft: false` |
| 4 | PR 本文の末尾に「実装完了。レビュー待ち。」コメントを追記 |

### ステップ 5: 結果報告

| No | 報告項目 |
|---|---|
| 1 | 追加コミット数 |
| 2 | PR の現在ステータス（ready_for_review / auto-review 待ち） |
| 3 | 次のアクション（`/gh:pr-review-auto` を実行） |

## 注意

- 新規ブランチ・新規 PR は作成しない（pr-wip-create 専門）
- マージはしない（pr-review-auto 専門）
- 既存 worktree がある場合は `fetch + reset --hard origin/{branch}` で remote と同期してから着手
