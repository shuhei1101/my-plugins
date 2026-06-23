---
name: gh-kit:pr-plan-auto
description: 確認:pr-plan ラベル付き open Issue（processing:* なし）を全件巡回し Draft PR を並列で作成する（1 Issue 複数派生対応）
disable-model-invocation: true
---

# pr-plan-auto

「実装着手 OK」になった Issue を全件巡回し、それぞれから Draft PR を作る。
1 Issue から複数派生してよい。実装は `/gh-kit:pr-implement-auto` が担当。

実装着手 OK の条件:

| No | 条件 |
|---|---|
| 1 | `state: open` |
| 2 | `確認:pr-plan` ラベルが付いている |
| 3 | `処理中` で始まるラベル（`処理中:pr-planner`・`処理中:pr-implementer`・`処理中:pr-reviewer`・`処理中:pr-merger` 等）のいずれも付いていない |

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_KIT_PR_PLAN_PARALLEL` | `5` | 並列起動上限 |

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| Issue 番号 | 任意 | 指定時はその 1 件のみ |
| 分割スコープ | 任意 | カンマ区切り |

## タスク

### ステップ 0: Monitor でイベント待機

対象 Issue が既に存在する場合はそのままステップ 1 へ進む。
存在しない場合は Monitor ツールで以下のポーリングスクリプトを実行し、対象が出現したらステップ 1 へ進む。

対象条件: `state: open` かつ `確認:pr-plan` ラベルが付いていて、`処理中:` で始まるラベルのいずれも付いていない Issue。

```bash
# Monitor に渡すポーリングスクリプト
while true; do
  # 確認:pr-plan 付き・処理中:* なし・open の Issue を取得
  AVAILABLE=$(gh issue list --state open \
    --label "$GH_KIT_LABEL_CONFIRM_PR_PLANNER" \
    --json number,labels \
    --jq "[.[] | select(
      (.labels | map(.name) | (
        (map(startswith(\"処理中:\")) | any | not)
      ))
    )] | length" 2>/dev/null || echo 0)
  if [ "$AVAILABLE" -gt 0 ]; then
    echo "TRIGGER:pr-plan-auto:count=$AVAILABLE"
    break
  fi
  sleep 30
done
```

Monitor の stdout に `TRIGGER:pr-plan-auto` が来たらステップ 1 へ進む。
手動停止は TaskStop で行う。

### ステップ 1: 対象 Issue を収集

```bash
gh issue list --state open --label "$GH_KIT_LABEL_CONFIRM_PR_PLANNER" \
  --json number,title,body,labels,assignees,comments --limit 100
```

`確認:pr-plan` ラベルが付いていて、`処理中:` で始まるラベル（`処理中:pr-planner`・`処理中:pr-implementer`・`処理中:pr-reviewer`・`処理中:pr-merger` 等）のいずれも含まないものをフィルタ。0 件なら停止。

jq フィルタ例:
```bash
# 処理中: prefix 一括除外: startswith("処理中:") でマッチするラベルがひとつでもあれば除外
select(
  (.labels | map(.name) | (
    index("確認:pr-plan") != null and
    (map(startswith("処理中:")) | any | not)
  ))
)
```

フィルタ後、`優先度:急ぎ` ラベルが付いている Issue を先頭に並べ、次に `優先度:いつでも` 付き、それ以外は番号昇順で処理する:

```bash
# jq でラベル名に優先度:急ぎ を含むものを先頭に、次に優先度:いつでも、残りは番号昇順
jq --arg urgent "$GH_KIT_LABEL_PRIORITY_URGENT" --arg low "$GH_KIT_LABEL_PRIORITY_LOW" 'sort_by(
  if (.labels | map(.name) | index($urgent)) then 0
  elif (.labels | map(.name) | index($low)) then 1
  else 2
  end, .number
)'
```

### ステップ 2: 各 Issue から作る Draft PR 数を決定

| 条件 | 作る PR 数 |
|---|---|
| `issue-reviewer` コメントに分割提案表あり | 分割提案表の行数 |
| 引数で分割スコープ指定あり | 指定数 |
| 上記なし | 1 |

並列実行待ち行列に積む（上限 **N**）。

### ステップ 3: 排他制御

```bash
gh issue edit {N} --add-label "$GH_KIT_LABEL_PROCESSING_PR_PLANNER"
```

### ステップ 4: pr-planner をバックグラウンドで並列起動（完了を待たない・通知駆動）

**原則: 完了を待たない。** `run_in_background: true` でサブエージェントを起動したら即座に Monitor 監視に戻る。
完了通知（`<task-notification>`）を受けたら後処理（ステップ 5）を実行する。

各 Issue に対して `pr-planner` サブエージェントを `run_in_background: true` で起動する:
- 起動上限 **N**（`GH_KIT_PR_PLAN_PARALLEL`）に達している場合は新規起動をキューイングし、1 体完了通知を受けたら次を起動する
- 起動後は即座に Monitor に制御を戻す

### ステップ 5: 通知ハンドラ（サブエージェント完了時に実行）

`pr-planner` からの完了通知（`<task-notification>`）を受信したら以下を実行する:
（戻り値: `{branch, pr_url, pr_number}` を通知から取得）

```bash
gh pr edit {PR番号} --add-label "$GH_KIT_LABEL_WIP"
gh issue comment {N} --body "PR #{番号} を起票（スコープ: {scope}）"
# 処理中:pr-planner は排他制御（ステップ 3）で付与済みのため、ここでは何もしない
```

後処理完了後、キューに積まれた次の Issue があれば `pr-planner` を起動する。

### ステップ 6: 完了報告

| 項目 | 内容 |
|---|---|
| 対象 Issue 件数 / 作成 PR 件数 | |
| 各 PR の URL と紐づく Issue | |
| 次アクション | `/gh-kit:pr-implement-auto` |
