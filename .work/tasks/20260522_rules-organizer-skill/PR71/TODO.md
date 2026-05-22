# PR71 — claude-refactor

## 概要

`rules-organizer` スキルを拡張し、Claude 設定全体（rules / skills / CLAUDE.md / hooks）を
監査・整理する `claude-refactor` スキルに変更する。
重複ルール・スキルの統合提案、CLAUDE.md ↔ rules/hooks の移管提案など
設定の肥大化を防ぐ総合オーガナイザーとして再設計する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する（なし） | `.work/tasks/.../PR71/QA.md` |
| 済 | SKILL.jp.md を新設計で書き直す | `plugins/claude-kit/skills/claude-refactor/SKILL.jp.md` |
| 済 | SKILL.md を英語に翻訳する | `plugins/claude-kit/skills/claude-refactor/SKILL.md` |
| 済 | スキル名・フォルダ名を `claude-refactor` にリネームする | `plugins/claude-kit/skills/` |
| 済 | 参照元を更新する（glossary.md） | `.claude/rules/glossary.md` |
| 済 | plugin.json / marketplace.json のバージョンをバンプする | `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| 済 | レビュー反映（分離候補・JPミラー・クリエータースキル明示） | `plugins/claude-kit/skills/claude-refactor/SKILL.jp.md`, `SKILL.md` |
| 済 | ユースケース思考・ルール2種類の定義を追記 | `plugins/claude-kit/skills/claude-refactor/SKILL.jp.md`, `SKILL.md` |
| 済 | ルール・CLAUDE.md を整備する（変更不要と確認） | — |

## 参考ドキュメント

- `plugins/claude-kit/skills/claude-refactor/SKILL.jp.md`: 改修済みスキル
- `plugins/claude-kit/skills/rule-creator/SKILL.jp.md`: ルールの定義基準
- `plugins/claude-kit/skills/skill-creator/SKILL.jp.md`: スキルの定義基準
- `plugins/claude-kit/skills/hook-creator/SKILL.jp.md`: フックの定義基準
- `plugins/claude-kit/skills/claude-creator/SKILL.jp.md`: CLAUDE.md の定義基準

## 次PR候補

| タイトル | 概要 |
|---|---|
| conversation-to-claude に claude-refactor を登録 | conversation-to-claude の Step 3 デリゲート表に claude-refactor を追加する候補 |
