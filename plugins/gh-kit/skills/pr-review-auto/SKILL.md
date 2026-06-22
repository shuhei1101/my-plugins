---
name: gh-kit:pr-review-auto
description: 確認:issue-reviewer または user-reviewed の Ready PR を 1 件ずつ直列でレビューし、合格 + assignees なしならマージまで実行
disable-model-invocation: true
---

# pr-review-auto

`確認:issue-reviewer` または `user-reviewed` 付き Ready PR をキューとして 1 件ずつ消化する。
**並列実行は絶対にしない**（master 取り込みとマージが競合してバグるため）。

PR に assignees が設定されている場合はレビューだけ実施してマージしない。
ユーザーが確認完了後に `user-reviewed` ラベルを付与して assignees を外すと、Monitor が検知してマージフローへ自動進行する。

## タスク

### ステップ -1: ラベルを冪等に用意する

```bash
gh label list | grep -q "^${GH_KIT_LABEL_USER_REVIEWED}" || \
  gh label create "$GH_KIT_LABEL_USER_REVIEWED" --color "$GH_KIT_LABEL_COLOR_USER_REVIEWED" --description "ユーザーがレビュー確認済み（マージ許可サイン）"
```

### ステップ 0: Monitor でイベント待機

対象 PR が既に存在する場合はそのままステップ 1 へ進む。
存在しない場合は Monitor ツールで以下のポーリングスクリプトを実行し、対象が出現したらステップ 1 へ進む。

対象条件: `確認:issue-reviewer` または `user-reviewed` ラベル付きの Ready（非 Draft）PR（`処理中` 付きは除外）。
直列制約は維持（Monitor 検知後もステップ 1→4 の直列ループを継続する）。

```bash
# Monitor に渡すポーリングスクリプト
while true; do
  # 確認:issue-reviewer 付き PR を収集
  AI_REVIEW=$(gh pr list --state open --label "$GH_KIT_LABEL_NEEDS_AI_REVIEW" \
    --json number,labels,isDraft \
    --jq "[.[] | select(
      .isDraft == false and
      (.labels | map(.name) | index(\"$GH_KIT_LABEL_PROCESSING\") | not)
    )] | length" 2>/dev/null || echo 0)
  # user-reviewed 付き PR を収集
  USER_REVIEWED=$(gh pr list --state open --label "$GH_KIT_LABEL_USER_REVIEWED" \
    --json number,labels,isDraft \
    --jq "[.[] | select(
      .isDraft == false and
      (.labels | map(.name) | index(\"$GH_KIT_LABEL_PROCESSING\") | not)
    )] | length" 2>/dev/null || echo 0)
  AVAILABLE=$((AI_REVIEW + USER_REVIEWED))
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

`確認:issue-reviewer` と `user-reviewed` の両方を対象とする。重複を排除してマージする。

```bash
# 確認:issue-reviewer 付き PR
AI_LIST=$(gh pr list --state open --label "$GH_KIT_LABEL_NEEDS_AI_REVIEW" \
  --json number,title,headRefName,baseRefName,statusCheckRollup,labels --limit 50)
# user-reviewed 付き PR
USER_LIST=$(gh pr list --state open --label "$GH_KIT_LABEL_USER_REVIEWED" \
  --json number,title,headRefName,baseRefName,statusCheckRollup,labels --limit 50)
# 重複除去してマージ（number で unique）
COMBINED=$(echo "$AI_LIST $USER_LIST" | jq -s '[.[][] ] | unique_by(.number)')
```

`処理中` 付きは除外。`優先度:急ぎ` 付き PR を先頭に、次に `優先度:いつでも` 付き、それ以外は番号昇順でキューを形成する:

```bash
# jq でラベル名に優先度:急ぎ を含むものを先頭に、次に優先度:いつでも、残りは番号昇順
jq --arg urgent "$GH_KIT_LABEL_PRIORITY_URGENT" --arg low "$GH_KIT_LABEL_PRIORITY_LOW" 'sort_by(
  if (.labels | map(.name) | index($urgent)) then 0
  elif (.labels | map(.name) | index($low)) then 1
  else 2
  end, .number
)'
```

### ステップ 2: 上から 1 件取り出す

```bash
gh pr edit {N} --add-label "$GH_KIT_LABEL_PROCESSING"
# 紐づく Issue に 処理中:pr-review を付与
ISSUE_N=$(gh pr view {N} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
if [ -n "$ISSUE_N" ]; then
  gh issue edit "$ISSUE_N" --add-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEW"
fi
```

CI が failure なら failed へ。

`user-reviewed` ラベルが付いている PR（ユーザーが確認済みサインを送った PR）かどうかを確認する:

```bash
HAS_USER_REVIEWED=$(gh pr view {N} --json labels \
  --jq "[.labels[].name] | index(\"$GH_KIT_LABEL_USER_REVIEWED\") | . != null")
```

- `HAS_USER_REVIEWED=true` の場合: AI レビュー済みとして扱い、ステップ 3 をスキップしてステップ 3-B（直接マージ）へ進む。
- `HAS_USER_REVIEWED=false` の場合: 通常通りステップ 3（pr-reviewer への委譲）へ進む。

### ステップ 3: pr-reviewer に委譲

[サブエージェントで実行・完了を待つ]
（戻り値: `{verdict, pr_number, branch, message, findings_count}`）

入力:
- PR 番号 / タイトル / base / head
- リポジトリ root
- 現在 assignees 一覧（有無を判定するのに使う）

### ステップ 3-B: user-reviewed PR の直接マージ（ステップ 3 をスキップ）

`user-reviewed` ラベル付き PR はすでに AI レビュー承認済みのため、pr-reviewer を再度呼ばずに直接 pr-reviewer スキルのマージステップ（ステップ 6）を実行する。

```bash
# pr-reviewer を assignees なし・approve 済みとして起動し、マージのみ実行させる
# （verdict = approved-merged を期待）
```

サブエージェント（pr-reviewer）を呼び出す際、`skip_review=true` フラグを渡してマージのみ実行するよう指示する。または pr-reviewer スキルのステップ 6 相当の操作（worktree 同期 → base 取り込み → マージ → push）を自前で実行する。

> **実装注**: `pr-reviewer` サブエージェントへの入力に「AI レビュー済み。マージのみ実行してください」と明示して委譲するのが最も安全。

### ステップ 4: 後処理

```bash
# 全 verdict 共通: Issue の 処理中:pr-review を除去
ISSUE_N=$(gh pr view {N} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
```

| verdict | 動作 |
|---|---|
| approved-merged | `gh pr edit {N} --remove-label "$GH_KIT_LABEL_PROCESSING" --remove-label "$GH_KIT_LABEL_NEEDS_AI_REVIEW" --remove-label "$GH_KIT_LABEL_USER_REVIEWED"`（マージは pr-reviewer が実施済み）+ `gh issue edit "$ISSUE_N" --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEW"` |
| approved-user-review-pending | `gh pr edit {N} --remove-label "$GH_KIT_LABEL_PROCESSING" --remove-label "$GH_KIT_LABEL_NEEDS_AI_REVIEW"`（assignees はそのまま残す。ユーザーが `user-reviewed` を付けて assignees を外すと次回 Monitor が検知してマージへ自動進行）+ `gh issue edit "$ISSUE_N" --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEW"` |
| changes-requested | `gh pr edit {N} --remove-label "$GH_KIT_LABEL_PROCESSING" --add-label "$GH_KIT_LABEL_NEEDS_FIX"` + `gh issue edit "$ISSUE_N" --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEW"` |
| conflict / failed | `GH_LOGIN="$(gh api user --jq '.login')" && gh pr edit {N} --remove-label "$GH_KIT_LABEL_PROCESSING" --add-label "$GH_KIT_LABEL_NEEDS_FIX" --add-assignee "$GH_LOGIN" && gh pr comment {N} --body "{詳細}"` + `gh issue edit "$ISSUE_N" --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEW"` |

ステップ 2 に戻ってキューが空になるまで繰り返す。

### ステップ 5: 完了報告

| 項目 | 内容 |
|---|---|
| 処理 PR 件数 | カテゴリ別 |
| 残った PR | 各カテゴリの番号一覧 |
