# PR42 — master-commit-guard-improve

## 概要

`develop` ブランチもガード対象に追加し、フック実行時に `git status` を自動実行してその結果をプロンプトに渡すよう改善する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | `develop` ブランチをガード対象に追加 | - `plugins/work-kit/hooks/hooks.json` |
| - | フック実行時に `git status` を自動実行し出力をブロック理由に含める | - `plugins/work-kit/hooks/hooks.json` |
| - | プロンプトから手動 `git status` の指示を削除し、渡された結果を参照するよう更新（EN） | - `plugins/work-kit/hooks/prompts/master-commit-guard.md` |
| - | プロンプトから手動 `git status` の指示を削除し、渡された結果を参照するよう更新（JP） | - `plugins/work-kit/hooks/prompts/master-commit-guard.jp.md` |
| - | バージョンバンプ | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
