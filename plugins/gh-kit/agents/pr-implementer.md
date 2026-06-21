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
| 採用方針 | Issue コメントの `issue-reviewer` 結果から抽出 |
| 分割スコープ | この PR で扱うスコープ |

## ステップ 1: 判定基準テンプレートを取得

```bash
cat "${CLAUDE_PLUGIN_ROOT}/templates/ユーザーレビュー要否判定.md"
```

ステップ 4 で参照する。

## ステップ 2: ワークツリー復帰 + remote 同期

```bash
WT=".claude/worktrees/$(echo {branch} | tr '/' '-')"
if [ ! -d "$WT" ]; then
  echo "worktree missing, please run /work:start with branch={branch}" >&2
  exit 1
fi
git -C "$WT" fetch origin
git -C "$WT" reset --hard origin/{branch}
```

## ステップ 3: 実装

採用方針と分割スコープに従って実装する。コミットは細かく刻んでよい。

| No | 動作 |
|---|---|
| 1 | 採用方針の通りにコード変更 |
| 2 | 影響範囲のテストを追加/更新 |
| 3 | プロジェクトのテストを実行 |

## ステップ 4: push

```bash
git -C "$WT" push origin {branch}
```

## ステップ 5: `needs-user-review` 要否を再判定

ステップ 1 で取得した `ユーザーレビュー要否判定.md` に照らし、実装結果（実コード変更内容）から
`needs_user_review: true|false` を決める。
Issue 起票時の判断と変わる可能性あり（例: refactor 想定だったが仕様に踏み込んだ場合は true）。

## ステップ 6: PR を Ready 化

```bash
gh pr ready {PR_NUMBER}
gh pr comment {PR_NUMBER} --body "実装完了。レビュー待ち。{変更サマリ}"
```

ラベル付与（`needs-ai-review` / `needs-user-review`）は呼び出し側（`/gh-kit:pr-implement-auto`）の責務。

## ステップ 7: 戻り値

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
| 3 | コンフリクトが出たら親に報告して停止（`-X ours/theirs` 禁止） |
| 4 | `git push --force` は使わない |
