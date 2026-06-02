# setup.py index.yaml テンプレート廃止フィールド除去

## 概要

`setup.py` の `_TASKS_INDEX_YAML` / `_TASKS_INDEX_ARCHIVE_YAML` テンプレート定数が v2.54.0 のスキーマ変更に追従していなかった問題を修正した。

## 問題

v2.54.0（2026-05-31）でブランチインデックスのスキーマが変更された（`id` / `last_id` / `tags` を廃止し、`branch` / `created` をキーに変更）が、`setup.py` のテンプレート定数は更新されなかった。

結果として `work:setup` 実行時に生成される `index.yaml` に廃止済みの `last_id: 0` フィールドが含まれていた。

## 修正内容

`plugins/work/skills/setup/scripts/setup.py`:

- `_TASKS_INDEX_YAML`:
  - `last_id: 0` を除去（トップレベルキー）
  - コメントから `id: 連番（アーカイブ参照用）` と `tags: 自由形式タグ（省略可）` を除去
  - コメントに `created: 作成日（YYYY-MM-DD）` を追加
  - `title` の説明を `タスクドキュメントの H1 タイトル` から `ブランチ文書の H1 タイトル` に修正

- `_TASKS_INDEX_ARCHIVE_YAML`:
  - ヘッダーコメントを `index-tool.py archive` が実際に移動するエントリの説明に更新
  - `id`, `tags`, `archived`, `resolution` の廃止フィールドコメントを除去
  - `created`, `completed` の現行フィールドコメントを追加

## 教訓

スキーマ変更時はセットアップスクリプトのテンプレート定数も同時に更新する必要がある。`index-tool.py` / 参照ドキュメント / `setup.py` の 3 箇所を横断的にチェックすること。

## 変更履歴

| 日付 | 変更 |
|---|---|
| 2026-06-02 | 初版作成（ISSUE-097 対応） |
