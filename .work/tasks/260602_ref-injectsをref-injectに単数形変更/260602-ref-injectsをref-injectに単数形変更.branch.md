# .ref-injects を .ref-inject に単数形変更

> ブランチ: `refactor/rename-ref-injects-to-ref-inject`

## 概要

全プラグインの `references/.ref-injects/` ディレクトリ名が複数形になっている。
これを単数形 `.ref-inject/` に統一する。対象は `inject_references.py` スクリプト、
スキル定義ファイルなど `.ref-injects` を参照するすべての箇所。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | 未解決事項を `## QA` に記録する（なし） |
| 2 | 済 | `.ref-injects` ディレクトリを `.ref-inject` にリネーム（claude-kit / dev-kit / ref-inject テンプレート / work） |
| 3 | 済 | `inject_references.py` の `.ref-injects` 参照を `.ref-inject` に更新（全4プラグイン） |
| 4 | 済 | `_injection_rules.yaml` 内のパターン参照を `.ref-inject` に更新（claude-kit） |
| 5 | 済 | `.work/notes/` にノートを新規作成し `_index.md` に登録 |

## 変更内容

実装したファイル（テスト以外）。コミットに積まれる全ファイルを列挙する。

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/claude-kit/references/.ref-injects/` → `.ref-inject/` (5ファイル) | リネーム | ディレクトリ単数形化 | git mv |
| 2 | `plugins/dev-kit/references/.ref-injects/` → `.ref-inject/` (3ファイル) | 〃 | 〃 | 〃 |
| 3 | `plugins/ref-inject/templates/references/.ref-injects/` → `.ref-inject/` (5ファイル) | 〃 | 〃 | 〃 |
| 4 | `plugins/work/references/.ref-injects/` → `.ref-inject/` (5ファイル) | 〃 | 〃 | 〃 |
| 5 | `plugins/claude-kit/hooks/scripts/inject_references.py` | 編集 | `.ref-injects` → `.ref-inject` に変更 | |
| 6 | `plugins/dev-kit/hooks/scripts/inject_references.py` | 〃 | 〃 | |
| 7 | `plugins/ref-inject/templates/hooks/scripts/inject_references.py` | 〃 | 〃 | |
| 8 | `plugins/work/hooks/scripts/inject_references.py` | 〃 | 〃 | |
| 9 | `plugins/claude-kit/references/.ref-inject/_injection_rules.yaml` | 編集 | パターン内 `.ref-injects` → `.ref-inject` に更新 | |

## テスト

手動テスト・動作確認の実施記録。

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | `.ref-injects` → `.ref-inject` にリネームした全プラグインで参照が切れないこと | `grep -r ".ref-injects" plugins/` → 0件 | OK |

## QA

このブランチのスコープの未決定事項を QA-XXX として記録する。決定後は本文の該当箇所に反映する。

(なし)

## 参考ドキュメント

- [ref-inject ディレクトリ命名 — 単数形統一](.work/notes/プラグイン構成・統合/ref-injectディレクトリ単数形統一.md)

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | (なし) | - |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | (なし) | - | - |
