---
name: gh-kit:pr-review-auto
description: レビュー待ち PR を 1 件ずつ直列で取り出し、pr-reviewer サブエージェントにレビュー + マージまで委譲する
---

# pr-review-auto

メインエージェントが起動し、`auto-review` ラベルの Ready PR をキューとして 1 件ずつ消化する。
各 PR は `pr-reviewer` サブエージェントが「注入ルール準拠か」を中心に審査し、合格すれば自身でマージまで実行する。
**並列実行は絶対にしない**（master 取り込みとマージが競合してバグるため）。

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_KIT_PR_REVIEW_LABEL` | `auto-review` | レビュー対象 PR の識別ラベル |

## タスク

### ステップ 1: レビュー対象 PR を収集

```bash
gh pr list --state open --label "${GH_KIT_PR_REVIEW_LABEL:-auto-review}" \
  --json number,title,headRefName,baseRefName,statusCheckRollup --limit 50
```

`created_at` 昇順にソート。

| 状況 | 動作 |
|---|---|
| 0 件 | 「レビュー対象なし」と報告して停止 |
| 1 件以上 | ステップ 2 へ |

### ステップ 2: 上から 1 件取り出す

```bash
gh pr edit {N} --add-label reviewing --remove-label "${GH_KIT_PR_REVIEW_LABEL:-auto-review}"
```

CI status を確認: `statusCheckRollup` が failure なら 4-NG: failed へ。

### ステップ 3: レビュー + マージを委譲

[サブエージェントで実行・完了を待つ] `pr-reviewer` サブエージェントに以下を渡す。
（戻り値: `{verdict: "approved-merged"|"changes-requested"|"conflict"|"failed", pr_number, branch, message, findings_count}`）

入力:
- PR 番号 / PR タイトル / base / head
- リポジトリ root
- レビュー観点（既定: 注入ルール準拠 / correctness / security）

### ステップ 4: 後処理

| 結果 | コマンド |
|---|---|
| 4-OK: approved-merged | `gh pr edit {N} --remove-label reviewing`（マージは pr-reviewer が `/work:merge` で実施済み、push で PR は自動クローズ） |
| 4-NG: changes-requested | `gh pr edit {N} --remove-label reviewing --add-label needs-fix` |
| 4-NG: conflict | `gh pr edit {N} --remove-label reviewing --add-label conflict-needs-human && gh pr comment {N} --body "{コンフリクト概要}"` |
| 4-NG: failed | `gh pr edit {N} --remove-label reviewing --add-label auto-review-failed && gh pr comment {N} --body "{失敗内容}"` |

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
| 2 | `reviewing` ラベルが既に付いた PR を別セッションが触ってはならない |
| 3 | レビュー観点を「適合 / 不適合」の単純判定で終わらせない（理由を必ず inline コメントで残す） |
