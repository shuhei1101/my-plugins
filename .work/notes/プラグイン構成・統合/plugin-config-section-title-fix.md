# プラグイン設定.md セクションタイトル修正メモ

## 背景

`plugins/claude-kit/references/plugin/プラグイン設定.md` の `## Why every plugin needs a config skill` というセクションタイトルが「すべてのプラグイン」に config スキルが必要と読めていたが、本文は「env トグルを持つプラグインのみ」を対象としており矛盾していた（ISSUE-128）。

## 修正内容

| ファイル | 旧タイトル | 新タイトル |
|---|---|---|
| `プラグイン設定.md` | `## Why every plugin needs a config skill` | `## Why plugins with env toggles need a config skill` |
| `プラグイン設定.jp.md` | `## なぜすべてのプラグインに config スキルが必要か` | `## env トグルを持つプラグインに config スキルが必要な理由` |

## ポイント

- 本文（行 27）の条件 `Add a config skill when the plugin has one or more env toggles` は既に正しかったため変更なし。
- タイトルと本文の一貫性を保つことが重要。「every plugin」は「plugins with env toggles」への絞り込みが必要。
- `プラグイン構造.md` の `Required skills` セクションも `plugin-config` を「mandatory for plugins with env vars」と明示している。
