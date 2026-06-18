---
name: gh:pr-wip-create
description: ラベル `go` の付いた Issue から Draft PR-WIP を作成する（1 Issue から複数派生可）
---

# pr-wip-create — Draft PR の雛形を切る

ユーザーとの議論が終わって `go` ラベルが付いた Issue から、実装着手用の Draft PR を作る。1 Issue から複数派生してよい（粒度分割が必要なときは複数回起動）。実装は別途 `/gh:issue-resolve` か手作業で進める。

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| Issue 番号 | 必須 | 例: `#42` |
| 分割スコープ | 任意 | 1 Issue から複数派生する場合の各 PR のスコープ説明（例: 「ルーター層だけ」「DB スキーマだけ」） |

引数なしで起動した場合は `go` ラベル付き Issue を全件巡回し、ユーザーに「どの Issue / どのスコープで切るか」を `AskUserQuestion` で確認する。

## タスク

### ステップ 1: Issue を取得

`get_issue` で Issue 本文・コメント（特に `issue-review` の AI コメント）を読む。

| ラベル状態 | 動作 |
|---|---|
| `go` あり | 続行 |
| `go` なし | 「`go` ラベル未付与」と報告して停止 |

### ステップ 2: PR-WIP の雛形を作成

[サブエージェントで実行・完了を待つ] `pr-wip-creator` サブエージェントに以下を渡す。
（戻り値: `{branch, pr_url, pr_number}`）

入力:
- Issue 番号 / タイトル
- 分割スコープ（未指定なら Issue 全体）
- ブランチ名候補: `{type}/issue-{N}-{kebab-scope}`（同 Issue から複数派生時は scope で識別）
- PR 本文に必須で入れる文言:
  - `Refs #{Issue 番号}`（**`Closes` ではなく `Refs`** — 1 Issue 複数 PR を考慮し、最後の PR がマージされるまで Issue を閉じない）
  - 分割スコープの説明
  - 「このスコープで実装予定」のチェックボックス（雛形）

サブエージェントは:
1. `/work:start` でブランチ + worktree 作成
2. Issue 本文を引用した PR 用 README を最初のコミットとして積む（実装はまだ）
3. `git push -u origin {branch}`
4. `create_pull_request` で **draft: true** で PR 作成

### ステップ 3: 後処理

| No | 動作 |
|---|---|
| 1 | PR にラベル `wip` を付与 |
| 2 | 元 Issue にコメント「PR #{新 PR 番号} を起票しました（スコープ: {scope}）」を投稿 |
| 3 | 元 Issue の `go` ラベルは外さない（複数 PR を派生させる場合のため）。全派生が完了した時点でユーザーが手動で外す or 別スキルで一括処理 |

### ステップ 4: 結果報告

| No | 報告項目 |
|---|---|
| 1 | 作成したブランチ名 |
| 2 | 作成した Draft PR の URL と番号 |
| 3 | 次のアクション（`/gh:issue-resolve #{PR番号}` で実装着手、または手動実装） |

## 注意

- 必ず **draft** で作成する（`pr-review-auto` がレビュー対象に含めないため）
- `Closes #{Issue}` ではなく `Refs #{Issue}` を使う（1 Issue 複数 PR で Issue が早期クローズされるのを防ぐ）
- 同一 Issue から派生する PR はブランチ名でスコープを識別する（`issue-42-router` / `issue-42-schema` 等）
