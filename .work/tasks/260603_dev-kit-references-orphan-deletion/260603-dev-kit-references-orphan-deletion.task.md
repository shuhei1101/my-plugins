# dev-kit references ルート直下孤立ファイル削除

> ブランチ: `fix/delete-dev-kit-orphan-references`

## 概要

`plugins/dev-kit/references/` ルート直下に `マークダウン編集.md` と `マークダウン編集.jp.md` が残存している。これらは `markdown/` サブフォルダへの移動時に削除が漏れた孤立ファイルである。`_index.yaml` に未登録・どのパターンにもバインドされていない孤立ファイルを削除してリポジトリをクリーンにする。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | 未解決事項を `## QA` に記録する |
| 2 | 済 | ルート直下とmarkdown/配下のファイルの差分確認（diff一致確認） |
| 3 | 済 | ルート直下ファイルが _index.yaml に未登録・孤立であることを確認 |
| 4 | 済 | `plugins/dev-kit/references/マークダウン編集.md` を削除 |
| 5 | 済 | `plugins/dev-kit/references/マークダウン編集.jp.md` を削除 |
| 6 | 済 | 削除後に孤立参照が増えていないか確認 |
| 7 | 済 | `.work/notes/` の関連ノートを更新する |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/dev-kit/references/マークダウン編集.md` | 削除 | ルート直下の重複孤立ファイル削除 | markdown/配下に正規版あり |
| 2 | `plugins/dev-kit/references/マークダウン編集.jp.md` | 削除 | ルート直下の重複孤立ファイル削除（JPミラー） | markdown/配下に正規版あり |

## テスト

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | ルート直下と markdown/ 配下の .md ファイルが diff で完全一致 | diff exit code 0（完全一致） | OK |
| 2 | ルート直下と markdown/ 配下の .jp.md ファイルが diff で完全一致 | diff exit code 0（完全一致） | OK |
| 3 | ルート直下ファイルが _index.yaml に未登録 | `markdown/マークダウン編集.md` のみ登録、ルート直下は未登録 | OK |
| 4 | 削除後に _index.yaml の孤立参照が増えていないこと | 既存7件の孤立参照はmaster時点から存在し今回の削除と無関係 | OK |

## QA

QA なし。対応案確定済み。

## 参考ドキュメント

- `.work/notes/バグ・不具合/dev-kit-references-orphan-files.md`: 本件の孤立ファイル発生経緯と対処記録

## 関連イシュー

| # | ID | 概要 | resolution |
|---|---|---|---|
| 1 | ISSUE-135 | dev-kit: references/ ルート直下に マークダウン編集.md の重複ファイルが残存 | resolved |

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | (なし) | |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | (なし) | | |
