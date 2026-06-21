---
name: gh-kit:pr-review-auto
description: gh-kit:needs-ai-review の Ready PR を 1 件ずつ直列でレビューし、合格 + assignees なしならマージまで実行
disable-model-invocation: true
---

# pr-review-auto

`gh-kit:needs-ai-review` 付き Ready PR をキューとして 1 件ずつ消化する。
**並列実行は絶対にしない**（master 取り込みとマージが競合してバグるため）。

PR に assignees が設定されている場合はレビューだけ実施してマージしない。
ユーザーが assignees を外したら別途再エントリー（`gh-kit:needs-ai-review` を付け直す）。

!`cat "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"`

## タスク

### ステップ 0: Monitor でイベント待機

対象 PR が既に存在する場合はそのままステップ 1 へ進む。
存在しない場合は Monitor ツールで以下のポーリングスクリプトを実行し、対象が出現したらステップ 1 へ進む。

対象条件: `needs-ai-review` ラベル付きの Ready（非 Draft）PR（`processing` 付きは除外）。
直列制約は維持（Monitor 検知後もステップ 1→4 の直列ループを継続する）。

```bash
# Monitor に渡すポーリングスクリプト
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"

while true; do
  AVAILABLE=$(gh pr list --state open --label "$LABEL_NEEDS_AI_REVIEW" \
    --json number,labels,isDraft \
    --jq "[.[] | select(
      .isDraft == false and
      (.labels | map(.name) | index(\"$LABEL_PROCESSING\") | not)
    )] | length" 2>/dev/null || echo 0)
  if [ "$AVAILABLE" -gt 0 ]; then
    echo "TRIGGER:pr-review-auto:count=$AVAILABLE"
    break
  fi
  sleep 30
done
```

Monitor の stdout に `TRIGGER:pr-review-auto` が来たらステップ 1 へ進む。
手動停止は TaskStop で行う。

### ステップ 1: レビュー対象 PR を収集

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
gh pr list --state open --label "$LABEL_NEEDS_AI_REVIEW" \
  --json number,title,headRefName,baseRefName,statusCheckRollup,labels --limit 50
```

`gh-kit:processing` 付きは除外。`created_at` 昇順。

### ステップ 2: 上から 1 件取り出す

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
gh pr edit {N} --add-label "$LABEL_PROCESSING"
# 紐づく Issue に processing:pr-review を付与
ISSUE_N=$(gh pr view {N} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
if [ -n "$ISSUE_N" ]; then
  gh issue edit "$ISSUE_N" --add-label "$LABEL_PROCESSING_PR_REVIEW"
fi
```

CI が failure なら failed へ。

### ステップ 3: pr-reviewer に委譲

[サブエージェントで実行・完了を待つ]
（戻り値: `{verdict, pr_number, branch, message, findings_count}`）

入力:
- PR 番号 / タイトル / base / head
- リポジトリ root
- 現在 assignees 一覧（有無を判定するのに使う）

### ステップ 4: 後処理

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
# 全 verdict 共通: Issue の processing:pr-review を除去
ISSUE_N=$(gh pr view {N} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
```

| verdict | 動作 |
|---|---|
| approved-merged | `gh pr edit {N} --remove-label "$LABEL_PROCESSING" --remove-label "$LABEL_NEEDS_AI_REVIEW"`（マージは pr-reviewer が実施済み）+ `gh issue edit "$ISSUE_N" --remove-label "$LABEL_PROCESSING_PR_REVIEW"` |
| approved-user-review-pending | `gh pr edit {N} --remove-label "$LABEL_PROCESSING" --remove-label "$LABEL_NEEDS_AI_REVIEW"`（assignees はそのまま残す）+ `gh issue edit "$ISSUE_N" --remove-label "$LABEL_PROCESSING_PR_REVIEW"` |
| changes-requested | `gh pr edit {N} --remove-label "$LABEL_PROCESSING" --add-label "$LABEL_NEEDS_FIX"` + `gh issue edit "$ISSUE_N" --remove-label "$LABEL_PROCESSING_PR_REVIEW"` |
| conflict / failed | `GH_LOGIN="$(gh api user --jq '.login')" && gh pr edit {N} --remove-label "$LABEL_PROCESSING" --add-label "$LABEL_NEEDS_FIX" --add-assignee "$GH_LOGIN" && gh pr comment {N} --body "{詳細}"` + `gh issue edit "$ISSUE_N" --remove-label "$LABEL_PROCESSING_PR_REVIEW"` |

ステップ 2 に戻ってキューが空になるまで繰り返す。

### ステップ 5: 完了報告

| 項目 | 内容 |
|---|---|
| 処理 PR 件数 | カテゴリ別 |
| 残った PR | 各カテゴリの番号一覧 |
