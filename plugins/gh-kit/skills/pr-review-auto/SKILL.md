---
name: gh-kit:pr-review-auto
description: needs-ai-review の Ready PR を 1 件ずつ直列でレビューし、合格 + needs-user-review なしならマージまで実行
---

# pr-review-auto

`needs-ai-review` 付き Ready PR をキューとして 1 件ずつ消化する。
**並列実行は絶対にしない**（master 取り込みとマージが競合してバグるため）。

`needs-user-review` が残っている PR はレビューだけ実施してマージしない。
ユーザーが `needs-user-review` を外したら別途再エントリー（`needs-ai-review` を付け直す）。

!`cat "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"`

## タスク

### ステップ 1: レビュー対象 PR を収集

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
gh pr list --state open --label "$LABEL_NEEDS_AI_REVIEW" \
  --json number,title,headRefName,baseRefName,statusCheckRollup,labels --limit 50
```

`processing` 付きは除外。`created_at` 昇順。

### ステップ 2: 上から 1 件取り出す

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
gh pr edit {N} --add-label "$LABEL_PROCESSING"
```

CI が failure なら failed へ。

### ステップ 3: pr-reviewer に委譲

[サブエージェントで実行・完了を待つ]
（戻り値: `{verdict, pr_number, branch, message, findings_count}`）

入力:
- PR 番号 / タイトル / base / head
- リポジトリ root
- 現在ラベル一覧（`needs-user-review` の有無）

### ステップ 4: 後処理

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
```

| verdict | 動作 |
|---|---|
| approved-merged | `gh pr edit {N} --remove-label "$LABEL_PROCESSING" --remove-label "$LABEL_NEEDS_AI_REVIEW"`（マージは pr-reviewer が実施済み） |
| approved-user-review-pending | `gh pr edit {N} --remove-label "$LABEL_PROCESSING" --remove-label "$LABEL_NEEDS_AI_REVIEW"`（`needs-user-review` は残す） |
| changes-requested | `gh pr edit {N} --remove-label "$LABEL_PROCESSING" --add-label "$LABEL_NEEDS_FIX"` |
| conflict / failed | `gh pr edit {N} --remove-label "$LABEL_PROCESSING" --add-label "$LABEL_NEEDS_FIX" --add-label "$LABEL_NEEDS_USER_REVIEW" && gh pr comment {N} --body "{詳細}"` |

ステップ 2 に戻ってキューが空になるまで繰り返す。

### ステップ 5: 完了報告

| 項目 | 内容 |
|---|---|
| 処理 PR 件数 | カテゴリ別 |
| 残った PR | 各カテゴリの番号一覧 |
