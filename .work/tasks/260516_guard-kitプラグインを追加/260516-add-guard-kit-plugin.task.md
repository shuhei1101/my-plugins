# PR13 — add-guard-kit-plugin

## 概要

`work-kit` プラグインに含まれていた git-guard フック（`git push` / `git merge` 前にユーザー確認を強制する `PreToolUse` フック）を、セキュリティ・安全作業系ガードをまとめる新プラグイン `guard-kit` として切り出す。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `guard-kit` プラグイン新規作成（`plugin.json`） | - `plugins/guard-kit/.claude-plugin/plugin.json` |
| 済 | `marketplace.json` に `guard-kit` を登録 | - `.claude-plugin/marketplace.json` |
| 済 | git-guard フックを `guard-kit/hooks/hooks.json` に移植 | - `plugins/guard-kit/hooks/hooks.json` |
| 済 | git-guard プロンプトファイルを `guard-kit` に移動 | - `plugins/guard-kit/hooks/prompts/git-guard.md`<br>- `plugins/guard-kit/hooks/prompts/git-guard.jp.md` |
| 済 | `work-kit/hooks/hooks.json` から git-guard エントリを削除 | - `plugins/work-kit/hooks/hooks.json` |
| 済 | `work-kit` バージョンバンプ（PATCH） | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `.work/specs/guard-kit.md`: guard-kit プラグイン仕様

## QA

なし
