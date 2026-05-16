# PR3 — add-hook-creator-skill

## 概要

claude-kit プラグインに `hook-creator` スキルを追加する。
特定のイベント発火時にプロンプトを Claude のコンテキストへ注入するフックを、
ユーザーの要件に応じて作成するスキル。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `hook-creator` スキル作成（日本語ミラー） | - `plugins/claude-kit/skills/hook-creator/SKILL.jp.md` |
| 済 | `hook-creator` スキル作成（英語版） | - `plugins/claude-kit/skills/hook-creator/SKILL.md` |
| 済 | `CLAUDE_PLUGIN_ROOT` 制約とプロジェクト用パターン追記 | - `plugins/claude-kit/skills/hook-creator/SKILL.jp.md`<br>- `plugins/claude-kit/skills/hook-creator/SKILL.md` |
| 済 | Stop フックパターンを stdout 方式に修正 | - `plugins/claude-kit/skills/hook-creator/SKILL.jp.md`<br>- `plugins/claude-kit/skills/hook-creator/SKILL.md` |
| 済 | claude-kit バージョン bump (3.2.0 → 3.3.0) | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| 済 | work-kit Stop フックを stdout 方式に統一 (2.3.5) | - `plugins/work-kit/hooks/hooks.json`<br>- `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/hooks/hooks.json`: Stop フックの実装参考
