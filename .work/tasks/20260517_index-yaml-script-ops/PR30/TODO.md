# PR30 — index-yaml-script-ops

## 概要

`index.yaml` の読み書きを Python スクリプトに委譲することで、Claude Code が
ファイル全文をコンテキストに読み込むコストを削減する。

work-start・merge スキルのステップから `index.yaml` の直接 Read を排除し、
代わりに `index-tool.py` スクリプトを呼び出す形に変更する。

## 作業内容

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| 済 | index-tool.py を新規作成（next-id / add / list-active サブコマンド） | - `plugins/work-kit/scripts/index-tool.py` |
| 済 | work-start ステップ1を index-tool.py next-id 呼び出しに変更 | - `plugins/work-kit/skills/work-start/SKILL.md`<br>- `plugins/work-kit/skills/work-start/SKILL.jp.md` |
| 済 | work-start ステップ3を index-tool.py add 呼び出しに変更 | - `plugins/work-kit/skills/work-start/SKILL.md`<br>- `plugins/work-kit/skills/work-start/SKILL.jp.md` |
| 済 | merge ステップ1を index-tool.py list-active 呼び出しに変更 | - `plugins/work-kit/skills/merge/SKILL.md`<br>- `plugins/work-kit/skills/merge/SKILL.jp.md` |
| 済 | trim-index.py バグ修正（em dash → ハイフン・ID ソート追加） | - `plugins/work-kit/scripts/trim-index.py` |
| 済 | plugin.json と marketplace.json のバージョンを bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし
