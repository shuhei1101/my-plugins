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

`processing` 付きは除外（他セッションが処理中）。0 件なら停止。

### ステップ 2: 排他制御

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
gh issue edit {N} --add-label "$LABEL_PROCESSING"
```

### ステップ 3: issue-reviewer を並列起動

[サブエージェントで並列実行・完了を待つ] 上位 N 件を並列処理する。
（戻り値: `{issue_number, needs_user_review, status}` — エージェントが gh CLI でコメント投稿を完結させる）

### ステップ 4: ラベル更新

`status` の値に応じて処理を分岐する:

**status が `ok` の場合（通常レビュー完了）:**

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
ARGS=(--remove-label "$LABEL_PROCESSING" --remove-label "$LABEL_NEEDS_AI_REVIEW")
if [ "{needs_user_review}" = "true" ]; then
  ARGS+=(--add-label "$LABEL_NEEDS_USER_REVIEW")
fi
gh issue edit {N} "${ARGS[@]}"
```

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
| needs-user-review | 付与/非付与の内訳 |
| 重複検出 | `duplicate_merged` / `duplicate_closed` になった Issue 番号と移行先 Issue 番号 |
