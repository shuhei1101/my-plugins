# post-merge-upgrade 直接実行対応

## 概要

`python .claude/hooks/post-merge-upgrade.py` をコマンドラインから直接実行した際、何も処理されずに終了してしまう問題を修正する。

## 背景

このスクリプトは Claude Code のフック（PostToolUse）として動作するよう設計されており、stdin から JSON を受け取ることを前提としている。TTY 直接実行時は `d = {}` となり、`d.get("tool_name") != "Bash"` の条件で即 `sys.exit(0)` してしまっていた。

## 作業内容

| No | 作業 | 完了 |
| -- | ---- | ---- |
| 1  | `direct_run` フラグを導入し、TTY 直接実行時はフックチェックをスキップして本処理を実行するよう修正 | 済 |

## QA

なし

## 参考ドキュメント

- [post-merge-upgrade ノート](../../notes/hooks/post-merge-upgrade.md)
