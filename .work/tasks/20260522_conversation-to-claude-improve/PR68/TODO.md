# PR68 — conversation-to-claude-improve

## 概要

conversation-to-claude スキルの提案品質を改善する。
① 提案を「通常2〜3個」から「余すことなく全件」に変更
② 提案前（Step 0）に skill-creator / rule-creator / claude-creator を読んでから提案する

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/20260522_conversation-to-claude-improve/PR68/QA.md` |
| 済 | Step 0 を追加: 提案前にクリエータースキルを読む | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| 済 | Step 1 の抽出指示を「余すことなく全件」に強化 | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| 済 | Step 2 の "usually 2-3" 記述を削除し全件提案に変更 | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| 済 | SKILL.jp.md を同期更新 | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.jp.md` |
| 済 | plugin.json / marketplace.json のバージョンを上げる | - `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

| - | Step 2 提案フォーマットのルール説明を強化: ファイルリンク用ルールを明示的に提案する | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| - | Step 2 の「適用パス」という表現を修正: paths: が「読んだ時に発動」する仕組みを正確に説明 | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| - | SKILL.jp.md を同期更新 | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.jp.md` |

## 参考ドキュメント

- `plugins/claude-kit/skills/conversation-to-claude/SKILL.md`: 改修対象スキル
