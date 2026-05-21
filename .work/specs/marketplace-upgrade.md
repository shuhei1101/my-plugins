# marketplace upgrade コマンド仕様

## 目的

`marketplace.py upgrade` でインストール済みプラグインを最新版に更新する。
ユーザースコープ・プロジェクトスコープの両方を正しく扱う。

## 動作仕様

### スコープ検出

`installed_plugins.json` を2箇所から読み込む:
- `~/.claude/plugins/installed_plugins.json` → デフォルト scope: "user"
- `./.claude/plugins/installed_plugins.json` → デフォルト scope: "local"

両方に同じプラグインが存在する場合はプロジェクト側（local）を優先する。

### 更新方式

`plugin update` コマンドはユーザースコープのみ対応しているため、
全スコープで統一して以下の手順で更新する:

1. `plugin uninstall {name}@{marketplace}`
2. `plugin install {name}@{marketplace} --scope {scope}`

### 対象プラグイン

- `KEY_PREFIX`（`mentaiko-claude-plugins`）マーケットプレイスからインストール済みのプラグインのみ
- 未インストールプラグインは新規インストールしない
- マーケットプレイスから削除されたプラグインはアンインストールして除外
