# ISSUE-128: プラグイン設定.md のセクションタイトルが本文の条件と矛盾している

**作成日**: 2026-05-31

## 問題
`references/plugin/プラグイン設定.md` 行12のセクションタイトルが以下のように書かれている。

```
## Why every plugin needs a config skill
```

しかし行27の本文には：

```
Add a config skill when the plugin has one or more env toggles the user is expected to change.
```

とあり、「すべてのプラグイン」ではなく「env トグルを持つプラグインのみ」が対象である。実際、`references/plugin/プラグイン構造.md` の「Required skills」セクションも `plugin-config` を「mandatory for plugins with env vars」と明示している。

また JP ミラー（`プラグイン設定.jp.md`）行13のタイトルも「なぜすべてのプラグインに config スキルが必要か」と誤訳された状態で記述されている。

## 修正案

セクションタイトルを条件を反映した内容に修正する。例：

```
## Why plugins with env toggles need a config skill
```

JP ミラーも合わせて修正：

```
## env トグルを持つプラグインに config スキルが必要な理由
```
