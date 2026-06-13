# cmd_upgradeのuninstallに--scope指定を追加

> ブランチ: `fix/cmd-upgrade-scope`

## 概要

`cmd_upgrade()`のuninstallコマンドに`--scope`を指定していないため、localスコープのプラグインのアンインストールが常に失敗する（`allow_fail=True`で無視）。
その結果、次のinstallで「already installed」と判断されてキャッシュが更新されない。
uninstallコマンドに`--scope {scope}`を追加して修正する。

### 実施条件

即時実施可

## 作業内容

| No | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | `tools/marketplace.py`のcmd_upgrade()でuninstallコマンドに`--scope`を追加 |
| 2 | 済 | workプラグインのバージョンバンプ（1.5 → 1.6） |

## 変更内容

| No | ファイル名 | 新規/編集 | 内容 |
|---|---|---|---|
| 1 | `tools/marketplace.py` | 編集 | cmd_upgrade()のuninstallに`--scope scope`を追加 |
| 2 | `plugins/work/.claude-plugin/plugin.json` | 編集 | バージョン1.5→1.6 |

## 参考ドキュメント

- [MCP サーバー](.work/notes/hooks/mcp-server.md)
