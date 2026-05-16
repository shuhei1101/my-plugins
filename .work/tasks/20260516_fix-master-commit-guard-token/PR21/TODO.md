# PR21 — fix-master-commit-guard-token

## 概要

`plugins/work-kit/hooks/hooks.json` の PreToolUse (master-commit-guard) にトークンロジックのバグがある。
「トークンが存在する場合はトークンを削除して `exit(0)` = ALLOW」という挙動になっているため、
1回目はブロック、2回目は通過するという交互動作が発生する。

修正方針: トークン制御ロジックを削除し、master/main への `git commit` を常にブロックする。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | PreToolUse ハンドラーのトークン制御ロジック（token.unlink/touch 部分）を削除 | - `plugins/work-kit/hooks/hooks.json` |
| - | サブエージェントで動作検証 | - |
| - | work-kit プラグインのバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/hooks/hooks.json`: 修正対象フック定義
- `plugins/work-kit/hooks/prompts/master-commit-guard.md`: ブロック時のメッセージ
