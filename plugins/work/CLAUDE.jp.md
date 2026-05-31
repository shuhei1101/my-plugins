# work — プロジェクトライフサイクル管理

Claude Code 向けのフックベースのプロジェクトライフサイクル管理プラグイン。各プロンプト前にブランチコンテキストを注入し、Stop 時にタスク更新をリマインドし、ワークツリー管理と保護ブランチへの強制操作ガードを提供する。

## スキル

| # | スキル | 目的 |
|---|---|---|
| 1 | `work:start` | 新しいブランチと `.work/tasks/` 配下のブランチドキュメントを作成 |
| 2 | `work:pr-handoff` | 現在のブランチ完了後に次のブランチを予約 |
| 3 | `work:pr-show` | 次のブランチ候補を 3 カテゴリ（着手可能 / 進行中 / 条件あり）で表示 |
| 4 | `work:merge` | 現在のブランチをマージし、関連イシューをクローズ、ブランチドキュメントをアーカイブ |
| 5 | `work:qa-wizard` | 未解決の QA 項目を提示してユーザーの判断を収集 |
| 6 | `work:plugin-config` | `settings.json` の work env トグルを対話的に設定 |
| 7 | `work:issue-create` | `.work/issues/` 配下にイシューファイルを作成 |
| 8 | `work:issue-scan` | `work:issue-scanner` サブエージェントを並列起動して観点をスキャンし、発見をイシューとして記録して自動マージ |
| 9 | `work:impl-review` | ブランチドキュメントに照らして実装をレビュー |
| 10 | `work:setup` | テンプレートから `.work/` ディレクトリ構造を初期化 |
| 11 | `work:plugin-migrate` | `.work/` 静的テンプレートを現在の work バージョンに更新 |
| 12 | `work:worktree-create` | ブランチ用の git ワークツリーを作成 |
| 13 | `work:vscode-workspace-sync` | VS Code の `.code-workspace` ファイルを git ワークツリーと同期 |
| 14 | `work:branch-index-cleanup` | `.work/tasks/index.yaml` から古いエントリを削除 |

## エージェント

| # | エージェント | 役割 |
|---|---|---|
| 1 | `work:issue-scanner` | 1 つの観点（フォルダ / grep / レイヤー / ファイル群）を ref-inject の reference と照合してスキャンし、ISSUE ファイルを書き出す。`work:issue-scan` が起動する |

## フック

| # | イベント | トリガー | スクリプト / プロンプト |
|---|---|---|---|
| 1 | `PreToolUse` | Edit / Write / MultiEdit / Read | `hooks/scripts/inject_references.py` — リファレンス自動注入 |
| 2 | `PreToolUse` | Bash | `hooks/prompts/master-commit-guard.md` — 保護ブランチへのコミットをブロック |
| 3 | `PreToolUse` | Bash | `hooks/prompts/git-guard.md` — `git push` / `git merge` を確認 |
| 4 | `UserPromptSubmit` | — | `hooks/prompts/user-prompt-submit.md` — 各プロンプト前にブランチコンテキストを注入 |
| 5 | `Stop` | — | `hooks/prompts/stop.md` — タスク更新リマインド / マージ提案 |

## 環境変数

| # | 変数 | デフォルト | 説明 |
|---|---|---|---|
| 1 | `WORK_USE_WORKTREE` | `true` | 新しいブランチに git ワークツリーを作成 |
| 2 | `WORK_GUARD` | `true` | git-guard フックを有効化（push/merge を確認） |
| 3 | `WORK_PROTECTED_BRANCHES` | `master,main,develop` | master-commit-guard で保護するブランチのカンマ区切りリスト |
| 4 | `WORKSPACE_STOP_REMINDER` | `true` | Stop 時にタスク更新リマインドを表示 |
| 5 | `WORKSPACE_MERGE_PROPOSAL` | `true` | Stop 時に `/work:merge` の実行を提案 |
| 6 | `WORK_BRANCH_AUTHOR` | （空） | ブランチ名に作者名を追加：`{type}/{author}/{title}` 形式になる |
| 7 | `CLAUDE_KIT_INJECTION_DISABLE` | (off) | リファレンス注入を無効化（kill switch） |
| 8 | `DEV_KIT_INJECTION_DISABLE` | (off) | dev-kit リファレンス注入を無効化 |
| 9 | `WORK_COMMIT_LANG` | `JP` | コミットメッセージの言語：`JP` = 日本語、`EN` = 英語 |
| 10 | `WORK_COMMIT_TYPE` | `true` | Conventional commit タイププレフィックス（`feat:`、`fix:`、`chore:` など）を付与するか |
| 11 | `ISSUE_SCAN_AGENTS` | `1` | `issue-scan` 1 回あたりのスキャン観点数（= 並列 `issue-scanner` サブエージェント数） |

## ブランチドキュメント構造

各ブランチは `.work/tasks/{YYMMDD}_{title}/{YYMMDD}-{日本語タイトル}.md` の単一ファイルを使用し、以下のセクションを持つ：

- `## 作業内容` — タスク説明とチェックリスト
- `## QA` — 実装前に解決すべき質問
- `## テスト` — テスト項目
- `## 変更内容` — 実装メモ

ブランチ名はデフォルト `{type}/{title}`（PR 番号プレフィックスなし）。`WORK_BRANCH_AUTHOR` が設定されている場合は `{type}/{author}/{title}` になる。内部 ID は `index.yaml` で管理。

## 変更履歴

| # | バージョン | 日付 | 概要 |
|---|---|---|---|
| 1 | 2.56.0 | 2026-05-31 | `issue-scan` を並列 `work:issue-scanner` サブエージェント（新規エージェント）へ委譲するオーケストレーターに再設計。観点（フォルダ/grep/レイヤー/ファイル群）でスキャン・`ISSUE_SCAN_AGENTS` 追加。`issue-save` スキルを削除し、イシューファイルのフォーマットを `work-dir/イシュー` リファレンスへ集約（`issue-create`・`issue-scanner` が直接記述） |
| 2 | 2.55.0 | 2026-05-31 | `plugins/work/templates/` と `setup-task.py` を削除。テンプレート／フォルダ別構成定義を `references/work-dir/`（`タスクドキュメント` / `タスクインデックス` / `イシュー` / `ワークディレクトリ構成`）へ移し、該当 `.work/` パスの作成・編集時に ref-inject で注入。`work:start` は注入テンプレートを元にブランチドキュメントを直接作成。ブランチドキュメントのファイル名に `.branch.md` 拡張子を付与。`ドットワークディレクトリ構成`→`ワークディレクトリ構成` にリネーム・`TODOテンプレート同期` を削除 |
| 3 | 2.54.0 | 2026-05-31 | index.yaml のブランチ索引を `branch` キー化（id/last_id/tags 撤廃）、`created` サロゲート追加、レガシー分を `index.archive.yaml` へ移行、`next-id` 撤廃・`set-completed` を `--branch` 化 |
| 4 | 2.53.1 | 2026-05-31 | `references/` をカテゴリ別サブフォルダへ分割：`notes/`・`work-dir/`・`skill-sync/` |
| 2 | 2.53.0 | 2026-05-31 | ノートを「現在の仕様書」に再定義（スナップショット。本文に履歴を書かず `## 変更履歴` テーブルのみ・frontmatter 無し）、`ノート記述内容ルール` リファレンス追加、`.work/specs` を notes へ統合しフォルダ削除 |
| 2 | 2.52.0 | 2026-05-31 | ブランチ文書ファイル名を日本語タイトル基準に変更（`{YYMMDD}-{日本語タイトル}.md`）、`index.yaml` に `branch` フィールド追加 |
| 2 | 2.51.0 | 2026-05-31 | `WORK_COMMIT_LANG` / `WORK_COMMIT_TYPE` env var を追加 — コミットメッセージの言語とタイププレフィックスを設定可能に |
| 2 | 2.50.0 | 2026-05-31 | `WORK_BRANCH_AUTHOR` env var を追加 — ブランチ名に作者名セグメントを挿入 |
| 2 | 2.48.0 | 2026-05-30 | `work:notes-to-claude` スキルを削除 — プラグイン間依存を排除 |
| 3 | 2.47.0 | 2026-05-30 | `work:plugin-config` 管理対象トグルに `CLAUDE_KIT_INJECTION_DISABLE` / `DEV_KIT_INJECTION_DISABLE` を追加 |
| 4 | 2.46.2 | 2026-05-30 | `issue-scan` スキルの古い `py-kit`/`next-kit` 記述を削除、`_injection_rules.yaml` に更新 |
| 5 | 2.46.0 | 2026-05-30 | Stop フックのインライン python を `hooks/scripts/stop.py` + `_common.py` に抽出 |
| 6 | 2.44.0 | 2026-05-30 | ブランチドキュメントを単一ファイル（`{branch-hyphenated}.md`）に統合；`plugin-migrate` スキルにリネーム |
| 7 | 2.43.0 | 2026-05-30 | `WORKSPACE_MERGE_PROPOSAL` env トグルを追加 |
| 8 | 2.42.0 | 2026-05-30 | `WORKSPACE_PROTECTED_BRANCHES` env トグルを追加 |
| 9 | 2.41.0 | 2026-05-30 | `impl-review` Step 4 をバッチ AskUserQuestion 方式に変更（最大 4 件/回） |
| 10 | 2.40.0 | 2026-05-30 | `guard-kit` を work プラグインに統合 |
| 11 | 2.39.0 | 2026-05-30 | env トグルを対話的に設定する `work:plugin-config` スキルを追加 |
