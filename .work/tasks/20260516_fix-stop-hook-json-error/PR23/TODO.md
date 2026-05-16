# PR23 — fix-stop-hook-json-error

## 概要

Stop フックの Python スクリプトが `json.loads(sys.stdin.read())` で Claude Code からの入力を
パースする際、JSON が壊れていると例外が発生しノンゼロ終了していた。
`try/except` を追加して堅牢化し、サブエージェントで動作確認テストを実施する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | Stop フックに try/except を追加（JSON パース失敗時は sys.exit(0)） | - `plugins/work-kit/hooks/hooks.json` |
| 済 | サブエージェントを使って Stop フックの動作を確認 | - |

## 参考ドキュメント

- なし
