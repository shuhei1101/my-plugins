# PR70 — conversation-to-claude-existing-check

## 概要

conversation-to-claude スキルに「既存アーティファクト確認」ステップを挿入する。
提案フォーマットにも「新規作成 / 既存を編集」を明示し、管理コスト増大を防ぐ。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | QA.md に未決定事項を記録する | `.work/tasks/20260523_conversation-to-claude-existing-check/PR70/QA.md` |
| - | スペックを更新する | `.work/specs/` |
| - | SKILL.md: 旧ステップ2〜4を3〜5へ繰り下げ、ステップ2「既存確認」を挿入 | `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| - | SKILL.md: 提案フォーマットに「操作: 新規作成 / 既存を編集 — {path}」行を追加 | `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| - | SKILL.jp.md: 同上（日本語版） | `plugins/claude-kit/skills/conversation-to-claude/SKILL.jp.md` |
| - | plugin.json / marketplace.json: バージョンバンプ | `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/claude-kit/skills/conversation-to-claude/SKILL.md`: 編集対象スキル

## 次PR候補

| タイトル | 概要 |
|---|---|
| - | - |
