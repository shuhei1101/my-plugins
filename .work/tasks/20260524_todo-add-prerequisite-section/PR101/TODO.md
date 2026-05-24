# PR101 — todo-add-prerequisite-section

## 概要

TODO.mdテンプレートに `## 実施条件` セクションを追加する。概要と作業内容の間に置き、このPR自体の実施条件（即時実施可 / 他PRへの依存）を記録できるようにする。次PR候補テーブルの「実施条件」カラムと同じ概念。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | `templates/TODO.md` に `## 実施条件` セクションを追加（概要と作業内容の間） | - `plugins/work-kit/templates/TODO.md` |
| 済 | `templates/.work/.../TODO.md` に同じセクションを追加 | - `plugins/work-kit/templates/.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md` |
| 済 | `work-start` SKILL.md Step 7 の説明を更新（実施条件の記入指示を追加） | - `plugins/work-kit/skills/work-start/SKILL.md` |
| 済 | `work-start` SKILL.jp.md も同期更新 | - `plugins/work-kit/skills/work-start/SKILL.jp.md` |
| 済 | バージョンバンプ | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/skills/work-start/SKILL.md`: work-startスキル（Step 7がTODO.md記入仕様）

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {次にやること} | {背景・目的} | {例: 即時実施可 / 「{他候補タイトル}」が完了したら} |
