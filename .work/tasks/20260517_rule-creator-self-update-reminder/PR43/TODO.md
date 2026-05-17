# PR43 — rule-creator-self-update-reminder

## 概要

rule-creator スキルが生成するルールテンプレートに「このルール自体の保守」セクションを追加する。
関連ファイルを追加・削除・リネームしたときにルール自体の更新を促す文言を、生成されるすべてのルールに含める。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | SKILL.jp.md の構造例テンプレートに「このルール自体の保守」セクションを追加 | - `plugins/claude-kit/skills/rule-creator/SKILL.jp.md` |
| 済 | 「編集時の確認事項」チェックリストに新規ファイル追加時の確認項目を追加 | - `plugins/claude-kit/skills/rule-creator/SKILL.jp.md` |
| 済 | ステップ5の処理内容に保守セクションを必ず含める旨を追記 | - `plugins/claude-kit/skills/rule-creator/SKILL.jp.md` |
| 済 | 英語版 SKILL.md に同様の変更を反映 | - `plugins/claude-kit/skills/rule-creator/SKILL.md` |
| 済 | バージョンバンプ・コミット | - `plugins/claude-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/claude-kit/skills/rule-creator/SKILL.jp.md`: 変更対象のスキル定義（日本語ミラー）
- `plugins/claude-kit/skills/rule-creator/SKILL.md`: 変更対象のスキル定義（英語本体）
