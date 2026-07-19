# MCP サーバー作成ルール

## SDK とトランスポート

- 公式 MCP Python SDK（pip の `mcp` パッケージ）の `FastMCP` を使う
  - `from mcp.server.fastmcp import FastMCP`
  - サードパーティの「FastMCP 2.0」（pip の `fastmcp`）とは別物。混同しない
- ローカルツールは stdio トランスポート（`mcp.run()` のデフォルト）
  - Claude Code が子プロセスとして起動し標準入出力で通信する。ポートは使わない

## 構成

- ビジネスロジックは `scripts/` や `tools/` の単体実行可能な CLI に置き、MCP サーバーはそれを subprocess で呼ぶシン・ラッパーにする
  - CLI 単体でもデバッグでき、ロジックが MCP に縛られない
- サーバープロセスの環境には `CLAUDE_PROJECT_DIR`（プロジェクトルート）と `CLAUDE_CODE_SESSION_ID` が渡される
  - 作業ディレクトリに依存せず `CLAUDE_PROJECT_DIR` を基準にパス解決する

## ツール定義のスキーマ

| 要素 | 書き方 |
| --- | --- |
| description | 関数の docstring（1 行） |
| title | `@mcp.tool(title="日本語タイトル")` |
| 引数の説明 | `Annotated[型, Field(description=...)]` |
| 引数の選択肢制限 | `Literal[...]` → enum としてスキーマに反映 |
| 出力スキーマ | 戻り値を Pydantic モデルにする → outputSchema 自動生成。各フィールドに `Field(description=...)` |
| ツールの性質 | `ToolAnnotations(readOnlyHint=..., destructiveHint=...)` |

- 戻り値は `{success: bool, output: str}` 形式の共通モデルを基本とする
- docstring に引数説明を書かない（スキーマに反映されないため。必ず `Field` で書く）

## 登録

- プロジェクト用: ルートの `.mcp.json`（バージョン管理でチーム共有）
- プラグイン用: プラグインルートの `.mcp.json` + `${CLAUDE_PLUGIN_ROOT}` でパス解決
- 起動コマンドは `uv run --with mcp python {サーバーパス}`（依存を環境に入れずに起動できる）

## 動作確認

- `mcp.list_tools()` を非同期実行し、全ツールの title・引数説明・enum・outputSchema・annotations が生成されることを確認する
- 反映にはセッション再起動が必要（`/reload-plugins` ではプラグイン MCP サーバーは再接続されない場合がある。`/mcp` で接続状態を確認）
