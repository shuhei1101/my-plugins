# プラグイン更新時のルール

プラグイン更新時必ず以下ファイルのバージョンを更新すること。
Claude Code 向けと Codex 向けの両方を更新する。

## Claude Code 向け（.claude-plugin/）

- `plugins/<name>/.claude-plugin/plugin.json` — バージョン・説明を更新
- `.claude-plugin/marketplace.json` — バージョン・説明を更新

## Codex 向け（.codex-plugin/）

- `plugins/<name>/.codex-plugin/plugin.json` — バージョン・説明を更新
- `.codex-plugin/marketplace.json` — バージョン・説明を更新

> **推奨**: `.claude-plugin/*.json` を更新した後、同期スクリプトを実行すると Codex 側に自動反映できます。

```bash
# リポジトリルートで実行
bash plugins/gh-kit/scripts/sync-codex-manifests.sh
```

このスクリプトは冪等です。差分がある場合のみ上書きするため、何度実行しても安全です。
