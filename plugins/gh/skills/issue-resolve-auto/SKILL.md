---
name: gh:issue-resolve-auto
description: ラベル `wip` の Draft PR を上から N 件取り、issue-resolver に並列で実装させる
---

# issue-resolve-auto — 複数 Draft PR を並列消化

`/gh:pr-wip-create` で作られた Draft PR が複数たまっているときに、上から N 件並列で実装を進めるバッチ版。**マージはしない**（マージは `/gh:pr-review-auto` の責務）。

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_ISSUE_RESOLVE_PARALLEL` | `5` | 並列起動するサブエージェントの上限件数 |
| `GH_WIP_LABEL` | `wip` | 対象 Draft PR を識別するラベル |

## タスク

### ステップ 1: 対象 PR を収集

MCP `list_pull_requests`（`state: open`、`labels: ${GH_WIP_LABEL}`、`draft: true`）で取得し、`created_at` 昇順 → 上位 **N** 件を決定。

| 状況 | 動作 |
|---|---|
| 0 件 | 「対応可能な Draft PR はありません」と報告して停止 |
| 1 件以上 | ステップ 2 へ |

### ステップ 2: 排他制御

| No | 動作 |
|---|---|
| 1 | 各対象 PR にラベル `resolving` を付与（他セッションとの排他） |
| 2 | ラベル `wip` を外す |
| 3 | 自分を assignee に設定 |

### ステップ 3: issue-resolver を並列起動

[サブエージェントで並列実行・完了を待つ] N 件それぞれに `issue-resolver` サブエージェントを起動する。
（戻り値: `[{branch, pr_number, status, commits_added}]`）

各サブエージェントに渡す入力:
- PR 番号 / ブランチ名 / base
- 紐づく Issue 番号（PR 本文の `Refs #N`）
- 採用方針（Issue コメントの `issue-review` 結果から抽出）
- 分割スコープ（PR 本文の説明）

### ステップ 4: 後処理

| 結果 | 動作 |
|---|---|
| 4-OK: ready 化済み | `resolving` を外し `auto-review` を付与（draft 解除はサブエージェントが実施済み） |
| 4-NG: failed | `resolving` を外し `resolve-failed` を付与。失敗理由を PR にコメント |

### ステップ 5: 完了報告

| No | 報告項目 |
|---|---|
| 1 | 起動した PR 件数 / ready 化完了件数 / 失敗件数 |
| 2 | 失敗 PR の番号一覧（あれば） |

## 厳守事項

| No | 禁止 |
|---|---|
| 1 | マージしてはならない（マージは `pr-review-auto` の責務） |
| 2 | `resolving` ラベルが既に付いた PR を別セッションが触ってはならない |
| 3 | Draft 以外の PR は触らない（既に ready なものはレビューフェーズに居る） |
