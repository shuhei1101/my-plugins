# PR51 — summarize-official-plugins

## 概要

公式マーケットプレイス `claude-plugins-official` (実体は **anthropics/claude-plugins-official** リポジトリ、計 170+ プラグイン) に含まれる各プラグインを調査し、概要・機能を解説した日本語 markdown を `tmp/claude-plugins-official解説.md` に作成する。

> **修正履歴**: 当初 `anthropics/claude-code` の `plugins/` 直下 13 個を対象としていたが誤り。正しくは `anthropics/claude-plugins-official` (別リポジトリ) で総数 170+。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する (未決定事項なし) | - `.work/tasks/20260518_summarize-official-plugins/PR51/QA.md` |
| 済 | (誤) anthropics/claude-code の 13 プラグイン解説 | - 初版 |
| 済 | (修正) anthropics/claude-plugins-official の正しい marketplace.json を取得 | - WebFetch |
| 済 | 170+ プラグインをカテゴリ別に整理 | - WebFetch |
| 済 | 解説 markdown を全面書き直し | - `tmp/claude-plugins-official解説.md` |
| 済 | ルール・CLAUDE.md の整備 (今回は対象外につき不要) | - - |

## 参考ドキュメント

- https://github.com/anthropics/claude-plugins-official — 真の公式マーケットプレイス
- https://github.com/anthropics/claude-code — Claude Code 本体 (別物)

## QA

なし
