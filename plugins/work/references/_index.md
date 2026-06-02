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

---

## 会話キャプチャ（glossary / incidents 記述基準）

`conversation-to-claude` が生成する用語集・再発防止ログを編集するときに自動注入される、採用基準とファイル形式。

| # | ファイル | 注入パターン | 内容 |
|---|---|---|---|
| 1 | [conversation/グロッサリー.md](conversation/グロッサリー.md) | `.claude/rules/glossary.md` | 用語集の採用基準（プロジェクト固有・非自明・繰り返す・既出でない）とファイル形式 |
| 2 | [conversation/インシデント.md](conversation/インシデント.md) | `.claude/rules/incidents.md`・`.claude/references/incidents/**` | 再発防止ログの採用基準（実際のミス・一般化可能・既存ルールで未強制）と二層構造の形式 |
