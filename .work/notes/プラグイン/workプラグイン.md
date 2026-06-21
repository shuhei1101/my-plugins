# work プラグイン — ローカル Git ワークツリー作業基盤

## 概要

ローカル Git のワークツリー操作（ブランチ作成・親取り込み・マージ・ワークツリー削除）と、Claude Code タスク機能との連携リマインダーを提供するプラグイン。GitHub への依存はなし、gh-kit と独立に動く。保護フックは guard-kit、GitHub 操作は gh-kit、ローカル作業基盤は work、という三分割。

## バージョン

| バージョン | 主な変更 |
|---|---|
| 2.x | （旧 work、ノート機能などを段階的に削除） |
| 3.0 | `work` プラグインを再構築。`start` / `merge` スキル + worktree MCP は gh-kit から戻し、`task_reminder` フックと `TaskCreate/TaskList/TaskUpdate` 案内を追加。保護フックは guard-kit に分離 |

## スキル一覧

| No | スキル | 概要 |
|---|---|---|
| 1 | `/work:start` | ブランチ + ワークツリー作成、実装開始 |
| 2 | `/work:merge` | 親取り込み + コンフリクト処理 + マージ + ワークツリー削除 |

## MCP ツール（`work-tools` サーバー）

| ツール | 用途 |
|---|---|
| `worktree_create` | ブランチ `{type}/{title}` + worktree 作成 + Stop リマインダー用セッショントークン書き込み |
| `worktree_remove` | マージ済みワークツリー + ブランチ + セッショントークンを削除 |

## フック一覧

| No | フック | イベント | 役割 |
|---|---|---|---|
| 1 | `pre-merge-check` | PreToolUse(Bash) | マージ前の master 取り込み + dry-run コンフリクト検証 |
| 2 | `start_reminder` | UserPromptSubmit | `/work:start` 実行を促す |
| 3 | `task_reminder` | UserPromptSubmit | Claude Code タスク（TaskCreate/TaskList/TaskUpdate）の登録を促す |
| 4 | `session_start` | SessionStart | 作業フロー + タスクツール使い方ガイドを注入 |
| 5 | `merge_reminder` | Stop | `/work:merge` 提案リマインダー（worktree トークン有時のみ発火） |

## 環境変数

| 変数 | 用途 |
|---|---|
| `WORK_BRANCH_ENFORCEMENT` | `false` で start リマインダーを無効化 |
| `WORK_TASK_REMINDER` | `false` で task リマインダーを無効化 |
| `WORK_STOP_REMINDER` | `false` で merge リマインダー全体を無効化 |
| `WORK_MERGE_PROPOSAL` | `false` でマージ提案部分を省略 |

## トークンパス

| パス | 用途 |
|---|---|
| `~/.claude/tokens/work/worktree/<session>.json` | worktree-tool.py が管理。merge_reminder の発火条件 |

## 参考リンク

- `plugins/work/CLAUDE.md`: 同梱ドキュメント
- `plugins/work/skills/`: start / merge SKILL.md
- `plugins/work/mcp/server.py`: `work-tools` MCP サーバー
- `plugins/work/scripts/worktree/worktree-tool.py`: worktree 作成・削除 CLI
- `plugins/work/hooks/`: 5 フック（pre-merge-check / start_reminder / task_reminder / session_start / merge_reminder）
