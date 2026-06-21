# work プラグイン

ローカル Git ワークツリー作業の基盤プラグイン（GitHub 依存なし）。

## スキル

| No | スキル | 用途 |
|---|---|---|
| 1 | `/work:start` | ブランチ + ワークツリーを作成して作業開始（`worktree_create` MCP を呼ぶ） |
| 2 | `/work:merge` | 親取り込み + コンフリクト処理 + マージ + ワークツリー削除（`worktree_remove` MCP を呼ぶ） |

## MCP ツール（`work-tools` サーバー）

| ツール | 用途 |
|---|---|
| `worktree_create` | `{type}/{title}` ブランチ + `.claude/worktrees/{type}-{title}` 作成、Stop リマインダー用トークンを書く |
| `worktree_remove` | マージ済みワークツリー + ブランチ + トークンの削除 |

## フック

| No | フック | イベント | 役割 |
|---|---|---|---|
| 1 | `pre-merge-check` | PreToolUse(Bash) | マージ前の master 取り込み + dry-run コンフリクト検証 |
| 2 | `start_reminder` | UserPromptSubmit | `/work:start` 実行を促す |
| 3 | `task_reminder` | UserPromptSubmit | Claude Code タスク（TaskCreate/TaskList/TaskUpdate）の登録を促す |
| 4 | `session_start` | SessionStart | 作業フロー + タスクツール使い方ガイド + 禁止事項を注入 |
| 5 | `merge_reminder` | Stop | `/work:merge` 提案リマインダー |

## 環境変数

| 変数 | 用途 |
|---|---|
| `WORK_BRANCH_ENFORCEMENT` | `false` で `start_reminder` を無効化 |
| `WORK_TASK_REMINDER` | `false` で `task_reminder` を無効化 |
| `WORK_STOP_REMINDER` | `false` で `merge_reminder` 全体を無効化 |
| `WORK_MERGE_PROPOSAL` | `false` でマージ提案部分を省略 |

## ルール

| いつ             | 内容                                                                          |
| ---------------- | ----------------------------------------------------------------------------- |
| 新規フック追加時 | `plugins/work/hooks/session-start/session_start.md` も更新すること |
