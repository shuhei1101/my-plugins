---
name: gh-kit:issue-review
description: 未レビュー Issue を読み、AI が実装方針・質問を Issue コメントとして投稿する
---

# issue-review

ユーザーが書いた、または `/gh-kit:code-scan-auto` で起票された Issue に対し、
AI が実装方針案・確認したい質問・分割すべき粒度などを Issue コメントとして残す。

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| Issue 番号 | 任意 | 省略時は未レビュー Issue を全件巡回 |

未レビュー = ラベル `ai-reviewed` が付いていない open Issue。

## タスク

### ステップ 1: 対象 Issue を収集

| 状況 | コマンド |
|---|---|
| Issue 番号指定あり | `gh issue view {N} --json number,title,body,labels,comments` |
| 指定なし | `gh issue list --state open --search "-label:ai-reviewed" --json number,title,labels --limit 100`（昇順） |

0 件なら「未レビュー Issue なし」で停止。

### ステップ 2: 観点別レビューを委譲

[サブエージェントで並列実行・完了を待つ] 各 Issue について `issue-reviewer` サブエージェントを起動する。
（戻り値: `{issue_number, comment_body, suggested_labels[], status}`）

入力:
- Issue 番号 / タイトル / 本文 / 既存コメント全文
- リポジトリのコードベース参照可

### ステップ 3: Issue にコメント投稿 + ラベル更新

サブエージェントが返した `comment_body` を投稿する:

```bash
gh issue comment {N} --body-file <(cat <<'EOF'
{comment_body}
EOF
)
gh issue edit {N} --add-label ai-reviewed,{suggested_labels...}
```

### ステップ 4: 結果報告

| No | 報告項目 |
|---|---|
| 1 | レビューした Issue 件数と番号 |
| 2 | 各 Issue の状態（質問待ち / go 待ち / 分割提案あり） |
