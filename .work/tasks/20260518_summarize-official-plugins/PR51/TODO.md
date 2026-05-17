# PR51 — summarize-official-plugins

## 概要

anthropics/claude-code リポジトリの公式プラグインマーケットプレイス (claude-plugins-official) に含まれる各プラグインを調査し、それぞれの概要・機能を解説した日本語 markdown を `tmp/claude-plugins-official解説.md` に作成する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | QA.md に未決定事項を記録する (未決定事項なし) | - `.work/tasks/20260518_summarize-official-plugins/PR51/QA.md` |
| 済 | claude-plugins-official のマーケットプレイス定義 (marketplace.json) を取得 | - WebFetch |
| 済 | 各プラグインの README / plugin.json を確認し機能を整理 | - WebFetch |
| 済 | 解説 markdown を作成 | - `tmp/claude-plugins-official解説.md` |
| 済 | ルール・CLAUDE.md の整備 (今回は対象外につき不要) | - - |

## 参考ドキュメント

- https://github.com/anthropics/claude-code — 公式リポジトリ
