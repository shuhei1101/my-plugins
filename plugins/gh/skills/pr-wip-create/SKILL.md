---
name: gh:pr-wip-create
description: ラベル `go` の Issue を全件取り、各 Issue から Draft PR-WIP を作成する（1 Issue 複数派生対応）
---

# pr-wip-create — go Issue を Draft PR 化

ユーザーとの議論が終わって `go` ラベルが付いた Issue を全件巡回し、それぞれから Draft PR を作る。1 Issue から複数派生してよい（粒度分割が必要なときは同 Issue を分割スコープごとに複数回処理）。実装は別途 `/gh:pr-implement-auto` が担当。

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_PR_WIP_CREATE_PARALLEL` | `5` | 並列起動するサブエージェント上限件数 |
| `GH_GO_LABEL` | `go` | 対象 Issue を識別するラベル |

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| Issue 番号 | 任意 | 指定時はその 1 件のみ処理 |
| 分割スコープ | 任意 | 1 Issue から複数派生する場合のスコープ名（カンマ区切り） |

引数なしのときは `go` ラベル付き Issue を全件取得し、各 Issue について `issue-review` の AI コメントから「分割提案」を読んで自動で分割スコープを決定する。

## タスク

### ステップ 1: 対象 Issue を収集

| 状況 | 取得方法 |
|---|---|
| Issue 番号指定あり | `get_issue` で 1 件取得 |
| 指定なし | `list_issues`（`state: open`、`labels: ${GH_GO_LABEL}`）昇順 |

0 件なら「`go` ラベル付き Issue はありません」と報告して停止。

### ステップ 2: 各 Issue から作る Draft PR の数を決定

| 条件 | 作る PR 数 |
|---|---|
| `split-needed` ラベルあり + `issue-review` コメントに分割提案表あり | 分割提案表の行数（各スコープ 1 PR） |
| 引数で分割スコープ指定あり | 指定数 |
| 上記なし | 1 PR（Issue 全体） |

各 Draft PR の生成タスクを並列実行待ち行列に積む（上限 **N**）。

### ステップ 3: 排他制御

| No | 動作 |
|---|---|
| 1 | 各 Issue にラベル `wip-creating` を一時付与（処理中の他セッション衝突防止） |

`go` ラベル自体は外さない（複数派生で何度も処理対象になるため。全派生完了後にユーザーが手動で外す）。

### ステップ 4: pr-wip-creator を並列起動

[サブエージェントで並列実行・完了を待つ] 各 Draft PR 生成タスクに `pr-wip-creator` サブエージェントを起動する。
（戻り値: `[{branch, pr_url, pr_number}]`）

各サブエージェントに渡す入力:
- Issue 番号 / タイトル
- 分割スコープ（未指定なら Issue 全体）
- ブランチ名候補: `{type}/issue-{N}-{kebab-scope}`
- base ブランチ

### ステップ 5: 後処理

| No | 動作 |
|---|---|
| 1 | 作成された各 PR にラベル `wip` を付与 |
| 2 | 元 Issue に「PR #{番号} を起票（スコープ: {scope}）」コメントを追記 |
| 3 | `wip-creating` ラベルを外す |

### ステップ 6: 完了報告

| No | 報告項目 |
|---|---|
| 1 | 対象 Issue 件数 / 作成した Draft PR 件数 |
| 2 | 各 PR の URL と紐づく Issue 番号 |
| 3 | 次のアクション（`/gh:pr-implement-auto` を実行） |

## 注意

| No | 内容 |
|---|---|
| 1 | 必ず **draft** で作成（`pr-review-auto` の対象外に置くため） |
| 2 | `Closes #N` ではなく `Refs #N` を使う（1 Issue 複数 PR で Issue が早期クローズされるのを防ぐ） |
| 3 | 同一 Issue から派生する PR はブランチ名のスコープで識別（`issue-42-router` / `issue-42-schema` 等） |
| 4 | `go` ラベルは外さない（外す判断はユーザー） |
