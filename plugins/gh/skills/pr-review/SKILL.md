---
name: gh:pr-review
description: 指定 PR を観点別に AI レビューし、findings を GitHub 上にコメント投稿する
---

# pr-review — PR を AI レビュー

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| PR 番号 | 任意 | `#42` 形式。省略時は現在ブランチに紐づく open な PR を `list_pull_requests` で探す |
| 観点指定 | 任意 | `security` / `perf` / `style` などカンマ区切り。省略時はデフォルト 4 観点 |

## タスク

### ステップ 1: PR 情報取得

MCP で以下を取得:
- `get_pull_request`（メタ情報）
- `get_pull_request_files`（変更ファイル一覧と diff）
- 既存の review comments（観点重複を避けるため）

### ステップ 2: レビュー観点を決定

デフォルト観点（環境変数 `GH_PR_REVIEW_PERSPECTIVES` で上書き可）:

| No | 観点 | 視点 |
|---|---|---|
| 1 | correctness | バグ・ロジック誤り・エッジケース漏れ |
| 2 | security | 認証・入力検証・SQLi/XSS・シークレット混入 |
| 3 | maintainability | 命名・重複・複雑度・将来の拡張容易性 |
| 4 | test-coverage | テスト不足・テスト品質・回帰の取りこぼし |

PR の規模（変更ファイル数）が大きい場合、観点ごとに対象ファイル群を分割割当して負荷を散らす。

### ステップ 3: 観点別にレビューを並列実行

[サブエージェントで並列実行・完了を待つ] 観点ごとに `pr-reviewer` サブエージェントを起動する。
（戻り値: `[{path, line, side, severity, body, perspective}]` の inline コメント候補配列）

入力:
- PR 番号
- レビュー観点と視点
- 対象ファイル一覧 + diff

### ステップ 4: findings を統合・重複排除

| No | 処理 |
|---|---|
| 1 | 同一 file:line に複数 finding がある場合は body を統合 |
| 2 | `severity: nit` のうち装飾的なものは件数が多ければ間引く（10 件超なら general コメントに集約） |
| 3 | 観点間の矛盾は維持して各観点の意見として併記 |

### ステップ 5: PR に投稿

| 投稿方法 | 内容 |
|---|---|
| inline コメント | `create_pending_pull_request_review` → `add_comment_to_pending_review`（複数）→ `submit_pending_pull_request_review` |
| 総評 | `submit_pending_pull_request_review` の `body` フィールドに観点別サマリ |
| イベント | findings の severity 最大が `blocker`/`critical` → `REQUEST_CHANGES`、`major` → `COMMENT`、それ以外 → `APPROVE` |

### ステップ 6: 結果報告

| No | 報告項目 |
|---|---|
| 1 | 観点ごとの finding 件数 |
| 2 | 投稿した review URL |
| 3 | 採用した review event（APPROVE / COMMENT / REQUEST_CHANGES） |

## 注意

- 自分が作成した PR への `APPROVE` は GitHub の制約で投稿できない場合がある → そのときは `COMMENT` にフォールバック
- レビュー実施中は `pr-review-running` ラベルを付与して重複起動を防ぐ
