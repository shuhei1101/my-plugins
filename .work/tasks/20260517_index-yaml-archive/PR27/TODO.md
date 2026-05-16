# PR27 — index-yaml-archive

## 概要

`index.yaml` が PR を重ねるごとに肥大化する問題を解消する。
`last_id` フィールドで次の PR 番号を管理し、完了済みエントリを `index.archive.yaml` に移す
trim スクリプトを追加することで、`index.yaml` を常にアクティブな PR のみの小さいファイルに保つ。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | index.yaml に last_id フィールドを追加し、completed: true エントリを archive に移動 | - `.work/tasks/index.yaml`（ローカルのみ） |
| - | trim スクリプトを作成（completed: true を index.archive.yaml へ移動） | - `plugins/work-kit/scripts/trim-index.py` |
| - | index.archive.yaml を .gitignore に追加 | - `plugins/work-kit/templates/.work/tasks/.gitignore` |
| - | work-start ステップ1を last_id 参照に更新 | - `plugins/work-kit/skills/work-start/SKILL.md`<br>- `plugins/work-kit/skills/work-start/SKILL.jp.md` |
| - | plugin.json と marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし
