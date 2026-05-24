# PR102 — todo-prerequisite-h3-and-related-prs

## 概要

PR101で追加した `## 実施条件` セクションをH3（`### 実施条件`）に変更し、さらに `### 関連プルリクエスト`（PR番号と概要の表）セクションを追加する。

## 実施条件

即時実施可

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | `templates/TODO.md` の `## 実施条件` を `### 実施条件` に変更し `### 関連プルリクエスト` セクションを追加 | - `plugins/work-kit/templates/TODO.md` |
| - | `templates/.work/.../TODO.md` にも同様の変更 | - `plugins/work-kit/templates/.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md` |
| - | `work-start` SKILL.md Step 7 の記入指示を更新 | - `plugins/work-kit/skills/work-start/SKILL.md` |
| - | `work-start` SKILL.jp.md も同期更新 | - `plugins/work-kit/skills/work-start/SKILL.jp.md` |
| - | バージョンバンプ | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- `plugins/work-kit/skills/work-start/SKILL.md`: Step 7がTODO.md記入仕様

## 次PR候補

| タイトル | 概要 | 実施条件 |
|---|---|---|
| {次にやること} | {背景・目的} | {例: 即時実施可 / 「{他候補タイトル}」が完了したら} |
