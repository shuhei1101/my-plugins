# work リファレンス インデックス

`references/` 配下のリファレンスドキュメント一覧。

---

## ワークディレクトリ（`.work/` 配下の構成・テンプレート）

`.work/` 配下のファイルを作成・編集するときに、該当パスのリファレンスが ref-inject で自動注入される。

| # | ファイル | 注入パターン | 内容 |
|---|---|---|---|
| 1 | [work-dir/ワークディレクトリ構成.md](work-dir/ワークディレクトリ構成.md) | `.work/**` | `.work/` の俯瞰図・各サブフォルダの役割・コミット規約。詳細は各サブフォルダリファレンスへ |
| 2 | [work-dir/タスクドキュメント.md](work-dir/タスクドキュメント.md) | `.work/tasks/**/*.branch.md` | ブランチドキュメントのテンプレート全文 + 記入ガイド |
| 3 | [work-dir/タスクインデックス.md](work-dir/タスクインデックス.md) | `.work/tasks/index*.yaml` | `index.yaml` / `index.archive.yaml` スキーマ |
| 4 | [work-dir/イシュー.md](work-dir/イシュー.md) | `.work/issues/**` | `ISSUE-{N}.md` 構成 + `_index.yaml` / `_index.archive.yaml` スキーマ |
| 5 | [notes/ノート命名規則.md](notes/ノート命名規則.md) | `.work/notes/**` | `.work/notes/` ファイルの命名・`_index.md` 管理規則 |
| 6 | [notes/ノート記述内容ルール.md](notes/ノート記述内容ルール.md) | `.work/notes/**` | ノートに書く内容と固定テンプレート。現在状態のみ・履歴は変更履歴テーブルのみ |

---

## スキル同期ルール

スキル間の整合性を保つための同期ルール。

| # | ファイル | 内容 |
|---|---|---|
| 1 | [skill-sync/ストッププロンプト同期.md](skill-sync/ストッププロンプト同期.md) | `stop.md` と `stop-no-merge.md` の同期ルール。2 ファイルは対称な組・ステップ 1〜3 を常に一致させる |
| 2 | [skill-sync/マージスキル同期.md](skill-sync/マージスキル同期.md) | `merge` SKILL.md とマージフローノートの同期ルール。ステップを追加・削除したらノートも更新 |
| 3 | [skill-sync/スタートスキル同期.md](skill-sync/スタートスキル同期.md) | `work-start`・`worktree-create`・`vscode-workspace-sync` スキルの同期ルール。Step 4 の委譲インターフェース整合 |
