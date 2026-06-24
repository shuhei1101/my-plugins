# プラグイン更新時のルール

プラグイン更新時必ず以下ファイルのバージョンを更新すること。

## マニフェスト管理方針（symlink 方式）

`.codex-plugin/*.json` を正ファイルとし、`.claude-plugin/*.json` はシンボリックリンクで参照します。

```
.codex-plugin/plugin.json  ← 正ファイル（こちらを更新する）
.claude-plugin/plugin.json → ../.codex-plugin/plugin.json（symlink）
```

### 更新手順

`.codex-plugin/` 側のみを更新すれば、`.claude-plugin/` 側にも自動反映されます。

- `plugins/<name>/.codex-plugin/plugin.json` — バージョン・説明を更新
- `.codex-plugin/marketplace.json` — バージョン・説明を更新

### symlink を初期化する場合

symlink が壊れているまたは初回セットアップの場合は `/util:codex-compat` スキルを実行してください。

```bash
# 手動で symlink を作成する場合
cd plugins/<name>/
rm -f .claude-plugin/plugin.json
ln -s "../.codex-plugin/plugin.json" .claude-plugin/plugin.json

# ルートの marketplace.json
cd <repo-root>
rm -f .claude-plugin/marketplace.json
ln -s "../.codex-plugin/marketplace.json" .claude-plugin/marketplace.json
```

> **前提**: WSL2 環境（`core.symlinks=true` が必要）。詳細は `plugins/util/skills/codex-compat/SKILL.md` を参照。
