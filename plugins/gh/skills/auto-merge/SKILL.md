---
name: gh:auto-merge
description: ラベル `merge-ok` の付いた PR を直列で 1 件ずつマージする
---

# auto-merge — 直列マージ窓口

メインエージェントが起動し、`merge-ok` ラベルの PR をキューとして 1 件ずつ消化する。**並列実行は絶対にしない**（master 取り込みとマージが競合してバグるため）。

## タスク

### ステップ 1: マージ対象 PR を収集

MCP `list_pull_requests`（`state: open`、`labels: merge-ok`）または `search_pull_requests` で取得し、`created_at` 昇順にソート。

| 状況 | 動作 |
|---|---|
| 0 件 | 「マージ対象なし」と報告して停止 |
| 1 件以上 | ステップ 2 へ |

### ステップ 2: 上から 1 件取り出す

| No | 動作 |
|---|---|
| 1 | PR にラベル `merging` を付与（他セッションの auto-merge と排他するため） |
| 2 | ラベル `merge-ok` を外す |
| 3 | CI status を確認（`get_pull_request_status`）。failure ならステップ 4-NG へ |

### ステップ 3: マージ実行

[サブエージェントで実行・完了を待つ] `auto-merger` サブエージェントに以下を渡す。
（戻り値: `{status: "merged"|"conflict"|"failed", branch, pr_number, message}`）

入力:
- PR 番号 / PR タイトル / ベースブランチ / ヘッドブランチ
- リポジトリ root のパス

サブエージェントは:
1. ヘッドブランチに対応するワークツリーを復帰（無ければ作成）
2. `/work:merge` スキルを実行（コンフリクト時の方針も `/work:merge` のものに従う）
3. マージ後ローカルから push して GitHub 側を `merged` 状態にする
4. 結果を返す

### ステップ 4: 後処理

| 結果 | 動作 |
|---|---|
| 4-OK: merged | PR は自動的にクローズ。`merging` ラベル削除。ステップ 2 に戻って次の 1 件 |
| 4-NG: conflict | `conflict-needs-human` ラベルを付与し `merging` を外す。コンフリクト概要を PR にコメント。ステップ 2 に戻って次の 1 件 |
| 4-NG: failed | `auto-merge-failed` ラベルを付与し `merging` を外す。失敗内容を PR にコメント。ステップ 2 に戻って次の 1 件 |

### ステップ 5: 完了報告

| No | 報告項目 |
|---|---|
| 1 | 処理した PR 件数（merged / conflict / failed） |
| 2 | 残ったコンフリクト PR の番号一覧（あれば） |

## 厳守事項

| No | 禁止 |
|---|---|
| 1 | サブエージェントを並列起動して同時に複数 PR をマージしてはならない |
| 2 | `merging` ラベルが既に付いた PR を別セッションが触ってはならない（取得時にスキップ） |
| 3 | コンフリクトを `-X ours/theirs` で一括解消してはならない（`/work:merge` の方針に従う） |
