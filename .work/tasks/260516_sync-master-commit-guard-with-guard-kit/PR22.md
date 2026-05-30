# PR22 — sync-master-commit-guard-with-guard-kit

## 概要

master-commit-guard フックを guard-kit の git-guard と同じパターンに統一する。

現状（PR21 後）: フック自体はトークンを作成せず、常時ブロック。
目標: guard-kit と同じ「1回目ブロック+トークン作成、2回目トークン消費でALLOW」パターン。
worktree 対応（cd / git -C パス検出）は維持する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | hooks.json を guard-kit パターンに合わせる（トークン作成+ブロック → 2回目ALLOW）＋ worktree 対応維持 | - `plugins/work-kit/hooks/hooks.json` |
| 済 | master-commit-guard.md を 316c081 以前のシンプルなメッセージに差し戻し | - `plugins/work-kit/hooks/prompts/master-commit-guard.md` |
| 済 | master-commit-guard.jp.md を同様に差し戻し | - `plugins/work-kit/hooks/prompts/master-commit-guard.jp.md` |
| 済 | work-kit バージョンを bump (2.6.8 → 2.6.9) | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/guard-kit/hooks/hooks.json`: 参照元パターン
- `plugins/guard-kit/hooks/prompts/git-guard.md`: 参照元プロンプト

## QA

なし
