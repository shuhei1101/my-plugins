# workコマンドのMCP化とStopフック制御

> ブランチ: `feat/work-mcp-tools`

## 概要

work プラグインのスキルが Bash で叩いているコマンド群（worktree 作成/削除・index-tool・issue-tool）を MCP ツール化する。
あわせて、毎ターン発火してうるさい Stop フック（work_complete_check）を、worktree 作業中のセッションのみ発火するようセッショントークンで制御する。

設計の確定事項:
- MCP サーバープロセスの環境に `CLAUDE_CODE_SESSION_ID` と `CLAUDE_PROJECT_DIR` が渡ることを実機確認済み
- `WorktreeCreate` / `WorktreeRemove` フックイベントは `--worktree` / EnterWorktree 専用で `git worktree add` では発火しない（公式ドキュメント確認済み）→ トークン管理はスクリプト内で行う
- worktree 作成場所は公式デフォルトの `{リポジトリ}/.claude/worktrees/` に変更（要 .gitignore 追加）
- トークン: `~/.claude/tokens/worktree/<session_id>.json`（inject_rules のフラットトークンと分離）

### 実施条件

即時実施可

## 作業内容

| No | 完了 | 作業内容 |
|---|---|---|
| 1 | - | `plugins/work/scripts/worktree-tool.py` 新規作成（create/remove + トークン管理） |
| 2 | - | `plugins/work/mcp/server.py` 新規作成（worktree_create/worktree_remove/index_add/index_set_completed/index_archive/issue_close） |
| 3 | - | `plugins/work/.mcp.json` でプラグイン MCP サーバーを登録 |
| 4 | - | `work_complete_check.py` をトークン存在時のみ発火するよう修正 |
| 5 | - | `worktree-create` スキルを撤廃 |
| 6 | - | `start` / `merge` スキルを MCP ツール使用に書き換え |
| 7 | - | `.gitignore` に `.claude/worktrees/` を追加 |
| 8 | - | work プラグインのバージョンバンプ |
| 9 | - | `.work/notes/` の関連ノートを更新する |

## 変更内容

| No | ファイル名 | 新規/編集 | 内容 |
|---|---|---|---|
| 1 | `plugins/work/scripts/worktree-tool.py` | 新規 | worktree create/remove + セッショントークン管理 CLI |
| 2 | `plugins/work/mcp/server.py` | 新規 | FastMCP サーバー（work-tools） |
| 3 | `plugins/work/.mcp.json` | 新規 | プラグイン MCP サーバー登録 |
| 4 | `plugins/work/hooks/work_complete_check.py` | 編集 | worktree トークン存在チェックを追加 |
| 5 | `plugins/work/skills/worktree-create/SKILL.md` | 削除 | MCP ツールに置き換え |
| 6 | `plugins/work/skills/start/SKILL.md` | 編集 | index_add / worktree_create ツール使用に変更 |
| 7 | `plugins/work/skills/merge/SKILL.md` | 編集 | issue_close / index_set_completed / index_archive / worktree_remove ツール使用に変更 |
| 8 | `.gitignore` | 編集 | `.claude/worktrees/` を追加 |

## テスト

| No | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | worktree-tool.py create でワークツリーとトークンが作成される | (未実施) | - |
| 2 | worktree-tool.py remove でワークツリーとトークンが削除される | (未実施) | - |
| 3 | MCP サーバーの全ツールでスキーマが正しく生成される | (未実施) | - |
| 4 | work_complete_check がトークンなしで exit 0、ありでブロックする | (未実施) | - |
