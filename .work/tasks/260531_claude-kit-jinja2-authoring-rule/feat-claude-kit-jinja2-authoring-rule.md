# feat/claude-kit-jinja2-authoring-rule

> 内部 ID: 227（index.yaml 採番用 — クロスリファレンス目的）

## 概要

claude-kit / dev-kit の注入フックが使用する Jinja2 テンプレート（`.j2` ファイル）には、
`trim_blocks=True` / `lstrip_blocks=True` の設定に起因する罠がいくつかある。
PR201 で発覚した setext heading バグや `##` ヘッダー内の `{{ }}` レンダリングバグなどを
`references/jinja2/` フォルダにまとめてドキュメント化する。

テンプレートを新規作成・編集する際に Claude が参照できる注意事項集として機能させる。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 | 対象ファイル |
|---|---|---|---|
| 1 | - | QA に未決事項があれば記録する | - |
| 2 | - | .work/notes/ の関連ノートを更新する | - |
| 3 | - | references/jinja2/authoring.md を新規作成する（trim_blocks、setext heading、## ヘッダー内 {{ }} などの注意点） | plugins/claude-kit/references/jinja2/authoring.md |
| 4 | - | references/jinja2/authoring.jp.md を新規作成する（JP ミラー） | plugins/claude-kit/references/jinja2/authoring.jp.md |
| 5 | - | references/_index.yaml に jinja2/authoring.md を追加する | plugins/claude-kit/references/_index.yaml |
| 6 | - | references/_index.jp.yaml にも同様に追加する | plugins/claude-kit/references/_index.jp.yaml |
| 7 | - | references/_injection_rules.yaml に .j2 ファイルへのパターンを追加して自動注入を有効化する | plugins/claude-kit/references/_injection_rules.yaml |
| 8 | - | dev-kit 側も同期する（kit-hooks-sync.md の規約に従い、構造変更を両 kit に適用） | plugins/dev-kit/references/jinja2/authoring.md, plugins/dev-kit/references/_index.yaml, plugins/dev-kit/references/_injection_rules.yaml |
| 9 | - | CLAUDE.md / CLAUDE.jp.md を更新する | plugins/claude-kit/CLAUDE.md, plugins/claude-kit/CLAUDE.jp.md |
| 10 | - | plugin.json のバージョンを上げる | plugins/claude-kit/.claude-plugin/plugin.json, .claude-plugin/marketplace.json |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | plugins/claude-kit/references/jinja2/authoring.md | 新規 | Jinja2 テンプレート記法の注意事項（英語） | - |
| 2 | plugins/claude-kit/references/jinja2/authoring.jp.md | 新規 | 同上の JP ミラー | - |
| 3 | plugins/claude-kit/references/_index.yaml | 編集 | jinja2/authoring.md エントリを追加 | - |
| 4 | plugins/claude-kit/references/_index.jp.yaml | 編集 | 同上の JP ミラー | - |
| 5 | plugins/claude-kit/references/_injection_rules.yaml | 編集 | .j2 ファイルパターンを追加 | - |
| 6 | plugins/dev-kit/references/jinja2/authoring.md | 新規 | dev-kit 側に同期（claude-kit と同一内容） | kit-hooks-sync 規約 |
| 7 | plugins/dev-kit/references/jinja2/authoring.jp.md | 新規 | 〃 JP ミラー | 〃 |
| 8 | plugins/dev-kit/references/_index.yaml | 編集 | 〃 エントリ追加 | 〃 |
| 9 | plugins/dev-kit/references/_injection_rules.yaml | 編集 | 〃 .j2 パターン追加 | 〃 |
| 10 | plugins/claude-kit/CLAUDE.md | 編集 | Changelog 追加 | - |
| 11 | plugins/claude-kit/CLAUDE.jp.md | 編集 | 同上の JP ミラー | - |
| 12 | plugins/claude-kit/.claude-plugin/plugin.json | 編集 | バージョンアップ | MINOR |
| 13 | .claude-plugin/marketplace.json | 編集 | バージョン同期 | - |

## テスト

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | (テストなし) | - | - | - |

## QA

QA 事項なし。

## 参考ドキュメント

- plugins/claude-kit/references/kit-hooks-sync.md: dev-kit / claude-kit 構造同期規約
- .work/notes/Jinja2テンプレート記法メモ.md: Jinja2 テンプレート記法の既知の罠メモ

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | feat/claude-kit-jp-mirror-env (PR201) | trim_blocks バグと ## ヘッダーバグを発見・修正したブランチ |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
