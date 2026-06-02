# ISSUE-097: `setup.py` が生成する `index.yaml` テンプレートに廃止済みの `last_id` フィールドが残っている

**作成日**: 2026-05-31

## 概要

`work:setup` が生成する `index.yaml` テンプレート（`setup.py` 内の定数）に、v2.54.0 で廃止された `last_id` などのフィールドが残っており、新規プロジェクトで現行スキーマと乖離した `index.yaml` が生成される。

## 背景

work プラグイン v2.54.0（2026-05-31）の変更履歴:

> index.yaml branch index keyed by `branch` (drop id/last_id/tags); add `created` surrogate; legacy backlog migrated to `index.archive.yaml`; `next-id` removed and `set-completed` switched to `--branch`

スキーマ変更時に、セットアップスクリプトのテンプレート文字列の更新が漏れた。

## 現状

`plugins/work/skills/setup/scripts/setup.py` の `_TASKS_INDEX_YAML` 定数:

```python
_TASKS_INDEX_YAML = """\
# .work/tasks/index.yaml — ブランチ索引
...
last_id: 0
branches: []
"""
```

`last_id` フィールドは v2.54.0 でスキーマから削除されたが、`setup.py` のテンプレート文字列は更新されていない。また、コメント内の `id: 連番（アーカイブ参照用）` と `tags: 自由形式タグ（省略可）` も廃止済みフィールドとして残っている。

加えて、`_TASKS_INDEX_ARCHIVE_YAML` コメントにも廃止フィールド（`id: 連番`, `tags: 自由形式タグ`, `resolution: merged / abandoned`）が記載されており、実際の `index-tool.py` が出力するアーカイブエントリ（`branch`, `created`, `title`, `type`, `summary`, `task`, `archived`, `resolution`）と一致しない部分がある。

## 期待される状態

`setup.py` のテンプレート定数（`_TASKS_INDEX_YAML` / `_TASKS_INDEX_ARCHIVE_YAML`）が現行スキーマと一致し、`work:setup` 実行時に廃止フィールドを含まない `index.yaml` が生成される。

## 対応案

`_TASKS_INDEX_YAML` テンプレートを現行スキーマに合わせて更新する:

```python
_TASKS_INDEX_YAML = """\
# .work/tasks/index.yaml — ブランチ索引
#
# フィールド説明:
#   branch    : git ブランチ名（例: feat/my-feature）
#   created   : 作成日（YYYY-MM-DD）
#   title     : ブランチ文書の H1 タイトルそのまま
#   type      : feat / fix / docs / refactor / chore / test
#   summary   : ファイルを開かずに内容がわかる一行説明
#   task      : タスクフォルダ名（YYMMDD_{title}）
#   completed : false = 進行中、true = マージ済み / 廃止済み

branches: []
"""
```

`_TASKS_INDEX_ARCHIVE_YAML` のコメントも `index-tool.py cmd_archive` が出力する実際のフィールド（`branch`, `created`, `title`, `type`, `summary`, `task`, `archived`, `resolution`）に合わせて更新する。

## 横展開

スキーマ変更時はセットアップスクリプト・テンプレート文字列・`index-tool.py` の 3 箇所を同時に更新する必要がある。変更履歴にスキーマ変更を記録する際は、影響するすべての静的テンプレートのリストを明示することを推奨する。

---

# ユーザー回答欄

> 回答方法: 各 `**回答**:` 行で不要な選択肢を消し、1 つだけ残す（`{回答を入力}` は自由記入）。
> AI は選択肢・推奨と、候補を並べた `**回答**:` 行まで用意する。

## 意思

このイシューに対応するか。

**回答**: 対応する / 対応しない
