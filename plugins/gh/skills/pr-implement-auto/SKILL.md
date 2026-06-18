---
name: gh:pr-implement-auto
description: ラベル `wip` の Draft PR を上から N 件取り、pr-implementer で実装 → Ready 化する
---

# pr-implement-auto — Draft PR を実装して Ready 化

`/gh:pr-wip-create` で雛形化された Draft PR を拾い、中身を実装して Ready for review に切り替えるバッチスキル。**マージはしない**（マージは `/gh:pr-review-auto` の責務）。

実装はブランチごとに独立しているため並列起動可。1 件だけ処理したい場合は引数で PR 番号を渡す。

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_PR_IMPLEMENT_PARALLEL` | `5` | 並列起動するサブエージェント上限件数 |
| `GH_WIP_LABEL` | `wip` | 対象 Draft PR を識別するラベル |

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| PR 番号 | 任意 | 指定時はその 1 件のみ処理。省略時はバッチ |

## タスク

### ステップ 1: 対象 PR を収集

| 状況 | 取得方法 |
|---|---|
| PR 番号指定あり | `get_pull_request` で 1 件取得（`draft: false` ならエラー報告して停止） |
| 指定なし | `list_pull_requests`（`state: open`、`labels: ${GH_WIP_LABEL}`、`draft: true`）昇順 → 上位 **N** 件 |

0 件なら「対応可能な Draft PR はありません」と報告して停止。

### ステップ 2: 排他制御

| No | 動作 |
|---|---|
| 1 | 各対象 PR にラベル `implementing` を付与（他セッションとの排他） |
| 2 | ラベル `wip` を外す |
| 3 | 自分を assignee に設定 |

### ステップ 3: pr-implementer を並列起動

[サブエージェントで並列実行・完了を待つ] N 件それぞれに `pr-implementer` サブエージェントを起動する。
（戻り値: `[{branch, pr_number, status, commits_added}]`）

各サブエージェントに渡す入力:
- PR 番号 / ブランチ名 / base
- 紐づく Issue 番号（PR 本文の `Refs #N`）
- 採用方針（Issue コメントの `issue-review` 結果から抽出）
- 分割スコープ（PR 本文の説明）

### ステップ 4: 後処理

| 結果 | 動作 |
|---|---|
| 4-OK: ready | `implementing` を外し `auto-review` を付与（draft 解除はサブエージェントが実施済み）→ `/gh:pr-review-auto` の対象に入る |
| 4-NG: failed | `implementing` を外し `implement-failed` を付与。失敗理由を PR にコメント |

### ステップ 5: 完了報告

| No | 報告項目 |
|---|---|
| 1 | 起動した PR 件数 / ready 化完了件数 / 失敗件数 |
| 2 | 失敗 PR の番号一覧（あれば） |

## 厳守事項

| No | 禁止 |
|---|---|
| 1 | マージしてはならない（マージは `pr-review-auto` の責務） |
| 2 | `implementing` ラベルが既に付いた PR を別セッションが触ってはならない |
| 3 | Draft 以外の PR は触らない（既に Ready なものはレビューフェーズに居る） |
| 4 | 新規ブランチ・新規 PR を作成しない（雛形作成は `pr-wip-create` の責務） |
