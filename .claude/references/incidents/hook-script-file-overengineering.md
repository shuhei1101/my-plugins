# 単純なフックに Python スクリプトファイルを作成した（過剰設計）

## 日付

2026-05-24

## 何が起きたか

ui-kit の UserPromptSubmit フックを実装した際、以下のファイルを作成した:
- `hooks/scripts/user-prompt-submit.py` — キーワード検出スクリプト
- `hooks/prompts/base.md` — implement + logging リマインダー
- `hooks/prompts/with-mock.md` — implement + logging + mock リマインダー

これは work-kit の複雑な UserPromptSubmit フック実装を参考にしたが、ui-kit の要件には過剰だった。

## 原因

work-kit の `hooks/scripts/user-prompt-submit.py` は複雑な PR 状態チェックロジックを持つため別ファイルが適切。
しかし ui-kit はキーワード検出 + ファイル参照出力という単純な処理しか必要としていなかった。
単純な処理でも自動的にスクリプトファイルを作る習慣が過剰設計を招いた。

## 修正

- Python スクリプトファイルを削除
- 複数プロンプトファイルを1本 (`ui-skill-reminder.md`) に統合（条件分岐はファイル内の記述で対応）
- `hooks.json` のインライン Python でキーワード検出を実装

## 教訓

**単純なフックはインライン Python + 単一 MD ファイルで実装する。**
Python スクリプトファイル（`hooks/scripts/*.py`）は、ロジックが複雑で独立テスト・再利用が必要な場合のみ作成する。
プロンプトファイルの分割は「Claude が状況によって読み分ける必要がある場合」のみで、単一ファイルに「状況に応じて使い分けてね」と書く方がシンプル。
