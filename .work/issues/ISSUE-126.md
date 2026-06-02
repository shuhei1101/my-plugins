# ISSUE-126: _index.yaml の プラグイン構造.md 説明に旧スキル名 plugin-update が残存

**作成日**: 2026-05-31

## 概要

`references/.ref-injects/_index.yaml` の `plugin/プラグイン構造.md` エントリの description に、現在使われていない旧スキル名 `plugin-update` と省略形 `config` が残っている。

## 背景

本文のスキル名変更時に、`_index.yaml` の description は見落とされやすい。

## 現状

`_index.yaml` の `plugin/プラグイン構造.md` エントリの description:

```yaml
description: How to author or update a plugin. Standard directory layout, plugin.json fields,
  marketplace.json entry, create-vs-update mode, version bump rules, required skills
  (plugin-update, setup-wizard, config), and zero inter-plugin dependency principle.
```

`references/plugin/プラグイン構造.md` 本文では行 78 から一貫して `plugin-migrate` と呼ばれており、`plugin-update` という名称は現在使用されていない（行 105 には「not `<plugin>-update`」と明示的に禁止まで記載）。また同 description で required skills に `config` とあるが、正式名は `plugin-config` である。

## 期待される状態

`_index.yaml`（および `_index.jp.yaml`）の description が本文と一致し、旧スキル名・省略形が解消されている。

## 対応案

`_index.yaml` の当該エントリの description を以下のように修正する。

- `plugin-update` → `plugin-migrate`
- `config` → `plugin-config`

対応する `_index.jp.yaml` も同様に修正する。

## 横展開

`_index.yaml` の description は本文変更時に見落とされやすい。本文のスキル名変更時に `_index.yaml` description も必ず確認するよう、`plugin-migrate` のチェックリストに追加することを推奨する。

---

# ユーザー回答欄

> 回答方法: 各 `**回答**:` 行で不要な選択肢を消し、1 つだけ残す（`{回答を入力}` は自由記入）。
> AI は選択肢・推奨と、候補を並べた `**回答**:` 行まで用意する。

## 意思

このイシューに対応するか。

**回答**: 対応する / 対応しない
