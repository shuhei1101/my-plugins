# PR79 — conversation-to-claude-auto

## 概要

`conversation-to-claude` スキルの確認ステップを削除し、完全自動で全アーティファクトを作成するよう改修する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/20260523_conversation-to-claude-auto/PR79/QA.md` |
| 済 | Step 3 のユーザー確認プロンプトを削除し自動実行に変更 | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| 済 | Step 5 のコミット確認を削除し自動コミットに変更 | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| 済 | SKILL.jp.md を同期更新 | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.jp.md` |
| 済 | plugin.json / marketplace.json バージョンバンプ | - `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし（既存スキル改修）

| 済 | references/common.md にアーティファクト増殖ガードセクション追加 | - `plugins/claude-kit/references/common.md` |
| 済 | references/common.jp.md も同期更新 | - `plugins/claude-kit/references/common.jp.md` |
| 済 | conversation-to-claude Step 2 で common.md を読み込み増殖ガードを適用 | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.md` |
| 済 | conversation-to-claude SKILL.jp.md も同期更新 | - `plugins/claude-kit/skills/conversation-to-claude/SKILL.jp.md` |
| 済 | plugin.json / marketplace.json バージョンバンプ | - `plugins/claude-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 次PR候補

| タイトル | 概要 |
|---|---|
| — | — |

## QA

なし
