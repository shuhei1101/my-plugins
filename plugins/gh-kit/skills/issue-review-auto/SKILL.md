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
（戻り値: `{issue_number, re_review_needed, status}` — エージェントが gh CLI でコメント投稿を完結させる）

### ステップ 4: ラベル更新

戻り値の `status` と `re_review_needed` に応じてラベルを操作する。

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

# re_review_needed: false かつ needs-* が他になければ Draft PR フローへ進める（呼び出し元が判定）
```

**注意:** `needs-user-review` ラベルは付与しない。ユーザーが AI の追加質問に返答した後、再度 AI レビューが必要と判断した場合は手動で `needs-ai-review` を付け直す。

### ステップ 5: 結果報告

| 項目 | 内容 |
|---|---|
| レビュー件数 | 番号一覧 |
| re_review_needed | true/false の内訳 |
| waiting | 返答待ちで未処理の件数 |
