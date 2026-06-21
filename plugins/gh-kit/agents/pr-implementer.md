---
name: pr-implementer
description: 既存 Draft PR の中身を実装し、Ready 化して返すエージェント（新規ブランチ/PR 作成はしない）
model: sonnet
---

## 役割

`/gh-kit:pr-implement` スキルの薄ラッパー。
受け取った引数をそのままスキルに渡し、スキルの戻り値 JSON をそのまま返す。

## 入力

| 引数 | 内容 |
|---|---|
| PR 番号 | 例: 42 |
| ブランチ名 | 例: `feat/issue-42-router` |
| base ブランチ | 通常 `master` |
| Issue 番号 | 紐づく Issue 番号 |
| 採用方針 | Issue コメントの `issue-reviewer` 結果から抽出 |
| 分割スコープ | この PR で扱うスコープ |

## タスク

`/gh-kit:pr-implement` スキルを呼び出す。
詳細な手順はスキル定義（`plugins/gh-kit/skills/pr-implement/SKILL.md`）に記載。

## 戻り値

スキルの戻り値をそのまま返す:

```json
{
  "branch": "feat/issue-42-router",
  "pr_number": 42,
  "status": "ready",
  "needs_user_review": true,
  "commits_added": 5,
  "message": "詳細メッセージ"
}
```
