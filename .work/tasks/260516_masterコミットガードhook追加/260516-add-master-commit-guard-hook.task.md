# PR17 — add-master-commit-guard-hook

## 概要

AI が master/main ブランチへ直接 `git commit` しようとするのを防ぐ PreToolUse フックを guard-kit に追加する。
guard-kit の既存 git-guard フックと同じトークン方式（1回ブロック→2回目許可）を採用。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | PreToolUse フックを追加（git commit + master/main 検出 → block） | - `plugins/guard-kit/hooks/hooks.json` |
| 済 | ブロック時のプロンプトファイルを作成 | - `plugins/guard-kit/hooks/prompts/master-commit-guard.md` |
| 済 | guard-kit バージョンを 1.0.0 → 1.1.0 に bump | - `plugins/guard-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし

## QA

なし
