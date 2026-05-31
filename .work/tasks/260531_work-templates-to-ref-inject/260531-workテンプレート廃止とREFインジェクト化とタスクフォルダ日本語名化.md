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
| 2 | 済 | `plugins/work/templates/` の全ファイルを確認し、参照元（スクリプト・スキル）を列挙 |
| 3 | 済 | `_injection_rules.yaml` を更新（`templates/**` → `scripts/setup-task.py`）および `_index.yaml`/`.jp.yaml` 説明を更新 |
| 4 | 済 | `setup-task.py` / `setup.py` をテンプレートファイル非依存に改修（インライン定数へ切り替え） |
| 5 | 済 | `plugin-migrate/SKILL.md` のテンプレート参照をハードコード内容記述に更新（SKILL.jp.md 同期） |
| 6 | 済 | `plugins/work/templates/` を削除（git rm） |
| 7 | 済 | バージョン bump（plugin.json/marketplace.json/CLAUDE.md/CLAUDE.jp.md → v2.54.0） |
| 8 | 済 | `.work/notes/` の関連ノートを更新 |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/skills/setup/scripts/setup.py` | 編集 | shutil.copy2 → インライン定数で各ファイルを直接生成 | `_TASKS_GITIGNORE` / `_TASKS_INDEX_YAML` 等の定数を追加 |
| 2 | `plugins/work/scripts/setup-task.py` | 編集 | `_BRANCH_DOC_TEMPLATE` 定数を追加、テンプレートファイル読み込みを削除 | `--plugin-root` は後方互換で残す |
| 3 | `plugins/work/skills/plugin-migrate/SKILL.md` | 編集 | Step 2 のテンプレートディレクトリ参照を削除し、.gitignore 内容をハードコード記述に変更 | 〃 |
| 4 | `plugins/work/skills/plugin-migrate/SKILL.jp.md` | 編集 | SKILL.md の JP ミラーを同期 | - |
| 5 | `plugins/work/references/skill-sync/TODOテンプレート同期.md` | 編集 | 関連ファイルを `templates/note.md` → `scripts/setup-task.py` に変更 | 〃 |
| 6 | `plugins/work/references/skill-sync/TODOテンプレート同期.jp.md` | 編集 | JP ミラーを同期 | - |
| 7 | `plugins/work/references/.ref-injects/_injection_rules.yaml` | 編集 | `templates/**` → `scripts/setup-task.py` にパターン更新 | - |
| 8 | `plugins/work/references/.ref-injects/_index.yaml` | 編集 | TODOテンプレート同期の description を更新 | - |
| 9 | `plugins/work/references/.ref-injects/_index.jp.yaml` | 編集 | JP ミラーを同期 | - |
| 10 | `plugins/work/templates/` | 削除 | ディレクトリ全体を git rm | 8 ファイル削除 |
| 11 | `plugins/work/.claude-plugin/plugin.json` | 編集 | v2.53.1 → v2.54.0 | - |
| 12 | `.claude-plugin/marketplace.json` | 編集 | work エントリを v2.54.0 に更新 | - |
| 13 | `plugins/work/CLAUDE.md` | 編集 | changelog に v2.54.0 行を追加 | 〃 |
| 14 | `plugins/work/CLAUDE.jp.md` | 編集 | JP ミラーを同期 | - |

## テスト

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | `setup.py` が templates/ 参照なしで .work/ 構造を正しく生成する | 全ファイル（tasks/.gitignore, index.yaml 等）が正しく作成されることを確認 | OK |
| 2 | `setup-task.py` がテンプレートファイル不要でブランチドキュメントを生成する | `_BRANCH_DOC_TEMPLATE` から正しいドキュメントが生成されることを確認 | OK |
| 3 | `--plugin-root` 引数を渡しても警告なく動作する（後方互換） | 正常終了を確認 | OK |

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

- `.work/notes/workリファレンスサブフォルダ構造.md`: injection ルール含む work references サブフォルダ構造の現在仕様（injection ルールを本ブランチで更新）

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | refactor/references-subfolder-split | 前ブランチ。work references サブフォルダ分割（v2.53.1） |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | タスクフォルダ日本語名化 | `.work/tasks/` のフォルダ名を kebab-case 英語から日本語に変更。setup-task.py の生成ロジック・スキル・リファレンスを修正 | このブランチ（refactor/work-templates-to-ref-inject）が完了してから |
