# marketplace-upgradeコマンド — インストール済みプラグインの一括更新

## 概要

`marketplace.py upgrade` は、`mentaiko-claude-plugins` マーケットプレイス由来のインストール済みプラグインを最新版に更新する。ユーザースコープ・プロジェクトスコープの両方を正しく扱う。

## スコープ検出

`installed_plugins.json` を 2 箇所から読み込む。

| パス | デフォルト scope |
|---|---|
| `~/.claude/plugins/installed_plugins.json` | `user` |
| `./.claude/plugins/installed_plugins.json` | `local` |

- 両方に同じプラグインが存在する場合は local（プロジェクト側）を優先する。

## 更新方式

`plugin update` コマンドはユーザースコープのみ対応のため、全スコープで以下の手順に統一する。

1. `plugin uninstall {name}@{marketplace}`
2. `plugin install {name}@{marketplace} --scope {scope}`

## 対象プラグイン

- `KEY_PREFIX`（`mentaiko-claude-plugins`）マーケットプレイスからインストール済みのプラグインのみ。
- 未インストールプラグインは新規インストールしない。
- マーケットプレイスから削除されたプラグインはアンインストールして除外する。

## 参考ドキュメント

- `marketplace.py`: コマンド実装本体

## 変更履歴

| # | 日付 | 変更内容 | 関連タスク |
|---|---|---|---|
| 1 | 260531 | 新規作成（specsから統合） | 260531_notes-spec-and-ref-inject |
