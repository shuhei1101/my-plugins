---
name: gh-kit:pr-review-auto
description: 確認:pr-reviewer（GH_KIT_LABEL_CONFIRM_PR_REVIEW）ラベル付き PR を 1 件ずつ直列でレビューし、合格 + assignees なしなら 確認:pr-merger ラベルを付与する
disable-model-invocation: true
---

# pr-review-auto

`確認:pr-reviewer`（`$GH_KIT_LABEL_CONFIRM_PR_REVIEW`）付き PR をキューとして 1 件ずつ消化する（Draft・Ready 問わず）。
**並列実行は絶対にしない**（master 取り込みとマージが競合してバグるため）。

PR に assignees が設定されている場合はレビューだけ実施してマージしない。
ユーザーが確認完了後に `user-reviewed` ラベルを付与して assignees を外すと、Monitor が検知してマージフローへ自動進行する。
マージは `pr-merger-auto` が `確認:pr-merger` ラベルを検知して実行する。

## ラベル遷移表

gh-kit フローにおけるラベルの移り変わりを示す。

| フェーズ | PR ラベル | Issue ラベル | 付与者 | 使用変数 |
|---|---|---|---|---|
| Issue 起票直後 | — | `確認:issue-reviewer` | `issue-create` スキル | `$GH_KIT_LABEL_CONFIRM_ISSUE_REVIEW` |
| Issue レビュー中 | — | `確認:issue-reviewer` 除去 + `処理中:issue-reviewer` | `issue-review-auto` | `$GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER` |
| Issue レビュー完了 | — | `処理中:issue-reviewer` 除去、`確認:issue-reviewer` 除去 | `issue-review-auto` | — |
| Draft PR 作成中 | `処理中:pr-planner` | `処理中:pr-planner` | `pr-plan-auto` | `$GH_KIT_LABEL_PROCESSING_PR_PLANNER` |
| Draft PR 作成完了 | `処理中:pr-planner` 除去 + `確認:pr-plan-reviewer` | — | `pr-plan-auto` | `$GH_KIT_LABEL_CONFIRM_PR_PLAN_REVIEWER` |
| PR プランレビュー待ち | `確認:pr-plan-reviewer` | — | `pr-plan-auto` | `$GH_KIT_LABEL_CONFIRM_PR_PLAN_REVIEWER` |
| PR プランレビュー中 | `確認:pr-plan-reviewer` 除去 + `処理中:pr-plan-reviewer` | — | `pr-plan-review-auto` | `$GH_KIT_LABEL_PROCESSING_PR_PLAN_REVIEWER` |
| PR プランレビュー合格 | `処理中:pr-plan-reviewer` 除去 + `確認:pr-implementer` | — | `pr-plan-review-auto` | `$GH_KIT_LABEL_CONFIRM_PR_IMPLEMENTER` |
| 実装中 | `確認:pr-implementer` 除去 + `処理中:pr-implementer` | `処理中:pr-implementer` | `pr-implement-auto` | `$GH_KIT_LABEL_PROCESSING_PR_IMPLEMENTER` |
| 実装完了（Ready 化） | `処理中:pr-implementer` 除去 + `確認:pr-reviewer` | — | `pr-implement-auto`（ステップ 4） | `$GH_KIT_LABEL_CONFIRM_PR_REVIEW` |
| 実装失敗 | `処理中:pr-implementer` 除去 + `確認:pr-reviewer` | — | `pr-implement-auto`（ステップ 4） | `$GH_KIT_LABEL_CONFIRM_PR_REVIEW` |
| 実装差し戻し（再実装待ち） | `処理中:pr-reviewer` 除去 + `確認:pr-implementer` | — | `pr-review-auto`（ステップ 4） | `$GH_KIT_LABEL_CONFIRM_PR_IMPLEMENT` |
| PR レビュー中 | `確認:pr-reviewer` 除去 + `処理中:pr-reviewer` | `処理中:pr-reviewer` | `pr-review-auto` | `$GH_KIT_LABEL_CONFIRM_PR_REVIEW`, `$GH_KIT_LABEL_PROCESSING_PR_REVIEWER` |
| PR レビュー: ユーザー確認待ち | `処理中:pr-reviewer` 除去 + assignees | — | `pr-review-auto` / `pr-reviewer` | — |
| ユーザー確認完了 | `user-reviewed` + `確認:pr-merger` | — | ユーザー手動 + `pr-review-auto` | `$GH_KIT_LABEL_USER_REVIEWED`, `$GH_KIT_LABEL_CONFIRM_PR_MERGER` |
| マージ待ち | `確認:pr-merger` | — | `pr-reviewer` スキル | `$GH_KIT_LABEL_CONFIRM_PR_MERGER` |
| マージ中 | `確認:pr-merger` 除去 + `処理中:pr-merger` | — | `pr-merger-auto` | `$GH_KIT_LABEL_PROCESSING_PR_MERGER` |
| マージ完了 | （PR Close） | `処理中:*` 除去 + （Issue Close） | `pr-merger` スキル | — |

> **注記:** Issue レビュー用ラベル `確認:issue-reviewer`（`$GH_KIT_LABEL_CONFIRM_ISSUE_REVIEW`）と PR レビュー待ちラベル `確認:pr-reviewer`（`$GH_KIT_LABEL_CONFIRM_PR_REVIEW`）は用途が異なる別個のラベル。
> - Issue フェーズ: `確認:issue-reviewer` → `issue-review-auto` が検知・処理
> - PR フェーズ: `確認:pr-reviewer` → `pr-review-auto` が検知・処理

## ループ継続制約（厳守）

- Monitorは何があっても絶対に止めない。
- ステップ 4 完了後（キューが空になった場合も含む）は**即座にステップ 0（Monitor）へ戻る。**
- **途中結果報告は禁止。** ステップ 4 の後処理が終わったら報告せず次のポーリングサイクルへ。
- ステップ 5 はステップ 4 の通常完了フローとは別に、TaskStop を受信したときにのみ実行する。

## タスク

### ステップ -1: ラベルを冪等に用意する

```bash
gh label list | grep -q "^${GH_KIT_LABEL_USER_REVIEWED}" || \
  gh label create "$GH_KIT_LABEL_USER_REVIEWED" --color "$GH_KIT_LABEL_COLOR_USER_REVIEWED" --description "ユーザーがレビュー確認済み（マージ許可サイン）"
```

### ステップ 0: Monitor でイベント待機

対象 PR が既に存在する場合はそのままステップ 1 へ進む。
存在しない場合は Monitor ツールで以下のポーリングスクリプトを実行し、対象が出現したらステップ 1 へ進む。

対象条件: `確認:pr-reviewer`（`$GH_KIT_LABEL_CONFIRM_PR_REVIEW`）ラベル付きの PR（Draft・Ready 問わず、`処理中:` で始まるラベル付きは除外）。
直列制約は維持（Monitor 検知後もステップ 1→4 の直列ループを継続する）。

**ステップ 4 のキューが空になったらこのステップに戻り、Monitor を再起動してポーリングを継続する。**

```bash
# Monitor に渡すポーリングスクリプト
while true; do
  AVAILABLE=$(gh pr list --state open --label "$GH_KIT_LABEL_CONFIRM_PR_REVIEW" \
    --json number,labels \
    --jq "[.[] | select(
      (.labels | map(.name) | (map(startswith(\"処理中:\")) | any | not))
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

`確認:pr-reviewer`（`$GH_KIT_LABEL_CONFIRM_PR_REVIEW`）ラベル付きの PR を対象とする（Draft・Ready 問わず）。

```bash
gh pr list --state open --label "$GH_KIT_LABEL_CONFIRM_PR_REVIEW" \
  --json number,title,headRefName,baseRefName,statusCheckRollup,labels --limit 50
```

`処理中:` で始まるラベル（`処理中:pr-reviewer`・`処理中:pr-implementer`・`処理中:pr-planner`・`処理中:pr-merger` 等）付きは除外。`優先度:急ぎ` 付き PR を先頭に、次に `優先度:いつでも` 付き、それ以外は番号昇順でキューを形成する:

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
# 自身に依頼された確認ラベルを除去し、処理中ラベルを付与する
gh pr edit {N} \
  --remove-label "$GH_KIT_LABEL_CONFIRM_PR_REVIEW" \
  --add-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEWER"
# 紐づく Issue に 処理中:pr-reviewer を付与
ISSUE_N=$(gh pr view {N} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
if [ -n "$ISSUE_N" ]; then
  gh issue edit "$ISSUE_N" --add-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEWER"
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
# 全 verdict 共通: Issue の 処理中:pr-reviewer を除去
ISSUE_N=$(gh pr view {N} --json body --jq '.body' | grep -oP '(?:Refs|Closes|Fixes) #\K[0-9]+' | head -1)
```

| verdict | 動作 |
|---|---|
| approved-merge-ok | `gh pr edit {N} --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEWER" --remove-label "$GH_KIT_LABEL_CONFIRM_PR_REVIEW" --remove-label "$GH_KIT_LABEL_USER_REVIEWED"`（`確認:pr-merger` ラベルは pr-reviewer が付与済み。マージは pr-merger-auto が実行する）+ `gh issue edit "$ISSUE_N" --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEWER"` |
| approved-user-review-pending | `gh pr edit {N} --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEWER" --remove-label "$GH_KIT_LABEL_CONFIRM_PR_REVIEW"`（assignees はそのまま残す。ユーザーが `user-reviewed` を付けて assignees を外すと次回 Monitor が検知してマージへ自動進行）+ `gh issue edit "$ISSUE_N" --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEWER"` |
| needs-fix | `gh pr edit {N} --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEWER" --add-label "$GH_KIT_LABEL_CONFIRM_PR_IMPLEMENT"` + `gh issue edit "$ISSUE_N" --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEWER"`（PR 本文の `- [ ]` 未消化による差し戻し。`確認:pr-implementer`（`$GH_KIT_LABEL_CONFIRM_PR_IMPLEMENT`）ラベルが付与された状態で `pr-implement-auto` の次回実行を待つ） |
| changes-requested | `gh pr edit {N} --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEWER" --add-label "$GH_KIT_LABEL_CONFIRM_PR_IMPLEMENT"` + `gh issue edit "$ISSUE_N" --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEWER"` |
| failed | `GH_LOGIN="$(gh api user --jq '.login')" && gh pr edit {N} --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEWER" --add-label "$GH_KIT_LABEL_CONFIRM_PR_IMPLEMENT" --add-assignee "$GH_LOGIN" && gh pr comment {N} --body "{詳細}"` + `gh issue edit "$ISSUE_N" --remove-label "$GH_KIT_LABEL_PROCESSING_PR_REVIEWER"` |

ステップ 2 に戻ってキューが空になるまで繰り返す。
キューが空になったらステップ 0（Monitor）へ戻り、次のイベントを待機する。

### ステップ 5: 完了報告（TaskStop 受信後のみ実行）

**このステップは TaskStop を受け取った場合にのみ実行する。キューが空になっただけでは実行しない。**

| 項目 | 内容 |
|---|---|
| 処理 PR 件数 | カテゴリ別 |
| 残った PR | 各カテゴリの番号一覧 |
