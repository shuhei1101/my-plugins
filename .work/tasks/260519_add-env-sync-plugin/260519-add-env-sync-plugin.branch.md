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
| 済 | SKILL.jp.md をフォーマット準拠版に書き直す | - `plugins/claude-kit/skills/env-sync/SKILL.jp.md` |
| 済 | SKILL.md を完全英語版に統一する | - `plugins/claude-kit/skills/env-sync/SKILL.md` |
| 済 | ルール・CLAUDE.md を整備する（変更不要と判断） | - 不要 |

## 参考ドキュメント

- `.work/specs/env-sync-plugin.md`: プラグイン仕様

## QA

なし
