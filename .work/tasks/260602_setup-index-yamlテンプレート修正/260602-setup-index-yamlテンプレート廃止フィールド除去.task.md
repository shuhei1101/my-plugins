# setup-index-yamlテンプレート廃止フィールド除去

> ブランチ: `fix/setup-index-yaml-template`

## 概要

`plugins/work/skills/setup/scripts/setup.py` の `_TASKS_INDEX_YAML` / `_TASKS_INDEX_ARCHIVE_YAML` テンプレート定数に、v2.54.0 で廃止された `last_id`, `id`, `tags` フィールドがコメント・実値として残っている。`work:setup` 実行時に現行スキーマと乖離した `index.yaml` が生成されてしまう問題を修正する。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | 未解決事項を `## QA` に記録する（なし — 方針確定済み） |
| 2 | 済 | `_TASKS_INDEX_YAML`: `last_id: 0` を除去し、コメントを現行スキーマ（branch/created/title/type/summary/task/completed）に更新 |
| 3 | 済 | `_TASKS_INDEX_ARCHIVE_YAML`: コメントを `cmd_archive` が実際に出力するフィールドに合わせて更新（`id`, `tags`, 旧 `resolution` 表記を除去） |
| 4 | 済 | 構文検証・YAML パース検証 |
| 5 | 済 | `.work/notes/` の関連ノートを更新する |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/skills/setup/scripts/setup.py` | 編集 | `_TASKS_INDEX_YAML` と `_TASKS_INDEX_ARCHIVE_YAML` のテンプレート定数を現行スキーマに更新 | `index-tool.py` の実装ロジックは変更しない |

## テスト

| # | 確認内容 | 実測結果 | 判定 |
|---|---|---|---|
| 1 | `setup.py` が構文エラーなくパースできる | `ast.parse()` で構文 OK | OK |
| 2 | `_TASKS_INDEX_YAML` 定数が有効な YAML としてパースできる | `yaml.safe_load()` で `{'branches': []}` | OK |
| 3 | `_TASKS_INDEX_ARCHIVE_YAML` 定数が有効な YAML としてパースできる | `yaml.safe_load()` で `{'branches': []}` | OK |
| 4 | 生成された `index.yaml` に `last_id` フィールドが含まれない | テンプレート定数から `last_id: 0` を除去済み | OK |

## QA

未解決事項なし。

## 参考ドキュメント

- `.work/notes/バグ・不具合/setup-index-yaml-template-stale-fields.md`: setup.py テンプレート廃止フィールド除去の経緯と修正内容

## 関連イシュー

| # | ID | 概要 | resolution |
|---|---|---|---|
| 1 | ISSUE-097 | `setup.py` が生成する `index.yaml` テンプレートに廃止済みの `last_id` フィールドが残っている | resolved |

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | - | - |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | - | - | - |
