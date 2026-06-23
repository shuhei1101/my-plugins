---
name: gh-kit:pr-plan-review-auto
description: 確認:pr-plan-reviewer ラベル付き Draft PR を全件巡回し、pr-plan-reviewer に委譲して PR プランをレビューする。合格時は 確認:pr-implementer ラベルを付与して実装フローに引き渡す。
disable-model-invocation: true
---

# pr-plan-review-auto

`確認:pr-plan-reviewer` ラベル付き Draft PR を全件巡回し、PR プランをレビューする。
実装コードのレビューは行わない（それは `pr-review-auto` の責務）。

## ラベル遷移（このスキルに関係する部分）

| フェーズ | PR ラベル | 付与者 |
|---|---|---|
| Draft PR 作成直後 | `wip` | `pr-plan-auto` |
| PR プランレビュー待ち | `確認:pr-plan-reviewer` | ユーザーまたは将来の自動化 |
| PR プランレビュー中 | `処理中:pr-plan-reviewer` | このスキル（ステップ 2） |
| レビュー合格 | `確認:pr-implementer`（`処理中:pr-plan-reviewer` 除去） | このスキル（ステップ 4） |
| レビュー不合格 | `修正が必要`（`処理中:pr-plan-reviewer` 除去） | このスキル（ステップ 4） |

> **注記:** `wip` ラベルはこのスキルでは除去しない。`pr-implement-auto` の排他制御のため、実装開始時に除去する。

## タスク

### ステップ 0: Monitor でイベント待機

対象 PR が既に存在する場合はそのままステップ 1 へ進む。
存在しない場合は Monitor ツールで以下のポーリングスクリプトを実行し、対象が出現したらステップ 1 へ進む。

対象条件: `確認:pr-plan-reviewer` ラベル付きの Draft PR（`処理中:` で始まるラベル付きは除外）。

```bash
# Monitor に渡すポーリングスクリプト
while true; do
  AVAILABLE=$(gh pr list --state open --label "$GH_KIT_LABEL_CONFIRM_PR_PLAN_REVIEWER" \
    --json number,labels,isDraft \
    --jq "[.[] | select(
      .isDraft == true and
      (.labels | map(.name) | (map(startswith(\"処理中:\")) | any | not))
    )] | length" 2>/dev/null || echo 0)
  if [ "$AVAILABLE" -gt 0 ]; then
    echo "TRIGGER:pr-plan-review-auto:count=$AVAILABLE"
    break
  fi
  sleep 30
done
```

Monitor の stdout に `TRIGGER:pr-plan-review-auto` が来たらステップ 1 へ進む。
手動停止は TaskStop で行う。

### ステップ 1: 対象 PR を収集

```bash
gh pr list --state open --label "$GH_KIT_LABEL_CONFIRM_PR_PLAN_REVIEWER" \
  --json number,title,headRefName,baseRefName,labels,isDraft --limit 50
```

`isDraft: true` かつ `処理中:` で始まるラベルを含まないものをフィルタ。0 件なら停止。

`優先度:急ぎ` ラベルが付いている PR を先頭に、次に `優先度:いつでも` 付き、それ以外は番号昇順で処理する:

```bash
jq --arg urgent "$GH_KIT_LABEL_PRIORITY_URGENT" --arg low "$GH_KIT_LABEL_PRIORITY_LOW" 'sort_by(
  if (.labels | map(.name) | index($urgent)) then 0
  elif (.labels | map(.name) | index($low)) then 1
  else 2
  end, .number
)'
```

### ステップ 2: 排他制御

```bash
gh pr edit {N} \
  --add-label "$GH_KIT_LABEL_PROCESSING_PR_PLAN_REVIEWER" \
  --remove-label "$GH_KIT_LABEL_CONFIRM_PR_PLAN_REVIEWER"
```

### ステップ 3: pr-plan-reviewer に委譲（直列）

`pr-plan-reviewer` サブエージェントを起動し、完了を待つ。
（戻り値: `{verdict, pr_number, issue_number, findings_count, message}`）

入力:
- PR 番号
- base ブランチ

### ステップ 4: 後処理

```bash
# 共通: 処理中:pr-plan-reviewer を除去
gh pr edit {N} --remove-label "$GH_KIT_LABEL_PROCESSING_PR_PLAN_REVIEWER"
```

| verdict | 動作 |
|---|---|
| `approved` | `gh pr edit {N} --add-label "$GH_KIT_LABEL_CONFIRM_PR_IMPLEMENTER"` — `pr-implement-auto` が拾って実装開始 |
| `needs-revision` | `gh pr edit {N} --add-label "$GH_KIT_LABEL_NEEDS_FIX"` — PR 作成者が修正後に `確認:pr-plan-reviewer` を再付与 |
| `failed` | `GH_LOGIN="$(gh api user --jq '.login')" && gh pr edit {N} --add-label "$GH_KIT_LABEL_NEEDS_FIX" --add-assignee "$GH_LOGIN"` |

ステップ 1 に戻りキューが空になるまで繰り返す。

### ステップ 5: 完了報告

| 項目 | 内容 |
|---|---|
| 処理 PR 件数 | verdict 別（approved / needs-revision / failed） |
| 各 PR の URL と紐づく Issue | |
| 次アクション | `approved` 件数 > 0 なら `/gh-kit:pr-implement-auto` |

## 環境変数

| 変数 | 内容 |
|---|---|
| `GH_KIT_LABEL_CONFIRM_PR_PLAN_REVIEWER` | `確認:pr-plan-reviewer` |
| `GH_KIT_LABEL_PROCESSING_PR_PLAN_REVIEWER` | `処理中:pr-plan-reviewer` |
| `GH_KIT_LABEL_CONFIRM_PR_IMPLEMENTER` | `確認:pr-implementer` |
| `GH_KIT_LABEL_NEEDS_FIX` | `修正が必要` |

## 厳守事項

| No | 禁止 |
|---|---|
| 1 | 実装はしない |
| 2 | マージはしない |
| 3 | `wip` ラベルを除去しない |
| 4 | Draft 以外の PR は触らない |
