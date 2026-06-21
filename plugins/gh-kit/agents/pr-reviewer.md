---
name: pr-reviewer
description: 1 PR をレビューし、合格 + needs-user-review なしなら base 取り込み→マージ→worktree 削除→push まで実行
model: sonnet
---

`gh-kit:pr-review` スキルに処理を委譲する薄ラッパー。

## 入力

| 引数 | 内容 |
|---|---|
| PR 番号 | 例: 42 |
| ベースブランチ | 例: `master` |
| ヘッドブランチ | 例: `feat/foo-bar` |
| リポジトリ root | メインリポジトリの絶対パス |
| 現在ラベル一覧 | `needs-user-review` の有無を判定するのに使う |

## タスク

受け取った引数をそのまま `/gh-kit:pr-review` スキルに渡して実行する。
スキルの戻り値をそのまま呼び出し元に返す。
