---
name: gh:pr-review-auto
description: レビュー待ち PR を 1 件ずつ直列で取り出し、pr-reviewer サブエージェントにレビュー + マージまで委譲する
---

# pr-review-auto — レビュー＋マージ直列オーケストレーター

メインエージェントが起動し、`auto-review` ラベルの open PR をキューとして 1 件ずつ消化する。各 PR は `pr-reviewer` サブエージェントが「注入ルール準拠か」を中心に審査し、合格すれば自身でマージまで実行する。**並列実行は絶対にしない**（master 取り込みとマージが競合してバグるため）。

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_PR_REVIEW_LABEL` | `auto-review` | レビュー対象 PR の識別ラベル |

## タスク

### ステップ 1: レビュー対象 PR を収集

MCP `list_pull_requests`（`state: open`、`labels: ${GH_PR_REVIEW_LABEL}`）または `search_pull_requests` で取得し、`created_at` 昇順にソート。

| 状況 | 動作 |
|---|---|
| 0 件 | 「レビュー対象なし」と報告して停止 |
| 1 件以上 | ステップ 2 へ |

### ステップ 2: 上から 1 件取り出す

| No | 動作 |
|---|---|
| 1 | PR にラベル `reviewing` を付与（他セッションとの排他） |
| 2 | ラベル `auto-review` を外す |
| 3 | CI status を確認（`get_pull_request_status`）。failure ならステップ 4-NG へ |

### ステップ 3: レビュー + マージを委譲

[サブエージェントで実行・完了を待つ] `pr-reviewer` サブエージェントに以下を渡す。
（戻り値: `{verdict: "approved-merged"|"changes-requested"|"conflict"|"failed", pr_number, branch, message, findings_count}`）

入力:
- PR 番号 / PR タイトル / ベースブランチ / ヘッドブランチ
- リポジトリ root のパス
- レビュー観点（既定: 注入ルール準拠 / correctness / security）

### ステップ 4: 後処理

| 結果 | 動作 |
|---|---|
| 4-OK: approved-merged | PR は GitHub 側で自動クローズ。`reviewing` 削除。ステップ 2 へ |
| 4-NG: changes-requested | `needs-fix` ラベルを付与し `reviewing` を外す。サブエージェントが投稿した review が修正依頼として残る |
| 4-NG: conflict | `conflict-needs-human` を付与し `reviewing` を外す。コンフリクト概要を PR にコメント |
| 4-NG: failed | `auto-review-failed` を付与し `reviewing` を外す。失敗内容を PR にコメント |

ステップ 2 に戻ってキューが空になるまで繰り返す。

### ステップ 5: 完了報告

| No | 報告項目 |
|---|---|
| 1 | 処理した PR 件数（approved-merged / changes-requested / conflict / failed） |
| 2 | 各カテゴリに残った PR の番号一覧 |

## 厳守事項

| No | 禁止 |
|---|---|
| 1 | `pr-reviewer` を並列起動してはならない（マージが直列であるべきため） |
| 2 | `reviewing` ラベルが既に付いた PR を別セッションが触ってはならない（取得時にスキップ） |
| 3 | レビュー観点を「適合 / 不適合」の単純判定で終わらせない（理由を必ず inline コメントで残す） |
