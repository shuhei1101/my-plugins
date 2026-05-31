# PR19 — add-gitignore-to-template

## 概要

`/work-kit:setup` および `/work-kit:update` 実行時に `.work/tasks/.gitignore` が生成されるよう修正する。
テンプレートに `.gitignore` を追加し、update スキルで同期されるようにする。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | テンプレートに `.gitignore` を追加（`index.yaml` を除外） | - `plugins/work-kit/templates/.work/tasks/.gitignore` |
| 済 | update スキルに `.gitignore` 同期ステップを追記 | - `plugins/work-kit/skills/update/SKILL.jp.md`<br>- `plugins/work-kit/skills/update/SKILL.md` |
| 済 | work-kit バージョンを 2.6.5 → 2.6.6 に bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし

## QA

なし
