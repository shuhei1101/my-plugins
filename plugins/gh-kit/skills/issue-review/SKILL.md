---
name: gh-kit:issue-review
description: needs-ai-review ラベルの Issue を読み、AI が実装方針・質問を Issue コメントとして投稿する
---

# issue-review

`needs-ai-review` がついた Issue を AI が読み、実装方針・確認したい質問・分割すべき粒度などを
Issue コメントとして残す。完了後 `needs-ai-review` を外し、必要なら `needs-user-review` を付ける。

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| Issue 番号 | 任意 | 省略時は `needs-ai-review` 付きを全件巡回 |

## ラベル定義の読み込み

```bash
. "${CLAUDE_PLUGIN_ROOT}/scripts/labels.sh"
```

## タスク

### ステップ 1: 対象 Issue を収集

| 状況 | コマンド |
|---|---|
| Issue 番号指定あり | `gh issue view {N} --json number,title,body,labels,comments` |
| 指定なし | `gh issue list --state open --label "$LABEL_NEEDS_AI_REVIEW" --json number,title,labels --limit 100`（昇順） |

`processing` がついた Issue は除外（他セッションが触っている）。

0 件なら「未レビュー Issue なし」で停止。

### ステップ 2: 排他制御

各対象 Issue に `processing` を付ける:

```bash
gh issue edit {N} --add-label "$LABEL_PROCESSING"
```

### ステップ 3: 観点別レビューを委譲

[サブエージェントで並列実行・完了を待つ] 各 Issue について `issue-reviewer` サブエージェントを起動する。
（戻り値: `{issue_number, comment_body, needs_user_review, status}`）

入力:
- Issue 番号 / タイトル / 本文 / 既存コメント全文
- リポジトリのコードベース参照可

### ステップ 4: Issue にコメント投稿 + ラベル更新

サブエージェントが返した内容を反映:

```bash
gh issue comment {N} --body-file <(cat <<'EOF'
{comment_body}
EOF
)

# 排他解除 + AI レビュー完了マーク
ARGS=(--remove-label "$LABEL_PROCESSING" --remove-label "$LABEL_NEEDS_AI_REVIEW")
if [ "{needs_user_review}" = "true" ]; then
  # 既に付いていれば何もしない、無ければ付ける
  ARGS+=(--add-label "$LABEL_NEEDS_USER_REVIEW")
fi
gh issue edit {N} "${ARGS[@]}"
```

### ステップ 5: 結果報告

| No | 報告項目 |
|---|---|
| 1 | レビューした Issue 件数と番号 |
| 2 | `needs-user-review` を付けた / 付けなかった内訳 |
