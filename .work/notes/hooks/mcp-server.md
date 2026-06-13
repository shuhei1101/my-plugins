# my-plugins MCP サーバー — ツール群の MCP 公開

## 概要

`tools/` 配下の開発ツールを MCP サーバーとして Claude Code に公開する。`.mcp.json` で登録し、`uv run --with mcp` で起動する。

## 登録設定

`.mcp.json`（プロジェクトルート）に記述:
- サーバー名: `my-plugins-tools`
- 起動コマンド: `uv run --with mcp python tools/mcp_server.py`

## 公開ツール一覧

| ツール名 | 委譲先 | 概要 | annotations |
|---|---|---|---|
| `push` | `scripts/post_merge_upgrade.py` | push + marketplace upgrade + reload-plugins | 書き込み・非破壊 |
| `bump_version` | `tools/bump-version.py` | プラグインバージョンバンプ | 〃 |
| `marketplace` | `tools/marketplace.py` | マーケットプレイス管理 | 書き込み・破壊的（remove で uninstall） |
| `reload_plugins` | `tools/reload_plugins.py` | marketplace upgrade 後に tmux セッションへ /reload-plugins 送信 | 書き込み・非破壊 |
| `sync_plugin_cache` | `tools/sync_plugin_cache.py` | ローカル編集をキャッシュに同期 | 書き込み・破壊的（キャッシュ削除→コピー） |
| `pre_merge_check` | `tools/pre_merge_check.py` | マージ前バージョンチェック | 読み取りのみ |

## スキーマ定義の作法（MCP Python SDK 公式準拠）

- ツールの description: docstring（`@mcp.tool(description=...)` でも上書き可）
- ツールの title: `@mcp.tool(title=...)`
- 引数の説明: `Annotated[type, Field(description=...)]` → inputSchema に反映
- 引数の選択肢制限: `Literal[...]` → inputSchema の enum に反映
- 出力スキーマ: 戻り値の Pydantic モデル（`CommandResult`）→ outputSchema が自動生成、各フィールドの `Field(description=...)` が説明になる
- ツールの性質: `ToolAnnotations(readOnlyHint=..., destructiveHint=...)`

全ツールは `CommandResult { success: bool, output: str }` を返す。

## 参考リンク

- `.mcp.json`: MCP サーバー登録設定
- `tools/mcp_server.py`: FastMCP サーバー本体
