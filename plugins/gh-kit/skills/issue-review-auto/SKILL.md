---
name: gh-kit:issue-review-auto
description: needs-ai-review ラベルの Issue を並列で AI レビューし、コメント投稿する
---

# issue-review-auto

`needs-ai-review` 付きの Issue を `issue-reviewer` に並列で渡す。

!`cat "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"`

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_KIT_ISSUE_REVIEW_PARALLEL` | `5` | 並列起動上限 |

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| Issue 番号 | 任意 | 省略時は `needs-ai-review` 付きを全件巡回 |

## タスク

### ステップ 1: 対象 Issue を収集

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
# 指定なしのとき
gh issue list --state open --label "$LABEL_NEEDS_AI_REVIEW" --json number,title,labels --limit 100
# 指定ありのとき
gh issue view {N} --json number,title,body,labels,comments
```

`processing` 付きは除外（他セッションが処理中）。0 件なら停止。

### ステップ 2: 排他制御

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
gh issue edit {N} --add-label "$LABEL_PROCESSING"
```

### ステップ 3: issue-reviewer を並列起動

[サブエージェントで並列実行・完了を待つ] 上位 N 件を並列処理する。
（戻り値: `{issue_number, needs_user_review, status}` — エージェントが gh CLI でコメント投稿を完結させる）

### ステップ 4: ラベル更新 + assignee 追加

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
gh issue edit {N} --remove-label "$LABEL_PROCESSING" --remove-label "$LABEL_NEEDS_AI_REVIEW"
if [ "{needs_user_review}" = "true" ]; then
  GH_LOGIN="$(gh api user --jq '.login')"
  gh issue edit {N} --add-assignee "$GH_LOGIN"
fi
```

### ステップ 5: 結果報告

| 項目 | 内容 |
|---|---|
| レビュー件数 | 番号一覧 |
| ユーザー確認要 | assignee 追加/非追加の内訳 |
