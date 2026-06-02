# PR24 — add-todo-append-step

## 概要

UserPromptSubmit フックのステップ2に2つの改善を追加する。
1. ワークツリーへの移動手順（QA/TODO を正しい場所から読むため）
2. 今回の依頼内容が TODO に未掲載の場合、作業前に自動追記するステップ

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | JP ミラーを更新（ステップ2の処理内容を修正） | - `plugins/work-kit/hooks/prompts/user-prompt-submit.jp.md` |
| 済 | 英語版を同様に更新 | - `plugins/work-kit/hooks/prompts/user-prompt-submit.md` |
| 済 | バージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/hooks/prompts/user-prompt-submit.md`: 変更対象のフックプロンプト

## QA

なし
