# feat/claude-kit-jinja2-authoring-rule

> 内部 ID: 227（index.yaml 採番用 — クロスリファレンス目的）

## 概要

claude-kit / dev-kit の注入フックが使用する Jinja2 テンプレート（`.j2` ファイル）には、
`trim_blocks=True` / `lstrip_blocks=True` の設定に起因する罠がいくつかある。
PR201 で発覚した setext heading バグや `##` ヘッダー内の `{{ }}` レンダリングバグなどを
`references/jinja2/` フォルダにまとめてドキュメント化する。

テンプレートを新規作成・編集する際に Claude が参照できる注意事項集として機能させる。

**dev-kit 同期不要**: kit-hooks-sync.md の規約に従い、content-only 変更（リファレンス追加・パターン追加）は
クロスキット同期不要。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 | 対象ファイル |
|---|---|---|---|
| 1 | 済 | QA に未決事項があれば記録する（なし） | - |
| 2 | 済 | .work/notes/Jinja2テンプレート記法メモ.md を新規作成する | .work/notes/Jinja2テンプレート記法メモ.md |
| 3 | 済 | references/jinja2/authoring.md を新規作成する | plugins/claude-kit/references/jinja2/authoring.md |
| 4 | 済 | references/jinja2/authoring.jp.md を新規作成する（JP ミラー） | plugins/claude-kit/references/jinja2/authoring.jp.md |
| 5 | 済 | references/_index.yaml に jinja2/authoring.md を追加する | plugins/claude-kit/references/_index.yaml |
| 6 | 済 | references/_index.jp.yaml にも同様に追加する | plugins/claude-kit/references/_index.jp.yaml |
| 7 | 済 | references/_injection_rules.yaml の .j2 パターンに jinja2/authoring.md を追加する | plugins/claude-kit/references/_injection_rules.yaml |
| 8 | 済 | CLAUDE.md / CLAUDE.jp.md に Changelog を追記する | plugins/claude-kit/CLAUDE.md, plugins/claude-kit/CLAUDE.jp.md |
| 9 | 済 | plugin.json のバージョンを 3.46.0 → 3.47.0 に上げる | plugins/claude-kit/.claude-plugin/plugin.json, .claude-plugin/marketplace.json |
| 10 | 済 | changelogs/v3.47.0.md を作成する | plugins/claude-kit/changelogs/v3.47.0.md |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | plugins/claude-kit/references/jinja2/authoring.md | 新規 | Jinja2 テンプレート記法の注意事項（英語） | - |
| 2 | plugins/claude-kit/references/jinja2/authoring.jp.md | 新規 | 同上の JP ミラー | - |
| 3 | plugins/claude-kit/references/_index.yaml | 編集 | jinja2/authoring.md エントリを追加 | - |
| 4 | plugins/claude-kit/references/_index.jp.yaml | 編集 | 同上の JP ミラー | - |
| 5 | plugins/claude-kit/references/_injection_rules.yaml | 編集 | .j2 パターンに jinja2/authoring.md を追加 | - |
| 6 | plugins/claude-kit/CLAUDE.md | 編集 | Changelog に 3.47.0 を追記 | - |
| 7 | plugins/claude-kit/CLAUDE.jp.md | 編集 | 同上の JP ミラー | - |
| 8 | plugins/claude-kit/.claude-plugin/plugin.json | 編集 | バージョン 3.46.0 → 3.47.0 | MINOR |
| 9 | .claude-plugin/marketplace.json | 編集 | claude-kit バージョン同期 | - |
| 10 | plugins/claude-kit/changelogs/v3.47.0.md | 新規 | バージョン変更記録 | - |

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
