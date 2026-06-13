# MCP サーバーの pyyaml 依存追加

## 概要

work プラグインの MCP サーバーが `uv run --with mcp` で起動するとき、`index-tool.py` 等のスクリプトが `import yaml` を使うが pyyaml が入っておらずエラーになっていた。
`.mcp.json` に `--with pyyaml` を追加して解消する。

## 作業内容

| 作業 | 完了 |
| ---- | ---- |
| `plugins/work/.mcp.json` に `--with pyyaml` を追加 | 済 |

## 参考ドキュメント
