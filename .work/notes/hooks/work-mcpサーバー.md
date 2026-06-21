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

## SessionStart での概要注入

- `plugins/work/hooks/session-start/session_start.py` がセッション開始時に `session_start.md`（作業フロー・MCP ツール一覧・ガード・cwd 注意）を additionalContext として注入する
- 新しいセッションが work プラグインの使い方を最初から把握できる

## VS Code ワークスペース連携

- 環境変数 `VSCODE_WORKSPACE_FILE` に `.code-workspace` のパスを設定すると有効化（未設定ならスキップ）
  - 設定場所: settings.json の `env` フィールド（例: `"env": {"VSCODE_WORKSPACE_FILE": "C:/Users/shuhe/repo/my.code-workspace"}` 相当の WSL パス）
- worktree 作成時に `folders` 末尾へ `{name: ブランチ名, path: ワークツリーパス}` を追加、削除時に取り除く
- WSL の `/mnt/<drive>/` パスは Windows 形式（`C:/...`）に変換して書き込む
- コメント付き JSONC など解析できないワークスペースファイルは壊さずスキップする

## トークンのディレクトリ構造

`~/.claude/tokens/{プラグイン}/{用途}/<session_id>.json` に統一:

| パス | 書き手 | 用途 |
|---|---|---|
| `tokens/dev-kit/rules/` | dev-kit の inject_rules.py | ルール注入済みリスト |
| `tokens/work/rules/` | work の inject_rules.py | 〃 |
| `tokens/work/worktree/` | work の worktree-tool.py | worktree 作業中フラグ |

## Stop フックのセッショントークン制御

- トークン: `~/.claude/tokens/work/worktree/<session_id>.json`
- 中身: `{"worktrees": [{"branch", "path"}]}` — 1 セッション複数ワークツリー対応
- ライフサイクル: `worktree-tool.py create` で作成・`remove` で削除（worktrees が空になるとトークンごと削除）
- `work_complete_check.py` は stdin の `session_id` でトークンを引き、なければ exit 0（リマインダーを出さない）
- 放置トークンは create 時に 7 日 TTL で掃除される
- `WorktreeCreate` / `WorktreeRemove` フックイベントは `--worktree` / EnterWorktree 専用で `git worktree add` では発火しないため、フックイベントではなくスクリプト内でトークンを管理する

## 参考リンク

- `plugins/work/.mcp.json`: MCP サーバー登録設定
- `plugins/work/mcp/server.py`: FastMCP サーバー本体
- `plugins/work/scripts/worktree-tool.py`: ワークツリー + トークン管理 CLI
- `plugins/work/hooks/stop/work_complete_check.py`: トークンゲート付き Stop フック
- `plugins/dev-kit/hooks/rules/claude/mcp.md`: MCP サーバー作成ルール（MCP 関連ファイル編集時に自動注入）
