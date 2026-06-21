---
name: gh-kit:pr-implement-auto
description: ラベル wip / needs-fix の Draft PR を N 件並列で実装し、Ready 化 → そのまま pr-review-auto に連鎖
disable-model-invocation: true
---

# pr-implement-auto

`pr-draft-create-auto` で雛形化された Draft PR を拾い、中身を実装して Ready for review に切り替える。

!`cat "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"`

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_KIT_PR_IMPLEMENT_PARALLEL` | `5` | 並列起動上限 |

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| PR 番号 | 任意 | 指定時はその 1 件のみ |

## タスク

### ステップ 0: Monitor でイベント待機

対象 PR が既に存在する場合はそのままステップ 1 へ進む。
存在しない場合は Monitor ツールで以下のポーリングスクリプトを実行し、対象が出現したらステップ 1 へ進む。

対象条件: `wip` または `needs-fix` ラベル付きの Draft PR（`processing` 付きは除外）。

```bash
# Monitor に渡すポーリングスクリプト
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"

while true; do
  WIP_COUNT=$(gh pr list --state open --label "$LABEL_WIP" --draft \
    --json number,labels \
    --jq "[.[] | select(.labels | map(.name) | index(\"$LABEL_PROCESSING\") | not)] | length" 2>/dev/null || echo 0)
  FIX_COUNT=$(gh pr list --state open --label "$LABEL_NEEDS_FIX" --draft \
    --json number,labels \
    --jq "[.[] | select(.labels | map(.name) | index(\"$LABEL_PROCESSING\") | not)] | length" 2>/dev/null || echo 0)
  AVAILABLE=$((WIP_COUNT + FIX_COUNT))
  if [ "$AVAILABLE" -gt 0 ]; then
    echo "TRIGGER:pr-implement-auto:count=$AVAILABLE"
    break
  fi
  sleep 30
done
```

Monitor の stdout に `TRIGGER:pr-implement-auto` が来たらステップ 1 へ進む。
手動停止は TaskStop で行う。

### ステップ 1: 対象 PR を収集

`wip`（初回実装待ち）と `needs-fix`（レビューで差し戻された再実装待ち）の Draft PR
を両方拾う。gh CLI のラベル絞り込みは AND 扱いになるので 2 回呼んでマージする。

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
# 指定なしのとき
{
  gh pr list --state open --label "$LABEL_WIP" --draft \
    --json number,title,headRefName,baseRefName,body,labels --limit 50
  gh pr list --state open --label "$LABEL_NEEDS_FIX" --draft \
    --json number,title,headRefName,baseRefName,body,labels --limit 50
} | jq -s 'add | unique_by(.number)'
# 指定ありのとき
gh pr view {N} --json number,title,headRefName,baseRefName,body,labels,isDraft
```

`processing` 付きは除外。`isDraft: false` は対象外。昇順 → 上位 **N** 件。0 件なら停止。

### ステップ 2: 排他制御

`wip` / `needs-fix` どちらが付いていても外せるよう、両方 `--remove-label` する
（存在しないラベルを外そうとしてもエラーにはならない）。

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
gh pr edit {N} --add-label "$LABEL_PROCESSING" \
  --remove-label "$LABEL_WIP" --remove-label "$LABEL_NEEDS_FIX"
gh issue edit {N} --add-assignee @me
```

### ステップ 3: pr-implementer を並列起動

起動前に、紐づく Issue に `processing:pr-implement` を付与する。

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
# PR 本文から Issue 番号を抽出して付与
ISSUE_N=$(gh pr view {N} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
if [ -n "$ISSUE_N" ]; then
  gh issue edit "$ISSUE_N" --add-label "$LABEL_PROCESSING_PR_IMPLEMENT"
fi
```

[サブエージェントで並列実行・完了を待つ]
（戻り値: `[{branch, pr_number, status, needs_user_review, commits_added}]`）

### ステップ 4: 後処理

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"

# 成功
ARGS=(--remove-label "$LABEL_PROCESSING" --add-label "$LABEL_NEEDS_AI_REVIEW")
if [ "{needs_user_review}" = "true" ]; then
  ARGS+=(--add-label "$LABEL_NEEDS_USER_REVIEW")
fi
gh pr edit {N} "${ARGS[@]}"
# Issue の processing:pr-implement を除去
ISSUE_N=$(gh pr view {N} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
if [ -n "$ISSUE_N" ]; then
  gh issue edit "$ISSUE_N" --remove-label "$LABEL_PROCESSING_PR_IMPLEMENT"
fi

# 失敗
gh pr edit {N} --remove-label "$LABEL_PROCESSING" --add-label "$LABEL_NEEDS_FIX"
gh pr comment {N} --body "{失敗理由}"
ISSUE_N=$(gh pr view {N} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
if [ -n "$ISSUE_N" ]; then
  gh issue edit "$ISSUE_N" --remove-label "$LABEL_PROCESSING_PR_IMPLEMENT"
fi
```

### ステップ 5: pr-review-auto を連鎖実行

ステップ 4 で 1 件以上 `needs-ai-review` を付与した PR が存在すれば、続けて
`/gh-kit:pr-review-auto` を呼び出して直列レビュー → マージへ進める。

## 厳守事項

| No | 禁止 |
|---|---|
| 1 | マージしてはならない（マージは `pr-review-auto` の責務） |
| 2 | `processing` 付き PR を別セッションが触ってはならない |
| 3 | Draft 以外の PR は触らない |
| 4 | 新規ブランチ・新規 PR を作成しない |
