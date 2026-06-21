---
name: gh-kit:pr-draft-create-auto
description: needs-* なしの open Issue 全件から Draft PR を並列で作成する（1 Issue 複数派生対応）
disable-model-invocation: true
---

# pr-draft-create-auto

「実装着手 OK」になった Issue を全件巡回し、それぞれから Draft PR を作る。
1 Issue から複数派生してよい。実装は `/gh-kit:pr-implement-auto` が担当。

実装着手 OK の条件:

| No | 条件 |
|---|---|
| 1 | `state: open` |
| 2 | `gh-kit:needs-ai-review` / `gh-kit:needs-user-review` / `gh-kit:needs-fix` / `gh-kit:processing` のいずれも付いていない |
| 3 | Issue 本文・コメントの `- [ ]` がすべて埋まっている（推奨案・QA 回答が選択済み） |

!`cat "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"`

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

対象条件: `state: open` かつ `needs-ai-review` / `needs-user-review` / `needs-fix` / `processing` のいずれも付いていない Issue。

```bash
# Monitor に渡すポーリングスクリプト
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"

while true; do
  # needs-* / processing なし・open の Issue を取得
  AVAILABLE=$(gh issue list --state open \
    --json number,labels \
    --jq "[.[] | select(
      (.labels | map(.name) | (
        index(\"$LABEL_NEEDS_AI_REVIEW\") == null and
        index(\"$LABEL_NEEDS_USER_REVIEW\") == null and
        index(\"$LABEL_NEEDS_FIX\") == null and
        index(\"$LABEL_PROCESSING\") == null
      ))
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
gh issue list --state open --json number,title,body,labels,comments --limit 100
```

needs-* / gh-kit:processing いずれも含まず、`- [ ]` 残数 0 のものをフィルタ。0 件なら停止。

### ステップ 2: 各 Issue から作る Draft PR 数を決定

| 条件 | 作る PR 数 |
|---|---|
| `issue-reviewer` コメントに分割提案表あり | 分割提案表の行数 |
| 引数で分割スコープ指定あり | 指定数 |
| 上記なし | 1 |

並列実行待ち行列に積む（上限 **N**）。

### ステップ 3: 排他制御

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
gh issue edit {N} --add-label "$LABEL_PROCESSING"
```

### ステップ 4: pr-draft-creator を並列起動

[サブエージェントで並列実行・完了を待つ]
（戻り値: `[{branch, pr_url, pr_number}]`）

### ステップ 5: 後処理

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
gh pr edit {PR番号} --add-label "$LABEL_WIP"
gh issue comment {N} --body "PR #{番号} を起票（スコープ: {scope}）"
gh issue edit {N} --remove-label "$LABEL_PROCESSING" --add-label "$LABEL_PROCESSING_PR_DRAFT"
```

### ステップ 6: 完了報告

| 項目 | 内容 |
|---|---|
| 対象 Issue 件数 / 作成 PR 件数 | |
| 各 PR の URL と紐づく Issue | |
| 次アクション | `/gh-kit:pr-implement-auto` |
