---
name: gh-kit:pr-review-auto
description: needs-ai-review が付いた Ready PR を 1 件ずつ直列でレビューし、合格 + needs-user-review なしならマージまで実行
---

# pr-review-auto

メインエージェントが起動し、`needs-ai-review` ラベル付きの Ready PR をキューとして 1 件ずつ消化する。
各 PR は `pr-reviewer` サブエージェントが「注入ルール準拠か」を中心に審査し、合格 + `needs-user-review` なしなら自身でマージまで実行する。
**並列実行は絶対にしない**（master 取り込みとマージが競合してバグるため）。

`needs-user-review` が残っている PR はレビューだけ実施してマージしない（ユーザー判断待ち）。
ユーザーが `needs-user-review` を外したら再エントリーで拾われる。

## ラベル定義の読み込み

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
```

## タスク

### ステップ 1: レビュー対象 PR を収集

```bash
gh pr list --state open --label "$LABEL_NEEDS_AI_REVIEW" \
  --json number,title,headRefName,baseRefName,statusCheckRollup,labels --limit 50
```

`processing` 付きは除外（他セッションが触っている）。
`created_at` 昇順にソート。

| 状況 | 動作 |
|---|---|
| 0 件 | 「レビュー対象なし」と報告して停止 |
| 1 件以上 | ステップ 2 へ |

### ステップ 2: 上から 1 件取り出す

```bash
gh pr edit {N} --add-label "$LABEL_PROCESSING"
```

`needs-ai-review` は完了時に外す（処理中も付いたまま）。CI が failure なら 4-NG: failed へ。

### ステップ 3: レビュー + マージを委譲

[サブエージェントで実行・完了を待つ] `pr-reviewer` サブエージェントに以下を渡す。
（戻り値: `{verdict: "approved-merged"|"approved-user-review-pending"|"changes-requested"|"conflict"|"failed", pr_number, branch, message, findings_count}`）

入力:
- PR 番号 / PR タイトル / base / head
- リポジトリ root
- レビュー観点（既定: 注入ルール準拠 / correctness / security）
- PR 現在ラベル一覧（`needs-user-review` が付いているかをサブエージェントに伝える）

### ステップ 4: 後処理

| verdict | 動作 |
|---|---|
| approved-merged | `gh pr edit {N} --remove-label "$LABEL_PROCESSING" --remove-label "$LABEL_NEEDS_AI_REVIEW"`（マージは pr-reviewer が `/work:merge` で実施済み、push で PR は自動クローズ） |
| approved-user-review-pending | `gh pr edit {N} --remove-label "$LABEL_PROCESSING" --remove-label "$LABEL_NEEDS_AI_REVIEW"`（needs-user-review は残す。ユーザーが外したら再エントリーされない — needs-ai-review が無いので。再エントリーが必要なら別途付け直す or ユーザーが付け直す） |
| changes-requested | `gh pr edit {N} --remove-label "$LABEL_PROCESSING" --add-label "$LABEL_NEEDS_FIX"` |
| conflict | `gh pr edit {N} --remove-label "$LABEL_PROCESSING" --add-label "$LABEL_NEEDS_FIX" --add-label "$LABEL_NEEDS_USER_REVIEW" && gh pr comment {N} --body "{コンフリクト概要}"` |
| failed | `gh pr edit {N} --remove-label "$LABEL_PROCESSING" --add-label "$LABEL_NEEDS_FIX" --add-label "$LABEL_NEEDS_USER_REVIEW" && gh pr comment {N} --body "{失敗内容}"` |

ステップ 2 に戻ってキューが空になるまで繰り返す。

### ステップ 5: 完了報告

| No | 報告項目 |
|---|---|
| 1 | 処理した PR 件数（カテゴリ別） |
| 2 | 各カテゴリに残った PR の番号一覧 |

## 厳守事項

| No | 禁止 |
|---|---|
| 1 | `pr-reviewer` を並列起動してはならない |
| 2 | `processing` 付きの PR を別セッションが触ってはならない |
| 3 | `needs-user-review` が付いている PR をマージしてはならない（AI 単独判断でマージできない印） |
