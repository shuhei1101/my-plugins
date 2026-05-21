# PR61 — merge-conversation-skills

## 概要

`conversation-to-skill` と `conversation-to-rule` を統合し、
hook-creator・claude-creator も含む新スキル `conversation-capture` を作成する。
会話履歴を分析して最適なアーティファクト種別（スキル/ルール/フック/CLAUDE.md）を提案し、
ユーザーが選択したものを対応するクリエイタースキルで実装する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | - `.work/tasks/.../PR61/QA.md` |
| - | `.work/specs/` の仕様書を更新する | - `.work/specs/claude-kit-conversation-skills.md` |
| - | 新スキル `conversation-capture` の SKILL.jp.md を作成する | - `plugins/claude-kit/skills/conversation-capture/SKILL.jp.md` |
| - | 新スキル `conversation-capture` の SKILL.md を作成する | - `plugins/claude-kit/skills/conversation-capture/SKILL.md` |
| - | 旧スキル `conversation-to-skill` を削除する | - `plugins/claude-kit/skills/conversation-to-skill/` |
| - | 旧スキル `conversation-to-rule` を削除する | - `plugins/claude-kit/skills/conversation-to-rule/` |
| - | plugin.json のスキル登録を更新する | - `plugins/claude-kit/.claude-plugin/plugin.json` |
| - | ルール・CLAUDE.md を整備する | - 不要 |

## 参考ドキュメント

- `.work/specs/claude-kit-conversation-skills.md`: 会話スキル仕様書
