# work リファレンス インデックス

`references/` 配下のリファレンスドキュメント一覧。

---

## ディレクトリ構造・コミット規約

| # | ファイル | 内容 |
|---|---|---|
| 1 | [work-dot-work-dir.md](work-dot-work-dir.md) | `.work/` 配下のファイルを編集する際のガイド。ディレクトリ構成・ブランチドキュメントのセクション構成・notes のライフサイクル・コミット規約（`.work/` は実装コードと別コミットにすること） |
| 2 | [notes-naming-rules.md](notes-naming-rules.md) | `.work/notes/` ファイルの命名・インデックス規則。ファイル名と H1 タイトルは日本語（技術識別子は原形維持）・ノート作成/リネーム/削除時は同コミットで `_index.md` を更新 |

---

## スキル同期ルール

スキル間の整合性を保つための同期ルール。

| # | ファイル | 内容 |
|---|---|---|
| 1 | [work-stop-prompt-sync.md](work-stop-prompt-sync.md) | `stop.md` と `stop-no-merge.md` の同期ルール。2 ファイルは対称な組・ステップ 1〜3 を常に一致させる |
| 2 | [work-merge-skill-sync.md](work-merge-skill-sync.md) | `merge` SKILL.md とマージフロー仕様書の同期ルール。ステップを追加・削除したら仕様書も更新 |
| 3 | [work-start-skill-sync.md](work-start-skill-sync.md) | `work-start`・`worktree-create`・`vscode-workspace-sync` スキルの同期ルール。Step 4 の委譲インターフェース整合 |
| 4 | [work-todo-template-sync.md](work-todo-template-sync.md) | TODO テンプレートと `work-start` SKILL.md の同期ルール。テンプレートのセクション構成は Step 7 の記入ガイドと一致させる |
