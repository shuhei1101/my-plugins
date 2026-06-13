# reload-plugins時にmarketplace upgradeも実行する

> ブランチ: `feat/reload-with-upgrade`

## 概要

`reload_plugins.py`（および`mcp_server.py`の`reload_plugins`ツール）がtmuxに`/reload-plugins`を送信するだけで、`marketplace.py upgrade`を実行しないため、キャッシュが古いままになる問題があった。
`reload_plugins.py`のmain処理でupgradeを先に実行してからtmux送信するよう変更する。

### 実施条件

即時実施可

## 作業内容

| No | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | `tools/reload_plugins.py` でtmux送信前に`marketplace.py upgrade`を実行する |
| 2 | 済 | `mcp_server.py` の`reload_plugins`ツールのdescriptionを更新する |
| 3 | 済 | workプラグインのバージョンバンプ（1.4 → 1.5） |

## 変更内容

| No | ファイル名 | 新規/編集 | 内容 |
|---|---|---|---|
| 1 | `tools/reload_plugins.py` | 編集 | tmux送信前にmarketplace.py upgradeを実行 |
| 2 | `tools/mcp_server.py` | 編集 | reload_pluginsツールのdescription更新 |
| 3 | `plugins/work/.claude-plugin/plugin.json` | 編集 | バージョン1.4→1.5 |

## テスト

| No | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | reload_plugins実行時にupgradeが先に走る |  |  |
| 2 | upgrade後にtmuxへ/reload-pluginsが送信される |  |  |

## 参考ドキュメント

- [MCP サーバー](.work/notes/hooks/mcp-server.md)
