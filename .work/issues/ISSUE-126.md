---
decision: pending
status: not_started
branches: []
instruction: ""
---

# ISSUE-126: _index.yaml の プラグイン構造.md 説明に旧スキル名 plugin-update が残存

**作成日**: 2026-05-31

## 問題
`references/.ref-injects/_index.yaml` の `plugin/プラグイン構造.md` エントリの description に `plugin-update` という旧スキル名が残っている。

```yaml
description: How to author or update a plugin. Standard directory layout, plugin.json fields,
  marketplace.json entry, create-vs-update mode, version bump rules, required skills
  (plugin-update, setup-wizard, config), and zero inter-plugin dependency principle.
```

`references/plugin/プラグイン構造.md` 本文では行78から一貫して `plugin-migrate` と呼ばれており、`plugin-update` という名称は現在使用されていない（行105には「not `<plugin>-update`」と明示的に禁止まで記載）。

また同 description で required skills に `config` とあるが、正式名は `plugin-config` である（`plugin-config` が正しい名称として本文に記述されている）。

## 修正案

`_index.yaml` の当該エントリの description を以下のように修正する。

- `plugin-update` → `plugin-migrate`
- `config` → `plugin-config`

対応する `_index.jp.yaml` も同様に修正する。

## 水平展開
`_index.yaml` の description は本文変更時に見落とされやすい。本文のスキル名変更時に `_index.yaml` description も必ず確認するよう、`plugin-migrate` のチェックリストに追加することを推奨する。
