# post-commit-deletion-check — 大量削除検知 Stop hook

## 概要

レスポンス終了時に直近 N コミットの削除ファイル数を計測し、閾値超なら警告コンテキストを注入する。
block しない — 気付かせるだけ。マージ事故で大量ファイルが消えた直後にメインエージェントへ通知するのが目的。

## 仕様

| 項目 | 値 |
| --- | --- |
| 計測コマンド | `git log --diff-filter=D --name-only --pretty=format: HEAD~N..HEAD` |
| デフォルト閾値 | 30 件（env `WORK_DELETION_THRESHOLD` で変更可） |
| デフォルト遡行数 | 5 コミット（env `WORK_DELETION_LOOKBACK` で変更可） |
| 履歴不足時 | 黙ってスキップ（`HEAD~N` が無い場合の returncode 非ゼロ扱い） |
| サンプル表示 | 削除ファイルの先頭 10 件をコンテキストに含める |

## 参考リンク

- `plugins/work/hooks/stop/post-commit-deletion-check.py`: フックスクリプト本体
