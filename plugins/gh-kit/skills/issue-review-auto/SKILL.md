---
name: gh-kit:issue-review-auto
description: gh-kit:needs-ai-review ラベルの Issue を並列で AI レビューし、コメント投稿する
disable-model-invocation: true
---

# issue-review-auto

`gh-kit:needs-ai-review` 付きの Issue を `issue-reviewer` に並列で渡す。

!`cat "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"`

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_KIT_ISSUE_REVIEW_PARALLEL` | `5` | 並列起動上限 |

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| Issue 番号 | 任意 | 省略時は `gh-kit:needs-ai-review` 付きを全件巡回 |

## フロー概要

```
needs-ai-review 付き Issue 収集
  → issue-reviewer に渡す（初回レビュー or 再レビュー）
    → re_review_needed: false → needs-ai-review 除去 → Draft PR 作成フローへ
    → re_review_needed: true  → needs-ai-review 除去のみ（ユーザーが必要なら再付与）
    → status: waiting         → ラベル変更なし（ユーザー返答待ち）
```

**ユーザーが再レビューを要求する場合:** ユーザーが Issue にコメントを追記した後、手動で `needs-ai-review` を再付与すると、次回の `issue-review-auto` 実行時に `issue-reviewer` が再レビューモードで動作する。

## タスク

### ステップ 0: Monitor でイベント待機

対象 Issue が既に存在する場合はそのままステップ 1 へ進む。
存在しない場合は Monitor ツールで以下のポーリングスクリプトを実行し、対象が出現したらステップ 1 へ進む。

```bash
# Monitor に渡すポーリングスクリプト
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"

while true; do
  COUNT=$(gh issue list --state open --label "$LABEL_NEEDS_AI_REVIEW" \
    --json number --jq 'length' 2>/dev/null || echo 0)
  # processing 付きを除いたカウント
  AVAILABLE=$(gh issue list --state open --label "$LABEL_NEEDS_AI_REVIEW" \
    --json number,labels \
    --jq "[.[] | select(.labels | map(.name) | index(\"$LABEL_PROCESSING\") | not)] | length" 2>/dev/null || echo 0)
  if [ "$AVAILABLE" -gt 0 ]; then
    echo "TRIGGER:issue-review-auto:count=$AVAILABLE"
    break
  fi
  sleep 30
done
```

Monitor の stdout に `TRIGGER:issue-review-auto` が来たらステップ 1 へ進む。
手動停止は TaskStop で行う。

### ステップ 1: 対象 Issue を収集

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
# 指定なしのとき
gh issue list --state open --label "$LABEL_NEEDS_AI_REVIEW" --json number,title,labels --limit 100
# 指定ありのとき
gh issue view {N} --json number,title,body,labels,comments
```

`gh-kit:processing` 付きは除外（他セッションが処理中）。0 件なら停止。

### ステップ 2: 排他制御

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
gh issue edit {N} --add-label "$LABEL_PROCESSING"
```

### ステップ 3: issue-reviewer を並列起動

[サブエージェントで並列実行・完了を待つ] 上位 N 件を並列処理する。
（戻り値: `{issue_number, re_review_needed, status}` — エージェントが gh CLI でコメント投稿を完結させる）

### ステップ 4: ラベル更新 + assignee 追加

戻り値の `status` と `re_review_needed` に応じてラベルを操作する。

**status が `ok` の場合（通常レビュー完了）:**

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"

# status: waiting の場合 — ユーザー返答待ちのため processing のみ除去
if [ "{status}" = "waiting" ]; then
  gh issue edit {N} --remove-label "$LABEL_PROCESSING"
  # needs-ai-review は維持（次回以降も待機継続）
  return
fi

# status: ok の場合 — processing と needs-ai-review を除去
ARGS=(--remove-label "$LABEL_PROCESSING" --remove-label "$LABEL_NEEDS_AI_REVIEW")
gh issue edit {N} "${ARGS[@]}"

# needs_user_review: true の場合は assignee を追加
if [ "{needs_user_review}" = "true" ]; then
  GH_LOGIN="$(gh api user --jq '.login')"
  gh issue edit {N} --add-assignee "$GH_LOGIN"
fi

# re_review_needed: false かつ needs-* が他になければ Draft PR フローへ進める（呼び出し元が判定）
```

**注意:** `needs-user-review` ラベルは使用しない。ユーザー確認が必要な場合は assignee を追加する。ユーザーが AI の追加質問に返答した後、再度 AI レビューが必要と判断した場合は手動で `needs-ai-review` を付け直す。

**status が `duplicate_merged` または `duplicate_closed` の場合（重複検出・クローズ済み）:**

Issue はすでにクローズされているため、ラベル付け替えは不要。
`processing` ラベルのみ除去する（クローズ済み Issue には add-label が効かないため remove のみ）:

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
gh issue edit {N} --remove-label "$LABEL_PROCESSING" --remove-label "$LABEL_NEEDS_AI_REVIEW" 2>/dev/null || true
```

### ステップ 5: 結果報告

| 項目 | 内容 |
|---|---|
| レビュー件数 | 番号一覧 |
| ユーザー確認要 | assignee 追加/非追加の内訳 |
| re_review_needed | true/false の内訳 |
| waiting | 返答待ちで未処理の件数 |
| 重複検出 | `duplicate_merged` / `duplicate_closed` になった Issue 番号と移行先 Issue 番号 |
