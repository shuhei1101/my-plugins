# work-tools MCP サーバー — work プラグインのコマンド MCP 公開と Stop フック制御

## 概要

work プラグインのスキルが使うコマンド群を MCP ツールとして公開する。あわせて Stop フック（work_complete_check）は worktree 作業中のセッションのみ発火する。

## 登録設定

`plugins/work/.mcp.json`（プラグイン MCP サーバー）:
- サーバー名: `work-tools`
- 起動コマンド: `uv run --with mcp python ${CLAUDE_PLUGIN_ROOT}/mcp/server.py`
- サーバー環境には `CLAUDE_CODE_SESSION_ID` と `CLAUDE_PROJECT_DIR` が渡される（実機確認済み）

## 公開ツール一覧

| ツール名 | 委譲先 | 概要 |
|---|---|---|
| `worktree_create` | `scripts/worktree-tool.py` | ブランチ + ワークツリー作成 + トークン書き込み |
| `worktree_remove` | 〃 | ワークツリー + ブランチ削除 + トークン削除 |
| `index_add` | `scripts/index-tool.py` | index.yaml にエントリ追加 |
| `index_set_completed` | 〃 | index.yaml で完了マーク |
| `index_archive` | 〃 | 完了エントリを index.archive.yaml へ移動 |
| `issue_close` | `scripts/issue-tool.py` | イシューをクローズ |

## ワークツリーの配置

- 作成場所: `{リポジトリ}/.claude/worktrees/{type}-{title}`（Claude Code 公式デフォルトと同じ場所）
- `.gitignore` に `.claude/worktrees/` を登録済み
- 旧形式（`../{repo}-wt-*`）のワークツリーも `worktree_remove` は `git worktree list` から探して削除できる

## Stop フックのセッショントークン制御

- トークン: `~/.claude/tokens/worktree/<session_id>.json`（inject_rules のフラットトークンとはサブフォルダで分離）
- 中身: `{"worktrees": [{"branch", "path"}]}` — 1 セッション複数ワークツリー対応
- ライフサイクル: `worktree-tool.py create` で作成・`remove` で削除（worktrees が空になるとトークンごと削除）
- `work_complete_check.py` は stdin の `session_id` でトークンを引き、なければ exit 0（リマインダーを出さない）
- 放置トークンは create 時に 7 日 TTL で掃除される
- `WorktreeCreate` / `WorktreeRemove` フックイベントは `--worktree` / EnterWorktree 専用で `git worktree add` では発火しないため、フックイベントではなくスクリプト内でトークンを管理する

## 参考リンク

- `plugins/work/.mcp.json`: MCP サーバー登録設定
- `plugins/work/mcp/server.py`: FastMCP サーバー本体
- `plugins/work/scripts/worktree-tool.py`: ワークツリー + トークン管理 CLI
- `plugins/work/hooks/work_complete_check.py`: トークンゲート付き Stop フック
