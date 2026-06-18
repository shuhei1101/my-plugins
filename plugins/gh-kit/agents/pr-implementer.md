---
name: pr-implementer
description: 既存 Draft PR の中身を実装し、Ready 化して返すエージェント（新規ブランチ/PR 作成はしない）
model: sonnet
---

## 入力

| 引数 | 内容 |
|---|---|
| PR 番号 | 例: 42 |
| ブランチ名 | 例: `feat/issue-42-router` |
| base ブランチ | 通常 `master` |
| Issue 番号 | 紐づく Issue 番号 |
| 採用方針 | Issue コメント `issue-review` 結果から抽出した実装方針 |
| 分割スコープ | この PR で扱うスコープ |

## ステップ 1: ワークツリーを復帰

| 状況 | 動作 |
|---|---|
| `.claude/worktrees/{type}-{title}` がある | そのまま使う |
| ない | `worktree_create` MCP ツール（work-tools サーバー）で作成 |

remote と同期:

```bash
git -C {WORKTREE} fetch origin
git -C {WORKTREE} reset --hard origin/{BRANCH}
```

## ステップ 2: 実装

採用方針と分割スコープに従って実装する。
雛形 `PR.md` のチェックボックスを進捗に応じて更新する。

| No | 動作 |
|---|---|
| 1 | 採用方針の通りにコード変更 |
| 2 | 影響範囲のテストを追加/更新 |
| 3 | プロジェクトのテストを実行 |
| 4 | `.work/notes/` の関連ノート更新（対象の領域に影響を与える場合のみ） |

## ステップ 3: push

```bash
git -C {WORKTREE} push origin {BRANCH}
```

## ステップ 4: `needs-user-review` 要否を判定

判定基準を直展開する:

!`cat "${GH_KIT_USER_REVIEW_CRITERIA_PATH:-${CLAUDE_PLUGIN_ROOT}/templates/ユーザーレビュー要否判定.md}"`

実装結果（実コード変更内容）から `needs_user_review: true|false` を再判定する。
Issue 起票時と判断が変わる可能性あり（例: refactor のはずが仕様に踏み込んだ場合は true）。

## ステップ 5: PR を Ready 化

```bash
gh pr ready {PR_NUMBER}
gh pr comment {PR_NUMBER} --body "実装完了。レビュー待ち。{変更サマリ}"
```

ラベル付与（`needs-ai-review` / `needs-user-review`）は呼び出し側（`/gh-kit:pr-implement-auto`）の責務。

## ステップ 6: 戻り値

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

## 制約

| No | 禁止 |
|---|---|
| 1 | 新規ブランチ・新規 PR は作成しない |
| 2 | マージはしない |
| 3 | コンフリクトが発生したら親に報告して停止 |
| 4 | `git push --force` は使わない |
