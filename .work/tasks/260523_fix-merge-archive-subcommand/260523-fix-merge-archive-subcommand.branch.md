# PR80 — fix-merge-archive-subcommand

## 概要

merge スキルが `index-tool.py archive` を呼んでいるが、そのサブコマンドが存在しないためエラーが発生する。`archive` サブコマンドを index-tool.py に追加して修正する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する | - `.work/tasks/.../PR80/QA.md` |
| 済 | `index-tool.py` に `archive` サブコマンドを追加する | - `plugins/work-kit/scripts/index-tool.py` |
| 済 | SKILL.md の `archive` コマンド記述を確認・修正する | - `plugins/work-kit/skills/merge/SKILL.md` |
| 済 | バージョンバンプ | - `plugins/work-kit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし

## 次PR候補

| タイトル | 概要 |
|---|---|
| {次にやること} | {背景・目的} |

## QA

なし
