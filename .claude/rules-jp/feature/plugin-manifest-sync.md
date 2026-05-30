---
paths:
  - "plugins/*/.claude-plugin/plugin.json"
  - ".claude-plugin/marketplace.json"
---
> ⚠️ **Japanese mirror** — Claude には読み込まれません。このファイルを更新するときは、必ず英語版 `.claude/rules/feature/plugin-manifest-sync.md` も同時に更新してください。

# Plugin Manifest Sync Rules（プラグインマニフェスト同期ルール）

## Overview

`plugins/{name}/.claude-plugin/plugin.json` を編集したら、**必ず同じコミットで `.claude-plugin/marketplace.json` も更新する**。

`plugin.json` はプラグインの自己宣言であり、`marketplace.json` はカタログのソース。片方だけ更新するとプラグインが古い名前・パスでリストされ続け、インストールが壊れる。

## Related Files

| ファイルパス | 役割 |
|---|---|
| `plugins/{name}/.claude-plugin/plugin.json` | プラグイン自体のマニフェスト（name / description / version） |
| `.claude-plugin/marketplace.json` | 全プラグインのカタログ（name / source / description / version） |
| `.claude/rules/feature/plugin-manifest-sync.md` | このルール（英語版） |

## When Editing

`plugin.json` または `marketplace.json` を編集するときは、必ずもう一方も確認する:

- [ ] `plugin.json` の `name` を変更した → `marketplace.json` の対応エントリの `name` と `source` を更新済みか
- [ ] `plugin.json` の `description` を変更した → `marketplace.json` の対応エントリの `description` を更新済みか
- [ ] `plugin.json` の `version` を変更した → `marketplace.json` の対応エントリの `version` を更新済みか
- [ ] プラグインフォルダを `git mv` でリネームした → `marketplace.json` の `source` パスが新しいフォルダ名を指しているか
- [ ] このドメインにファイルを追加した場合、このルールの `paths:` と Related Files も更新したか

## Rule Maintenance

このドメインのファイル操作を行う際:
- **新しいファイルを追加した** → `paths:` と Related Files リストに追加する
- **ファイルを削除・リネームした** → `paths:` と Related Files を修正する
- **ドメインの責務が変わった** → Overview セクションを更新する
