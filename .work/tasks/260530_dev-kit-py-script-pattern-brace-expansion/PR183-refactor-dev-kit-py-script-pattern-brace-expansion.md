# PR183 — dev-kit-py-script-pattern-brace-expansion

## 概要

dev-kit の `references/injection_rules.yaml` に定義されている `python-script.md` 注入パターンは現状 `**/tools/**/*.py` と `**/scripts/**/*.py` の **複数形のみ** マッチする。単数形フォルダ（`tool/` / `script/`）配下のスクリプトには注入されず、`python-script.md` のガイドが届かない取りこぼしが発生する。

ブレース展開でまとめて `**/{tool,tools,script,scripts}/**/*.py` の 1 パターンに統合し、2 行→1 行に整理する。

### 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | `python-script.md` の 2 つのパターンをブレース展開で 1 行に統合 | - `plugins/dev-kit/references/injection_rules.yaml` |
| - | YAML パース検証（`yaml.safe_load` で読み込めることを確認） | - |
| - | orphan-check（既存 `python-script.md` がパターンに紐づき続けていること） | - |

## 変更内容

| ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|
| `plugins/dev-kit/references/injection_rules.yaml` | 編集 | `**/tools/**/*.py` と `**/scripts/**/*.py` の 2 エントリを `**/{tool,tools,script,scripts}/**/*.py` の 1 エントリに統合 | `python/scripts/python-script.md` の required は不変 |

## テスト

テスト変更なし。

## 参考ドキュメント

- `plugins/dev-kit/references/injection_rules.yaml`: 注入ルール本体
- `plugins/dev-kit/references/python/scripts/python-script.md`: 注入対象 reference
- インシデント `glob-pattern-missing-recursive-prefix`: glob パターンの設計教訓

## 関連PR

| PR番号 | 概要 |
|---|---|
| #PR166 | merge-language-plugins-into-dev-kit（dev-kit に注入ルールを統合） |

## 次PR候補

なし
