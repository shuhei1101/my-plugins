# PR27 — index-yaml-archive

## 概要

`index.yaml` が PR を重ねるごとに肥大化する問題を解消する。
`last_id` フィールドで次の PR 番号を管理し、完了済みエントリを `index.archive.yaml` に移す
trim スクリプトを追加することで、`index.yaml` を常にアクティブな PR のみの小さいファイルに保つ。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | index.yaml に last_id フィールドを追加し、completed: true エントリを archive に移動 | - `.work/tasks/index.yaml`（ローカルのみ） |
| 済 | trim スクリプトを作成（completed: true を index.archive.yaml へ移動） | - `plugins/work-kit/scripts/trim-index.py` |
| 済 | index.archive.yaml を .gitignore に追加 | - `plugins/work-kit/templates/.work/tasks/.gitignore` |
| 済 | work-start ステップ1を last_id 参照に更新 | - `plugins/work-kit/skills/work-start/SKILL.md`<br>- `plugins/work-kit/skills/work-start/SKILL.jp.md` |
| 済 | plugin.json と marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |
| 済 | update スキルに index.yaml last_id マイグレーションステップを追加 | - `plugins/work-kit/skills/update/SKILL.md`<br>- `plugins/work-kit/skills/update/SKILL.jp.md` |
| 済 | trim-index.py を py:py 規約に従って書き直す | - `plugins/work-kit/scripts/trim-index.py` |
| - | merge スキルに trim 自動実行ステップを追加（案B） | - `plugins/work-kit/skills/merge/SKILL.md`<br>- `plugins/work-kit/skills/merge/SKILL.jp.md` |
| - | CLAUDE.md/jp.md に index.archive.yaml の説明を追記 | - `plugins/work-kit/templates/.work/CLAUDE.md`<br>- `plugins/work-kit/templates/.work/CLAUDE.jp.md` |
| - | プロジェクトの .work/tasks/.gitignore に index.archive.yaml を追記（既存プロジェクト対応） | - `.work/tasks/.gitignore` |

## 参考ドキュメント

- なし
