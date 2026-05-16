# PR21 — fix-master-commit-guard-token

## 概要

`plugins/work-kit/hooks/hooks.json` の PreToolUse (master-commit-guard) にトークンロジックのバグがある。
「トークンが存在する場合はトークンを削除して `exit(0)` = ALLOW」という挙動になっているため、
1回目はブロック、2回目は通過するという交互動作が発生する。

修正方針: トークン制御ロジックを削除し、master/main への `git commit` を常にブロックする。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | cd/git -C のパスを検出して実ブランチを確認するよう修正 | - `plugins/work-kit/hooks/hooks.json` |
| 済 | トークンはフック自体でなく Claude がユーザー確認後に作成する設計に変更 | - `plugins/work-kit/hooks/hooks.json` |
| 済 | master-commit-guard.md / jp.md にトークン作成コマンドを追記 | - `plugins/work-kit/hooks/prompts/master-commit-guard.md`<br>- `plugins/work-kit/hooks/prompts/master-commit-guard.jp.md` |
| 済 | サブエージェントで動作検証（全6シナリオ合格） | - |
| 済 | work-kit プラグインのバージョンを bump (2.6.7 → 2.6.8) | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/hooks/hooks.json`: 修正対象フック定義
- `plugins/work-kit/hooks/prompts/master-commit-guard.md`: ブロック時のメッセージ
