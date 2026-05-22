# PR74 — branch-index-cleanup

## 概要

未登録ブランチを精査して index.yaml / index.archive.yaml に整理するワークフロースキル `branch-index-cleanup` を新規作成する。
`pr-pick` が一覧表示までしか行わないのに対し、本スキルは A/B/C 分類 → 削除判断 → archive 登録 → index 反映までの整理実行を担う。
aituber PR360 で手動実施したワークフローを切り出したもの。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | `.work/tasks/20260522_branch-index-cleanup/PR74/QA.md` |
| 済 | `.work/specs/` の仕様書を作成する | `.work/specs/branch-index-cleanup.md` |
| 済 | `branch-index-cleanup` スキルを新規作成する | `plugins/work-kit/skills/branch-index-cleanup/SKILL.md` |
| 済 | `branch-index-cleanup` の JP 翻訳を作成する | `plugins/work-kit/skills/branch-index-cleanup/SKILL.jp.md` |
| 済 | `plugin.json` のバージョンを更新する | `plugins/work-kit/.claude-plugin/plugin.json` |
| 済 | `marketplace.json` のバージョンを更新する | `.claude-plugin/marketplace.json` |
| 済 | CLAUDE.md のスキル一覧を更新する | `plugins/work-kit/CLAUDE.md`（存在しないためスキップ） |

## 参考ドキュメント

- `.work/specs/branch-index-cleanup.md`: branch-index-cleanup スキル仕様

## 次PR候補

| タイトル | 概要 |
|---|---|
| PR75 — branch-index-sync ルール追加 | ブランチ操作時に index 同期を強制するルール |
