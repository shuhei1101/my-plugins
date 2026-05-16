# PR18 — move-commit-guard-to-work-kit

## 概要

master-commit-guard フックを guard-kit から work-kit へ移動する。
あわせて `.work/tasks/.gitignore` を追加し `index.yaml` をgit管理外にする。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | guard-kit から master-commit-guard フック・プロンプトを削除し、バージョンを 1.2.0 に上げる | - `plugins/guard-kit/hooks/hooks.json`<br>- `plugins/guard-kit/hooks/prompts/master-commit-guard.md`<br>- `plugins/guard-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| 済 | work-kit に master-commit-guard フック・プロンプトを追加し、バージョンを 2.6.5 に上げる | - `plugins/work-kit/hooks/hooks.json`<br>- `plugins/work-kit/hooks/prompts/master-commit-guard.md`<br>- `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| 済 | master-commit-guard.md（英語）と master-commit-guard.jp.md（日本語）を用意し、フックは英語版を使用 | - `plugins/work-kit/hooks/prompts/master-commit-guard.md`<br>- `plugins/work-kit/hooks/prompts/master-commit-guard.jp.md` |
| 済 | `.work/tasks/.gitignore` を作成して `index.yaml` を除外 + git untrack | - `.work/tasks/.gitignore` |

## 参考ドキュメント

- なし
