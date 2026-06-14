---
name: branch-blank-worker
description: 忘れ去られたブランチを最後まで実行する
---

## 作業内容
1. 入力されたブランチ名のワークツリーに入る
   1. もしワークツリーがない場合、`worktree_create` MCP ツール（work-tools サーバー）を実行し、ワークツリーを作る
2. `/work:start`スキルを実行し、作業を進める
   1. 必ずタスクドキュメントまではコミットすること(`.work/tasks/**/*.task.md`)
3. 作業が完了したらメインエージェントに結果を報告する
