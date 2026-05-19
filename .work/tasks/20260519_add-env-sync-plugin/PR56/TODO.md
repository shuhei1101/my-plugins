# PR56 — add-env-sync-plugin

## 概要

WSL ↔ Windows 間で Claude Code の設定ファイル（settings.json、CLAUDE.md、スキル等）を
コピー・同期するプラグインを my-plugins に追加する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | - `.work/tasks/20260519_add-env-sync-plugin/PR56/QA.md` |
| - | spec を新規作成する | - `.work/specs/env-sync-plugin.md` |
| - | プラグインディレクトリ構造を作成する | - `plugins/env-sync/` |
| - | plugin.json を作成する | - `plugins/env-sync/.claude-plugin/plugin.json` |
| - | WSL→Windows コピースキルを作成する | - `plugins/env-sync/skills/wsl-to-win/SKILL.md` |
| - | Windows→WSL コピースキルを作成する | - `plugins/env-sync/skills/win-to-wsl/SKILL.md` |
| - | marketplace.json に登録する | - `.claude-plugin/marketplace.json` |
| - | ルール・CLAUDE.md を整備する | - 必要に応じて |

## 参考ドキュメント

- `.work/specs/env-sync-plugin.md`: プラグイン仕様
