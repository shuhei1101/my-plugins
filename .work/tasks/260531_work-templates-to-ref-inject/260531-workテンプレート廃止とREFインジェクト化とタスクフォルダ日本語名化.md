# workテンプレート廃止とREFインジェクト化

> ブランチ: `refactor/work-templates-to-ref-inject`

## 概要

`plugins/work/templates/` を廃止し、タスク文書生成・スキル・スクリプトをテンプレートファイル参照からREF-inject 参照へ移行する。

### このブランチが必要な理由・前ブランチとの関係

- 前ブランチ `refactor/references-subfolder-split` で work references/ のサブフォルダ分割が完了し、REF-inject 機構がサブフォルダを正しく解決できることを確認済み。
- `plugins/work/templates/` は現状 `setup-task.py` などのスクリプトが参照するタスク文書テンプレートを保管している。これを廃止して REF-inject 参照へ移行することで、templates/ を削除できる。
- タスクフォルダ名の日本語化は別ブランチ（次ブランチ候補参照）で実施する。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | 未解決事項を `## QA` に記録（QA-001 を B で解決） |
| 2 | - | `plugins/work/templates/` の全ファイルを確認し、参照元（スクリプト・スキル）を列挙 |
| 3 | - | `.work/` 各フォルダの構成定義リファレンスを `references/work-dir/` に追加し `_injection_rules.yaml` を更新 |
| 4 | - | `setup-task.py` / `setup.py` をテンプレートファイル非依存に改修（REF-inject 参照へ切り替え） |
| 5 | - | `plugins/work/skills/start/SKILL.md` などスキル側のテンプレート参照を REF-inject 参照へ更新 |
| 6 | - | `plugins/work/templates/` を削除 |
| 7 | - | バージョン bump（plugin.json/marketplace.json/CLAUDE.md changelog 同期） |
| 8 | - | `.work/notes/` の関連ノートを更新 |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | (着手時に記入) | - | - | - |

## テスト

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | タスク文書が templates/ 参照なしで正しく生成される | (未実施) | - |

## QA

### QA-001: スコープ分割の是非

**背景**: 「templates廃止 + REF-inject化」と「タスクフォルダ日本語名化」は独立した変更であり、一つのブランチにまとめると規模が大きい可能性がある。

| # | 案 | 内容 |
|---|---|---|
| 1 | A | 1ブランチにまとめて実施（前ブランチの次候補として提案された単位を尊重） |
| 2 | B | templates廃止+REF-inject化 と タスクフォルダ日本語名化を別ブランチに分割 |

**推奨方式**: A — 前ブランチの次候補として提案された単位なので一括実施。進める中でスコープが大きすぎる場合は分割を判断する

**決定**: B — タスクフォルダ日本語名化は別ブランチに分割。このブランチは templates廃止+REF-inject化のみ実施。

**状態**: 解決済み

**反映先**: ## 作業内容（項目7削除）、## 次ブランチ候補（日本語名化を追加）

## 参考ドキュメント

- `.work/notes/workリファレンスサブフォルダ構造.md`: work references サブフォルダ構造の現在仕様

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | refactor/references-subfolder-split | 前ブランチ。work references サブフォルダ分割（v2.53.1） |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | タスクフォルダ日本語名化 | `.work/tasks/` のフォルダ名を kebab-case 英語から日本語に変更。setup-task.py の生成ロジック・スキル・リファレンスを修正 | このブランチ（refactor/work-templates-to-ref-inject）が完了してから |
