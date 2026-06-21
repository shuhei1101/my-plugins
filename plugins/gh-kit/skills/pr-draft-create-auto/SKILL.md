---
name: gh-kit:pr-draft-create-auto
description: needs-* なしかつ assignees 空の open Issue 全件から Draft PR を並列で作成する（1 Issue 複数派生対応）
disable-model-invocation: true
---

# pr-draft-create-auto

「実装着手 OK」になった Issue を全件巡回し、それぞれから Draft PR を作る。
1 Issue から複数派生してよい。実装は `/gh-kit:pr-implement-auto` が担当。

実装着手 OK の条件:

| No | 条件 |
|---|---|
| 1 | `state: open` |
| 2 | `確認:issue-reviewer` / `確認:pr-implementer` / `処理中` のいずれも付いていない |
| 3 | `assignees` が空（ユーザー確認待ちでない） |
| 4 | Issue 本文・コメントの `- [ ]` がすべて埋まっている（推奨案・QA 回答が選択済み） |

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_KIT_PR_DRAFT_CREATE_PARALLEL` | `5` | 並列起動上限 |

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| Issue 番号 | 任意 | 指定時はその 1 件のみ |
| 分割スコープ | 任意 | カンマ区切り |

## タスク

### ステップ 0: Monitor でイベント待機

対象 Issue が既に存在する場合はそのままステップ 1 へ進む。
存在しない場合は Monitor ツールで以下のポーリングスクリプトを実行し、対象が出現したらステップ 1 へ進む。

対象条件: `state: open` かつ `確認:issue-reviewer` / `確認:pr-implementer` / `処理中` のいずれも付いていない Issue かつ `assignees` が空。

```bash
# Monitor に渡すポーリングスクリプト
while true; do
  # 確認:* / 処理中 なし・open の Issue を取得
  AVAILABLE=$(gh issue list --state open \
    --json number,labels \
    --jq "[.[] | select(
      (.labels | map(.name) | (
        index(\"$GH_KIT_LABEL_NEEDS_AI_REVIEW\") == null and
        index(\"$GH_KIT_LABEL_NEEDS_FIX\") == null and
        index(\"$GH_KIT_LABEL_PROCESSING\") == null
      )) and
      (.assignees | length == 0)
    )] | length" 2>/dev/null || echo 0)
  if [ "$AVAILABLE" -gt 0 ]; then
    echo "TRIGGER:pr-draft-create-auto:count=$AVAILABLE"
    break
  fi
  sleep 30
done
```

Monitor の stdout に `TRIGGER:pr-draft-create-auto` が来たらステップ 1 へ進む。
手動停止は TaskStop で行う。

### ステップ 1: 対象 Issue を収集

```bash
gh issue list --state open --json number,title,body,labels,assignees,comments --limit 100
```

`確認:issue-reviewer` / `確認:pr-implementer` / `処理中` のいずれも含まず、`assignees` が空で、`- [ ]` 残数 0 のものをフィルタ。0 件なら停止。

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
gh issue edit {N} --add-label "$GH_KIT_LABEL_PROCESSING"
```

### ステップ 4: pr-draft-creator を並列起動

[サブエージェントで並列実行・完了を待つ]
（戻り値: `[{branch, pr_url, pr_number}]`）

### ステップ 5: 後処理

```bash
gh pr edit {PR番号} --add-label "$GH_KIT_LABEL_WIP"
gh issue comment {N} --body "PR #{番号} を起票（スコープ: {scope}）"
gh issue edit {N} --remove-label "$GH_KIT_LABEL_PROCESSING" --add-label "$GH_KIT_LABEL_PROCESSING_PR_DRAFT"
```

### ステップ 6: 完了報告

| 項目 | 内容 |
|---|---|
| 対象 Issue 件数 / 作成 PR 件数 | |
| 各 PR の URL と紐づく Issue | |
| 次アクション | `/gh-kit:pr-implement-auto` |
