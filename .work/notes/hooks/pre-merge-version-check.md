# pre-merge-version-check — マージ前バージョンチェックフック

## 概要

master へのマージ前に変更プラグインのバージョン更新漏れを検出してブロックする。フック（シン・ラッパー）とツール（コア処理）に分離している。

## 構成

| 役割 | ファイル |
|---|---|
| フック（シン・ラッパー） | `.claude/hooks/pre-merge-version-check.py` |
| コア処理 | `tools/pre_merge_check.py` |

## フックの条件チェック

- `tool_name` が `Bash` であること
- コマンドに `git merge` を含むこと
- `git merge origin/master`（master 取り込み）はスキップ
- 現在ブランチが `master` であること

## コア処理の動作

`tools/pre_merge_check.py <merge_branch>` として起動する。問題がある場合は stdout に警告メッセージを出力、なければ何も出力しない。

チェック対象:
- 変更プラグインの `plugin.json` バージョンが master と同一かどうか
- `marketplace.json` の対象プラグインバージョンが更新されているかどうか

問題検出時は `bump-version.py` の実行コマンドを含む警告を表示して deny する。

## 参考リンク

- `.claude/hooks/pre-merge-version-check.py`: フック（シン・ラッパー）
- `tools/pre_merge_check.py`: コア処理
