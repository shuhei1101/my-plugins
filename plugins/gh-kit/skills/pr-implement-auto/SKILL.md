---
name: gh-kit:pr-implement-auto
description: ラベル wip / 確認:pr-implementer の Draft PR を N 件並列で実装し、Ready 化 → そのまま pr-review-auto に連鎖
disable-model-invocation: true
---

# pr-implement-auto

`pr-draft-create-auto` で雛形化された Draft PR を拾い、中身を実装して Ready for review に切り替える。

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

対象条件: `wip` または `確認:pr-implementer` ラベル付きの Draft PR（`処理中` 付きは除外）。

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

`wip`（初回実装待ち）と `確認:pr-implementer`（レビューで差し戻された再実装待ち）の Draft PR
を両方拾う。gh CLI のラベル絞り込みは AND 扱いになるので 2 回呼んでマージする。

```bash
# 指定なしのとき
{
  gh pr list --state open --label "$GH_KIT_LABEL_WIP" --draft \
    --json number,title,headRefName,baseRefName,body,labels --limit 50
  gh pr list --state open --label "$GH_KIT_LABEL_NEEDS_FIX" --draft \
    --json number,title,headRefName,baseRefName,body,labels --limit 50
} | jq -s 'add | unique_by(.number)'
# 指定ありのとき
gh pr view {N} --json number,title,headRefName,baseRefName,body,labels,isDraft
```

`処理中` 付きは除外。`isDraft: false` は対象外。0 件なら停止。

収集後、`優先度:急ぎ` ラベルが付いている PR を先頭に並べ、次に `優先度:いつでも` 付き、それ以外の順（番号昇順）で処理する:

```bash
# jq でラベル名に優先度:急ぎ を含むものを先頭に、次に優先度:いつでも、残りは番号昇順
jq --arg urgent "$GH_KIT_LABEL_PRIORITY_URGENT" --arg low "$GH_KIT_LABEL_PRIORITY_LOW" 'sort_by(
  if (.labels | map(.name) | index($urgent)) then 0
  elif (.labels | map(.name) | index($low)) then 1
  else 2
  end, .number
)'
```

上記ソート後、上位 **N** 件を対象とする。

### ステップ 2: 排他制御

`wip` / `確認:pr-implementer` どちらが付いていても外せるよう、両方 `--remove-label` する
（存在しないラベルを外そうとしてもエラーにはならない）。

```bash
gh pr edit {N} --add-label "$GH_KIT_LABEL_PROCESSING" \
  --remove-label "$GH_KIT_LABEL_WIP" --remove-label "$GH_KIT_LABEL_NEEDS_FIX"
```

### ステップ 3: pr-test-creator を先行起動（テストタスクがある場合）

起動前に、紐づく Issue に `処理中:pr-implement` を付与する。

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
# PR 本文から Issue 番号を抽出して付与
ISSUE_N=$(gh pr view {N} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
if [ -n "$ISSUE_N" ]; then
  gh issue edit "$ISSUE_N" --add-label "$GH_KIT_LABEL_PROCESSING_PR_IMPLEMENT"
fi
```

PR 本文の「実装予定タスク」に「自動テスト作成/変更」チェックボックスが含まれ、かつ未完了（`- [ ] 自動テスト作成`）の場合は、`pr-test-creator` を先行起動してテストコードを作成させる。

```bash
# テストタスクの存在確認
gh pr view {N} --json body --jq '.body' | grep -q "- \[ \] 自動テスト作成" && HAS_TEST_TASK=true || HAS_TEST_TASK=false
```

`HAS_TEST_TASK=true` の場合: `pr-test-creator` サブエージェントを起動し、完了を待ってから `pr-implementer` を起動する（直列）。
`HAS_TEST_TASK=false` の場合: `pr-implementer` を直接起動する。

### ステップ 3a: pr-implementer を並列起動

`pr-test-creator` の完了後（またはテストタスクなしの場合はステップ 3 完了後）に `pr-implementer` を起動する。

[サブエージェントで並列実行・完了を待つ]
（戻り値: `[{branch, pr_number, status, needs_user_review, commits_added}]`）

### ステップ 4: 後処理

```bash
# 成功
gh pr edit {N} --remove-label "$GH_KIT_LABEL_PROCESSING" --add-label "$GH_KIT_LABEL_NEEDS_AI_REVIEW"
if [ "{needs_user_review}" = "true" ]; then
  GH_LOGIN="$(gh api user --jq '.login')"
  gh pr edit {N} --add-assignee "$GH_LOGIN"
fi
# Issue の 処理中:pr-implement を除去
ISSUE_N=$(gh pr view {N} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
if [ -n "$ISSUE_N" ]; then
  gh issue edit "$ISSUE_N" --remove-label "$GH_KIT_LABEL_PROCESSING_PR_IMPLEMENT"
fi

# 失敗
gh pr edit {N} --remove-label "$GH_KIT_LABEL_PROCESSING" --add-label "$GH_KIT_LABEL_NEEDS_FIX"
gh pr comment {N} --body "{失敗理由}"
ISSUE_N=$(gh pr view {N} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
if [ -n "$ISSUE_N" ]; then
  gh issue edit "$ISSUE_N" --remove-label "$GH_KIT_LABEL_PROCESSING_PR_IMPLEMENT"
fi
```

### ステップ 5: pr-review-auto を連鎖実行

ステップ 4 で 1 件以上 `確認:issue-reviewer` を付与した PR が存在すれば、続けて
`/gh-kit:pr-review-auto` を呼び出して直列レビュー → マージへ進める。

## 厳守事項

| No | 禁止 |
|---|---|
| 1 | マージしてはならない（マージは `pr-review-auto` の責務） |
| 2 | `処理中` 付き PR を別セッションが触ってはならない |
| 3 | Draft 以外の PR は触らない |
| 4 | 新規ブランチ・新規 PR を作成しない |
