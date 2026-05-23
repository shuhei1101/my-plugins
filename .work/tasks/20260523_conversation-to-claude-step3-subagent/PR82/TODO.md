# PR82 — conversation-to-claude Step3 サブエージェント化

## 概要

conversation-to-claude の Step 3 を、メインエージェントが逐次処理する方式から
サブエージェントを使って並列実装する方式に書き換える。
スキル・ルール・フック・CLAUDE.md は各カテゴリ1つのサブエージェントに委譲し、
incidents/glossary はメインエージェントが直接処理する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/.../PR82/QA.md` |
| 済 | SKILL.md (EN) の Step 3 をサブエージェント方式に書き換える | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| 済 | SKILL.jp.md (JP) の Step 3 をサブエージェント方式に書き換える | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.jp.md` |
| 済 | 各サブエージェントへの入力テンプレートを定型文化して記述する | - 上記2ファイル |
| 済 | Step 4: 検証セクションを追加する | - 上記2ファイル |
| 済 | コミットする | - |

## 参考ドキュメント

- `plugins/claude-kit/skills/conversation-to-claude/SKILL.md`: 変更対象

## 次PR候補

| タイトル | 概要 |
|---|---|
| - | - |
