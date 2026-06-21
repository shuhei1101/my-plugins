---
name: gh-kit:pr-implement
description: "wip Draft PR を 1 件実装する: worktree 復帰 → fetch/reset → 実装 → コミット → push → gh pr ready。pr-implementer エージェントから呼ばれる。"
---

# pr-implement

既存 Draft PR の中身を実装し、Ready for review にする。
新規ブランチ・新規 PR の作成は行わない。

## 入力

| 引数 | 必須 | 内容 |
|---|---|---|
| PR 番号 | 必須 | 例: 42 |
| branch | 必須 | 例: `feat/issue-42-router` |
| base ブランチ | 必須 | 通常 `master` |
| Issue 番号 | 必須 | 紐づく Issue 番号 |
| 採用方針 | 必須 | Issue コメントの `issue-reviewer` 結果から抽出 |
| 分割スコープ | 任意 | この PR で扱うスコープ（1 Issue 複数 PR 時） |

## ステップ 1: needs-user-review 判定基準を読み込む

```bash
cat "${CLAUDE_PLUGIN_ROOT}/templates/ユーザーレビュー要否判定.md"
```

ステップ 5 で参照する。

## ステップ 2: ワークツリー復帰 + remote 同期

```bash
WT=".claude/worktrees/$(echo {branch} | tr '/' '-')"
if [ ! -d "$WT" ]; then
  echo "worktree missing, please call gh-kit-tools worktree_create MCP for branch={branch}" >&2
  exit 1
fi
git -C "$WT" fetch origin
git -C "$WT" reset --hard origin/{branch}
```

## ステップ 3: 実装

採用方針と分割スコープに従ってコード変更する。コミットは細かく刻んでよい。

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

ステップ 1 で読み込んだ基準に照らし、実装結果（実コード変更内容）から
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
