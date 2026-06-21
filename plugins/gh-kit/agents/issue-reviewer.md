---
name: issue-reviewer
description: 1 Issue を AI レビューし、本文拡張コメント（任意）+ レビュー結果コメントを gh CLI で投稿するエージェント
model: sonnet
---

`gh-kit:issue-review` スキルに処理を委譲する薄ラッパー。

## 入力

| 引数 | 内容 |
|---|---|
| Issue 番号 | 例: 42 |

## タスク

受け取った引数をそのまま `/gh-kit:issue-review` スキルに渡して実行する。
スキルの戻り値をそのまま呼び出し元に返す。

## 戻り値

スキルの戻り値をそのまま返す:

```json
{
  "issue_number": 42,
  "needs_user_review": true,
  "status": "ok"
}
```
