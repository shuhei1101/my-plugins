---
name: gh:issue-resolve-auto
description: ラベル `auto-resolve` の付いた Issue を上から N 件取り、issue-resolver に並列で実装させる（PR 作成まで）
---

# issue-resolve-auto — 複数 Issue を並列消化

ユーザーが事前に「対応する／対応しない」「採用案」を Issue 上で確定させた上で、対象に `auto-resolve` ラベルを付ける運用を前提とする。本スキルはそれを上から拾って実装を並列実行する。**マージはしない**（PR 作成までで終了 → `pr-review-auto` の責務へ）。

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_ISSUE_RESOLVE_PARALLEL` | `5` | 並列起動するサブエージェントの上限件数 |
| `GH_ISSUE_RESOLVE_LABEL` | `auto-resolve` | 対象 Issue を識別するラベル |
| `GH_ISSUE_REJECT_LABEL` | `wontfix-auto` | 自動却下対象 Issue を識別するラベル |

## タスク

### ステップ 1: 対象 Issue を収集

MCP `list_issues`（`state: open`、`labels: ${GH_ISSUE_RESOLVE_LABEL}`）で取得し、`created_at` 昇順にソート → 上位 **N** 件（`GH_ISSUE_RESOLVE_PARALLEL`）を決定する。

| 状況 | 動作 |
|---|---|
| 0 件 | 「対応可能な Issue はありません」と報告して停止 |
| 1 件以上 | ステップ 2 へ |

並行してラベル `${GH_ISSUE_REJECT_LABEL}` 付きの open Issue も収集する → ステップ 2-B（REJECT）で処理。

### ステップ 2: 排他制御（取得した瞬間にラベル付け替え）

| No | 動作 |
|---|---|
| 1 | 各対象 Issue にラベル `resolving` を付与（他セッションとの排他） |
| 2 | ラベル `${GH_ISSUE_RESOLVE_LABEL}` を外す |
| 3 | 自分を assignee に設定 |

### ステップ 2-B: REJECT 系処理

`${GH_ISSUE_REJECT_LABEL}` 付き Issue は `update_issue`（`state: closed`、`state_reason: not_planned`）でクローズ → ラベル `${GH_ISSUE_REJECT_LABEL}` を `wontfix` に置き換えて記録に残す。

### ステップ 3: issue-resolver を並列起動

[サブエージェントで並列実行・完了を待つ] 取得した N 件それぞれに `issue-resolver` サブエージェントを起動する。
（戻り値: `[{branch, pr_url, pr_number, status}]`）

各サブエージェントに渡す入力:
- Issue 番号 / Issue タイトル / Issue 本文
- ブランチ名候補（`type/issue-{N}-kebab-title`）
- 採用方針（Issue 本文の「対応案」と直近コメントの議論結果から抽出）
- `auto_merge_ok`: Issue に `auto-merge` ラベルが付いていれば true。PR 作成時に `merge-ok` ラベルが付くため、後段の `pr-review-auto` 側のラベル設計と合わせて運用する

### ステップ 4: 後処理

| 結果 | 動作 |
|---|---|
| 4-OK: ready（PR 作成成功） | `resolving` 削除（Issue は PR の `Closes #N` でマージ時に自動クローズ） |
| 4-NG: failed | `resolving` を外し `resolve-failed` を付与。失敗理由を Issue にコメント |

### ステップ 5: 完了報告

| No | 報告項目 |
|---|---|
| 1 | 起動した Issue 件数と、各 PR 番号 / URL |
| 2 | REJECT で wontfix クローズした件数 |
| 3 | 失敗 Issue の番号一覧（あれば） |

## 厳守事項

| No | 禁止 |
|---|---|
| 1 | マージしてはならない（マージは `pr-review-auto` の責務） |
| 2 | `resolving` ラベルが既に付いた Issue を別セッションが触ってはならない |
| 3 | 「対応する／しない」が未確定の Issue（`${GH_ISSUE_RESOLVE_LABEL}` も `${GH_ISSUE_REJECT_LABEL}` も付いていない）には触らない |
