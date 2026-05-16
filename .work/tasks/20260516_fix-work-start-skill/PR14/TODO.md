# PR14 — fix-work-start-skill

## 概要

work-start スキルの挙動を修正する。
ステップ2の「ユーザーへの確認」文言を削除し、ステップ8にコミット→報告の順序を追加、禁止事項にワークツリー外コミット禁止を追加する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | ステップ2の「ユーザーから以下を確認する」文言を削除 | - `plugins/work-kit/skills/work-start/SKILL.jp.md`<br>- `plugins/work-kit/skills/work-start/SKILL.md` |
| 済 | ステップ8をコミット→報告の順序に変更（コミット前の報告を禁止） | - `plugins/work-kit/skills/work-start/SKILL.jp.md`<br>- `plugins/work-kit/skills/work-start/SKILL.md` |
| 済 | 禁止事項に「作成したワークツリー以外へのコミット禁止」を追加 | - `plugins/work-kit/skills/work-start/SKILL.jp.md`<br>- `plugins/work-kit/skills/work-start/SKILL.md` |
| 済 | plugin.json と marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし
