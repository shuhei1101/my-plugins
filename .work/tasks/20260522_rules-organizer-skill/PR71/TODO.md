# PR71 — claude-organizer

## 概要

`rules-organizer` スキルを拡張し、Claude 設定全体（rules / skills / CLAUDE.md / hooks）を
監査・整理する `claude-organizer` スキルに変更する。
重複ルール・スキルの統合提案、CLAUDE.md ↔ rules/hooks の移管提案など
設定の肥大化を防ぐ総合オーガナイザーとして再設計する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | `.work/tasks/.../PR71/QA.md` |
| - | SKILL.jp.md を新設計で書き直す | `plugins/claude-kit/skills/rules-organizer/SKILL.jp.md` |
| - | SKILL.md を英語に翻訳する | `plugins/claude-kit/skills/rules-organizer/SKILL.md` |
| - | スキル名・フォルダ名を `claude-organizer` にリネームする | `plugins/claude-kit/skills/` |
| - | 参照元を更新する（rule-creator 依存関係ルール等） | `.claude/rules/claude-kit-skill-dependencies.md` 等 |
| - | plugin.json / marketplace.json のバージョンをバンプする | `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| - | ルール・CLAUDE.md を整備する | 必要に応じて |

## 参考ドキュメント

- `plugins/claude-kit/skills/rules-organizer/SKILL.jp.md`: 現行スキル（改修前）
- `plugins/claude-kit/skills/rule-creator/SKILL.jp.md`: ルールの定義基準
- `plugins/claude-kit/skills/skill-creator/SKILL.jp.md`: スキルの定義基準
- `plugins/claude-kit/skills/hook-creator/SKILL.jp.md`: フックの定義基準
- `plugins/claude-kit/skills/claude-creator/SKILL.jp.md`: CLAUDE.md の定義基準

## 次PR候補

| タイトル | 概要 |
|---|---|
| conversation-to-claude に claude-organizer を登録 | conversation-to-claude の Step 3 デリゲート表に claude-organizer を追加する候補 |
