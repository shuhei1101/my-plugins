---
name: work:issue-resolve
description: 指定された 1 件のイシューを消化する（in_progress 化 → ブランチ作成 → 実装 → 必要なら merge）
---

# issue-resolve — レビュー済みイシューを消化する

## タスク
- 指定されたイシューを読む（イシューが指定されなければユーザに聞く）
- メインリポジトリの `_index.yaml` でイシューを in-progress にする
  - `issue_set_status` MCP ツール（work-tools サーバー）を実行:
    - issues_dir: `.work/issues` / issue_id: `ISSUE-{NNN}` / status: `in_progress`
- ブランチ名を決める（`type/kebab-title`）
- `worktree_create` MCP ツール（work-tools サーバー）を実行し、ワークツリーを作る
- `/work:start`スキルを実行し、作業を進める
  - 関連イシューがユーザのマージ確認が必要でない場合、`/merge`スキルを実行する
