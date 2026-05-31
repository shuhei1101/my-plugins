# ISSUE-002: work プラグインの description が marketplace.json と plugin.json で不一致

**作成日**: 2026-05-31

## 問題

`work` プラグインの `description` フィールドが以下の2ファイル間で内容が異なる。

- `.claude-plugin/marketplace.json` (marketplace エントリ)
- `plugins/work/.claude-plugin/plugin.json` (プラグイン個別マニフェスト)

具体的には、marketplace.json の description には `v2.54.0` の変更履歴エントリ（`index.yaml branch index is keyed by \`branch\` (drop id/last_id/tags); legacy backlog migrated to index.archive.yaml`）が含まれているが、plugin.json の description ではこのエントリが欠落しており、`v2.53.1` から `v2.55.0` に直接飛んでいる。

`references/plugin/バージョン同期.md` では「この3ファイルは常に同じバージョン番号を持ち、同期を保たなければならない」と定められており、description の内容ドリフトはその原則に反する。

## 修正案

`plugins/work/.claude-plugin/plugin.json` の `description` フィールドに `v2.54.0` エントリを追記し、marketplace.json と完全に一致させる。追記内容:

```
v2.54.0: index.yaml branch index is keyed by `branch` (drop id/last_id/tags); legacy backlog migrated to index.archive.yaml.
```

位置は `v2.53.1` エントリの直後、`v2.55.0` エントリの直前。

## 水平展開

他のプラグイン（dev-kit / claude-kit / ref-inject）でも同様の description ドリフトが生じる可能性がある。プラグインを更新するたびに `plugin.json` と `marketplace.json` の description を diff ツールで照合する習慣を持つか、バージョン同期チェックリストに「description 完全一致確認」の項目を追加することを推奨する。
