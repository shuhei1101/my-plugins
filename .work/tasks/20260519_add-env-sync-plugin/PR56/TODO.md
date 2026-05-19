# PR56 — add-env-sync-plugin

## 概要

WSL ↔ Windows 間で Claude Code の設定ファイル（settings.json、CLAUDE.md、スキル等）を
コピー・同期するプラグインを my-plugins に追加する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/20260519_add-env-sync-plugin/PR56/QA.md` |
| 済 | spec を新規作成する | - `.work/specs/env-sync-plugin.md` |
| 済 | claude-kit に env-sync スキルを追加する | - `plugins/claude-kit/skills/env-sync/SKILL.md` |
| 済 | marketplace.json / plugin.json をバージョンアップする | - `.claude-plugin/marketplace.json`, `plugins/claude-kit/.claude-plugin/plugin.json` |
| - | ルール・CLAUDE.md を整備する | - 必要に応じて |

## 参考ドキュメント

- `.work/specs/env-sync-plugin.md`: プラグイン仕様
