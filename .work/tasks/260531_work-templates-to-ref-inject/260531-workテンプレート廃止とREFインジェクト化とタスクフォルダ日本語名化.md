# workテンプレート廃止とREFインジェクト化

> ブランチ: `refactor/work-templates-to-ref-inject`

## 概要

`plugins/work/templates/` を廃止し、ブランチドキュメント等のテンプレート／構成定義を **`references/work-dir/` のリファレンス群へ移行**する。ref-inject の Write/Edit フックを使い、`.work/` 配下の各パスを編集・作成するとき該当リファレンス（テンプレート全文を含む）が自動注入される設計にする。スクリプトでテンプレートをコピーするのではなく、Claude が注入されたテンプレートを元にファイルを直接作成するワークフローへ転換する。

### このブランチが必要な理由・前ブランチとの関係

- 前ブランチ `refactor/references-subfolder-split` で work references/ のサブフォルダ分割が完了し、ref-inject 機構がサブフォルダを正しく解決できることを確認済み。
- `plugins/work/templates/` は `setup-task.py` などが参照するタスク文書テンプレートを保管していた。これを廃止し、テンプレートを `references/work-dir/` のリファレンスに移して ref-inject 注入で配信する。
- ref-inject は **Write フックでも発火する**ため、新規ファイル作成時（ブランチドキュメント生成）でもテンプレートが注入される。
- タスクフォルダはユーザーの任意ファイルも格納できる汎用フォルダにするため、ブランチドキュメントは `.branch.md` 拡張子で他ファイルと区別する。
- タスクフォルダ名の日本語化は別ブランチ（次ブランチ候補参照）で実施する。

### 設計方針（当初のインライン化を撤回）

当初 `setup-task.py` に `_BRANCH_DOC_TEMPLATE` 定数としてテンプレートをインライン化したが、これは ref-inject の主旨に反するため撤回する。テンプレートはリファレンス化し、ref-inject 注入で配信する。

| 項目 | 方針 |
|---|---|
| ブランチドキュメントのテンプレート | `references/work-dir/タスクドキュメント.md` に全文を置き、`.work/tasks/**/*.branch.md` 編集時に注入 |
| `.work/` 各サブフォルダの定義 | パス別にリファレンスを細分化（tasks / notes / issues） |
| `setup-task.py` | 廃止。`work:start` で Claude が注入テンプレートを元に直接 Write |
| `setup.py`（`work:setup`） | ブートストラップ（空ディレクトリ + 最小スケルトン生成）専用として残す |
| ブランチドキュメントのファイル名 | `{YYMMDD}-{日本語タイトル}.branch.md` |

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | 未解決事項を `## QA` に記録（QA-001 を B で解決） |
| 2 | 済 | `plugins/work/templates/` の全ファイルを確認し、参照元を列挙 |
| 3 | 済 | `plugins/work/templates/` を削除（git rm） |
| 4 | - | 【撤回】`setup-task.py` への `_BRANCH_DOC_TEMPLATE` インライン化を取り消し、リファレンス化へ転換 |
| 5 | - | `references/work-dir/タスクドキュメント.md`(+jp) を新規作成（ブランチドキュメントテンプレート全文 + 記入ガイド） |
| 6 | - | `references/work-dir/タスクインデックス.md`(+jp) を新規作成（index.yaml / index.archive.yaml スキーマ） |
| 7 | - | `references/work-dir/イシュー.md`(+jp) を新規作成（`.work/issues/` 構成・スキーマ） |
| 8 | - | `ドットワークディレクトリ構成.md`(+jp) → `ワークディレクトリ構成.md`(+jp) にリネーム + スリム化（詳細は各サブフォルダリファレンスへ委譲） |
| 9 | - | `setup-task.py` を廃止（git rm）。`work:start` SKILL.md/.jp.md を「Claude が注入テンプレートを元に直接 Write」へ変更 |
| 10 | - | ブランチドキュメントのファイル名を `{YYMMDD}-{日本語タイトル}.branch.md` に変更（skill・リファレンスの記述更新） |
| 11 | - | `_injection_rules.yaml` をパス別に細分化（tasks doc / tasks index / notes / issues / 全体） |
| 12 | - | `TODOテンプレート同期.md`(+jp) を廃止（`タスクドキュメント.md` に統合） |
| 13 | - | `setup.py` を最小ブートストラップに整理（リッチなスキーマ定義はリファレンスへ移管） |
| 14 | - | `plugin-migrate/SKILL.md`(+jp) のテンプレート参照を更新 |
| 15 | - | `_index.yaml`/`.jp.yaml` のリファレンス一覧を更新 |
| 16 | - | バージョン bump（plugin.json/marketplace.json/CLAUDE.md/CLAUDE.jp.md） |
| 17 | - | 現ブランチドキュメント自身を `.branch.md` 拡張子へリネーム（ドッグフーディング） |
| 18 | - | `.work/notes/` の関連ノートを更新 |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | (実装中に記入) | - | - | - |

## テスト

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | `setup.py` が .work/ 構造を正しくブートストラップする | (未実施) | - |
| 2 | ブランチドキュメント `.branch.md` 編集時に `タスクドキュメント.md` が注入される | (未実施) | - |
| 3 | `.work/issues/**` 編集時に `イシュー.md` が注入される | (未実施) | - |

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
