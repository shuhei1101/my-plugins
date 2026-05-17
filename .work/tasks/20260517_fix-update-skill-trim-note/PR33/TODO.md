# PR33 — fix-update-skill-trim-note

## 概要

update スキルのステップ4注記から「手動で trim-index.py を実行してください」という
案内を削除する。merge が自動実行するため不要になった（work-start と同様の修正）。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | update ステップ4の注記から手動 trim 案内を削除 | - `plugins/work-kit/skills/update/SKILL.md`<br>- `plugins/work-kit/skills/update/SKILL.jp.md` |
| - | plugin.json と marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし
