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

| 済 | index.archive.yaml を .gitignore から削除（テンプレート・プロジェクト両方） | - `plugins/work-kit/templates/.work/tasks/.gitignore`<br>- `.work/tasks/.gitignore` |
| 済 | index-tool.py に completed-count サブコマンドを追加 | - `plugins/work-kit/scripts/index-tool.py` |
| 済 | work-kit:archive スキルを新規作成（任意タイミングで実行可能） | - `plugins/work-kit/skills/archive/SKILL.md`<br>- `plugins/work-kit/skills/archive/SKILL.jp.md` |
| 済 | merge ステップ6を更新（count≥100 かつ .work/ 追跡時のみ archive フロー起動） | - `plugins/work-kit/skills/merge/SKILL.md`<br>- `plugins/work-kit/skills/merge/SKILL.jp.md` |
| 済 | バージョンを 2.8.0 → 2.9.0 に bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

| - | work-kit:archive スキルを削除（merge フロー内に統合するため不要） | - `plugins/work-kit/skills/archive/SKILL.md`<br>- `plugins/work-kit/skills/archive/SKILL.jp.md` |
| - | merge スキルを修正：ステップ2と3の間に archive ステップを追加、閾値・completed-count チェックを削除、ステップ番号を整理 | - `plugins/work-kit/skills/merge/SKILL.md`<br>- `plugins/work-kit/skills/merge/SKILL.jp.md` |
| - | バージョンを 2.9.0 → 2.10.0 に bump | - `plugins/work-kit/.claude-plugin/plugin.json`<br>- `.claude-plugin/marketplace.json` |

## 参考ドキュメント

- なし
