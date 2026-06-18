---
name: gh-kit:pr-wip-create
description: ラベル `go` の Issue を全件取り、各 Issue から Draft PR-WIP を作成する（1 Issue 複数派生対応）
---

# pr-wip-create

`go` ラベル付き Issue を全件巡回し、それぞれから Draft PR を作る。
1 Issue から複数派生してよい（粒度分割が必要なときは同 Issue を分割スコープごとに複数回処理）。
実装は別途 `/gh-kit:pr-implement-auto` が担当。

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_KIT_PR_WIP_CREATE_PARALLEL` | `5` | 並列起動するサブエージェント上限件数 |

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| Issue 番号 | 任意 | 指定時はその 1 件のみ処理 |
| 分割スコープ | 任意 | 1 Issue から複数派生する場合のスコープ名（カンマ区切り） |

引数なしのときは `go` ラベル付き Issue を全件取得し、各 Issue について `issue-review` の AI コメントから「分割提案」を読んで自動で分割スコープを決定する。

## タスク

### ステップ 1: 対象 Issue を収集

| 状況 | コマンド |
|---|---|
| Issue 番号指定あり | `gh issue view {N} --json number,title,body,labels,comments` |
| 指定なし | `gh issue list --state open --label go --json number,title,labels,comments --limit 50`（昇順） |

0 件なら「`go` ラベル付き Issue はありません」と報告して停止。

### ステップ 2: 各 Issue から作る Draft PR の数を決定

| 条件 | 作る PR 数 |
|---|---|
| `split-needed` ラベル + `issue-review` コメントに分割提案表あり | 分割提案表の行数（各スコープ 1 PR） |
| 引数で分割スコープ指定あり | 指定数 |
| 上記なし | 1 PR（Issue 全体） |

各 Draft PR の生成タスクを並列実行待ち行列に積む（上限 **N**）。

### ステップ 3: 排他制御

各 Issue にラベル `wip-creating` を一時付与:

```bash
gh issue edit {N} --add-label wip-creating
```

`go` ラベル自体は外さない（複数派生で何度も処理対象になるため）。

### ステップ 4: pr-wip-creator を並列起動

[サブエージェントで並列実行・完了を待つ] 各 Draft PR 生成タスクに `pr-wip-creator` サブエージェントを起動する。
（戻り値: `[{branch, pr_url, pr_number}]`）

入力:
- Issue 番号 / タイトル
- 分割スコープ（未指定なら Issue 全体）
- ブランチ名候補: `{type}/issue-{N}-{kebab-scope}`
- base ブランチ

### ステップ 5: 後処理

```bash
# 作成された各 PR にラベル `wip` を付与
gh pr edit {PR番号} --add-label wip

# 元 Issue にコメント追加 + wip-creating ラベル除去
gh issue comment {N} --body "PR #{番号} を起票（スコープ: {scope}）"
gh issue edit {N} --remove-label wip-creating
```

### ステップ 6: 完了報告

| No | 報告項目 |
|---|---|
| 1 | 対象 Issue 件数 / 作成した Draft PR 件数 |
| 2 | 各 PR の URL と紐づく Issue 番号 |
| 3 | 次のアクション（`/gh-kit:pr-implement-auto` を実行） |

## 注意

| No | 内容 |
|---|---|
| 1 | 必ず **draft** で作成（`--draft` フラグ） |
| 2 | `Closes #N` ではなく `Refs #N` を使う（1 Issue 複数 PR で Issue が早期クローズされるのを防ぐ） |
| 3 | 同一 Issue から派生する PR はブランチ名のスコープで識別 |
| 4 | `go` ラベルは外さない（外す判断はユーザー） |
