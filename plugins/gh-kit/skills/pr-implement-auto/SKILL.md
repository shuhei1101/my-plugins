---
name: gh-kit:pr-implement-auto
description: ラベル `wip` の Draft PR を上から N 件取り、pr-implementer で実装 → Ready 化する
---

# pr-implement-auto

`/gh-kit:pr-wip-create` で雛形化された Draft PR を拾い、中身を実装して Ready for review に切り替えるバッチスキル。**マージはしない**（マージは `/gh-kit:pr-review-auto` の責務）。

## 環境変数

| 変数 | 既定 | 用途 |
|---|---|---|
| `GH_KIT_PR_IMPLEMENT_PARALLEL` | `5` | 並列起動するサブエージェント上限件数 |

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| PR 番号 | 任意 | 指定時はその 1 件のみ処理 |

## ラベル定義の読み込み

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
```

## タスク

### ステップ 1: 対象 PR を収集

| 状況 | コマンド |
|---|---|
| PR 番号指定あり | `gh pr view {N} --json number,title,headRefName,baseRefName,body,labels,isDraft`（`isDraft: false` ならエラー報告して停止） |
| 指定なし | `gh pr list --state open --label "$LABEL_WIP" --draft --json number,title,headRefName,baseRefName,body,labels --limit 50` |

`processing` がついた PR は除外（他セッションが触っている）。
昇順 → 上位 **N** 件。

0 件なら停止。

### ステップ 2: 排他制御

```bash
gh pr edit {N} --add-label "$LABEL_PROCESSING" --remove-label "$LABEL_WIP"
gh issue edit {N} --add-assignee @me  # PR は issue 系コマンドで assignee 操作可
```

### ステップ 3: pr-implementer を並列起動

[サブエージェントで並列実行・完了を待つ] N 件それぞれに `pr-implementer` サブエージェントを起動する。
（戻り値: `[{branch, pr_number, status, needs_user_review, commits_added}]`）

各サブエージェントに渡す入力:
- PR 番号 / ブランチ名 / base
- 紐づく Issue 番号（PR 本文の `Refs #N`）
- 採用方針（Issue コメントの `issue-review` 結果から抽出）
- 分割スコープ（PR 本文の説明）

### ステップ 4: 後処理

| 結果 | 動作 |
|---|---|
| ready | `processing` を外し、`needs-ai-review` を必ず付与。サブエージェントの `needs_user_review: true` 戻り値があれば `needs-user-review` も付与 |
| failed | `processing` を外し、`needs-fix` を付与。失敗理由を PR にコメント |

```bash
# 成功ケース
ARGS=(--remove-label "$LABEL_PROCESSING" --add-label "$LABEL_NEEDS_AI_REVIEW")
if [ "{needs_user_review}" = "true" ]; then
  ARGS+=(--add-label "$LABEL_NEEDS_USER_REVIEW")
fi
gh pr edit {N} "${ARGS[@]}"

# 失敗ケース
gh pr edit {N} --remove-label "$LABEL_PROCESSING" --add-label "$LABEL_NEEDS_FIX"
gh pr comment {N} --body "{失敗理由}"
```

### ステップ 5: 完了報告

| No | 報告項目 |
|---|---|
| 1 | 起動した PR 件数 / ready 化件数 / 失敗件数 |
| 2 | 失敗 PR の番号一覧（あれば） |

## 厳守事項

| No | 禁止 |
|---|---|
| 1 | マージしてはならない（マージは `pr-review-auto` の責務） |
| 2 | `processing` ラベルが既に付いた PR を別セッションが触ってはならない |
| 3 | Draft 以外の PR は触らない |
| 4 | 新規ブランチ・新規 PR を作成しない |
