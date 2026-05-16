# PR25 — allow-merge-commit

## 概要

`master-commit-guard` フックがマージ中でも `git commit -m` をブロックしてしまう問題を修正する。
`MERGE_HEAD` が存在する場合（マージコミット実行中）はガードをスキップして許可する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | master-commit-guard フックに MERGE_HEAD チェックを追加してマージ中はスキップ | - `plugins/work-kit/hooks/hooks.json` |
| - | plugin.json と marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし
