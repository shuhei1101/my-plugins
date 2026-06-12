# my-plugins MCP サーバー — ツール群の MCP 公開

## 概要

`tools/` 配下の開発ツールを MCP サーバーとして Claude Code に公開する。`.mcp.json` で登録し、`uv run --with mcp` で起動する。

## 登録設定

`.mcp.json`（プロジェクトルート）に記述:
- サーバー名: `my-plugins-tools`
- 起動コマンド: `uv run --with mcp python tools/mcp_server.py`

## 公開ツール一覧

| ツール名 | 委譲先 | 概要 |
|---|---|---|
| `push` | `tools/post_merge_upgrade.py` | push + marketplace upgrade + reload-plugins |
| `bump_version` | `tools/bump-version.py` | プラグインバージョンバンプ |
| `marketplace` | `tools/marketplace.py` | マーケットプレイス管理 |
| `reload_plugins` | `tools/reload_plugins.py` | tmux セッションに /reload-plugins 送信 |
| `sync_plugin_cache` | `tools/sync_plugin_cache.py` | ローカル編集をキャッシュに同期 |
| `pre_merge_check` | `tools/pre_merge_check.py` | マージ前バージョンチェック |

## 参考リンク

- `.mcp.json`: MCP サーバー登録設定
- `tools/mcp_server.py`: FastMCP サーバー本体
