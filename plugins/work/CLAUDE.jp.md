<!-- This file is a Japanese mirror of CLAUDE.md. When updating the English original, update this file too. -->
# work — プロジェクトライフサイクル管理

Claude Code 向けのフックベースのプロジェクトライフサイクル管理プラグイン。各プロンプト前にブランチコンテキストを注入し、Stop 時にタスク更新をリマインドし、ワークツリー管理と保護ブランチへの強制操作ガードを提供する。

## ライフサイクル

work プラグインは「1 タスク = 1 ブランチ」のライフサイクルをフックで強制する。一連の流れは以下のとおり。

1. **プロンプト受信 → ブランチゲート**（`UserPromptSubmit` フック / `hooks/prompts/user-prompt-submit.md`）
   このセッションでブランチが進行中かを判定する。
   - **進行中でない** → 何かを編集・コミットする前に必ず `work:start` を実行する（ブランチ無しでの編集・コミット、master への直接コミットは禁止）。
   - **進行中** → そのブランチのワークツリーへ移動しタスクドキュメントを読む。`## QA` に未解決項目があれば**そこで停止**しユーザーに解決を促す。クリアなら今回の依頼を `## 作業内容` に追記してから作業を続ける。

2. **ブランチ作成**（`work:start` → `work:worktree-create`）
   ブランチ名決定（`{type}/{title}`、`${WORK_BRANCH_AUTHOR}` 設定時は作者セグメント挿入）→ 詳細収集（日本語タイトル・TODO・ノート・未決定事項）→ メインリポジトリの `index.yaml` にエントリ追加 → ワークツリーとブランチ作成 → タスクフォルダ選択／作成 → 注入テンプレートからタスクドキュメントを作成 → 未決定事項を `## QA` に記録 → **初回コミット（タスクドキュメントのみ）**。

3. **実装**（ワークツリー内）
   編集とコミットはブランチ上で行う。`PreToolUse(Bash)` の 2 つのガードがリポジトリを保護する：`master-commit-guard` は保護ブランチ（`master` / `main` / `develop`）への `git commit` をブロックし、`git-guard` は `git push` / 上流以外への `git merge` を確認する。

4. **最終コミット**（`work:start` Step 9）
   `.work/notes/` の関連ノートを更新／新規作成し、`## 参考ドキュメント` からリンクし、`_index.md` を更新して、ノート + タスクドキュメントをまとめて最後のコミットにする。

5. **レスポンス終了 → Stop リマインダー**（`Stop` フック / `hooks/prompts/stop.md`）
   完了した `## 作業内容` 行を `済` にし、`## QA` がクリアでノートが反映済みかを確認したうえで、**`/work:merge` の実行を提案**する（`${WORK_MERGE_PROPOSAL}` が falsy のときは提案を省略し `stop-no-merge.md` を使用）。

6. **マージ**（`work:merge`）
   TODO チェックリスト検証 → 親ブランチを取り込み → **関連イシューをクローズ**（`## 関連イシュー` の各行を `issue-tool.py close` で `.work/issues/closed/` へ移動し `_index.archive.yaml` に記録）→ `index.yaml` でブランチを完了化 → タスクドキュメントをアーカイブ → `--no-ff` で親ブランチへマージ → ワークツリー削除 → 残 QA 確認 → 次ブランチ候補があれば `branch-reserve` を自動起動。

**イシューのサブサイクル**: イシューは `.work/issues/ISSUE-{N}.md` に存在し、**フロントマターを持たない**
2 分割の Markdown ファイル — `# ユーザー回答欄`（`## 意思` / `## QA`）を**上部**に置き（回答済みか
一目で分かるように）、その下に AI 記入のイシュー本文。各 QA は番号・タイトル・選択肢・AI 推奨を持つ。
作業状態（`status` / `branches`）は `_index.yaml` のみが持つ。流れ：
**作成**（`issue-create` / `issue-scan` → 本文と回答欄の雛形を記入、各 `**回答**:` に全候補を事前記入、QA 提起）→
**レビュー**（`issue-review`、スマホ主用途 → ユーザーが `## 意思`（対応する/対応しない）と各 `## QA` の
`**回答**:` を 1 つに絞る）→
**対応**（`issue-resolve`、`/loop` で 1 起動 1 イシュー → 意思=肯定は `issue-resolver` サブエージェントを
委譲し `work:start`→マージ待ちコミットで停止、意思=否定は共有 `chore/rejected-issues` ブランチでクローズ）→
**クローズ**（`merge` がブランチの `## 関連イシュー` を `resolved` でクローズ; reject ブランチは
`wontfix` でクローズ）。QA はレビュー時にイシュー上で決着するため、resolver サブエージェントは
質問で止まらず最終コミットまで到達できる。

## スキル

| # | スキル | 目的 |
|---|---|---|
| 1 | `work:start` | 新しいブランチと `.work/tasks/` 配下のタスクドキュメントを作成 |
| 2 | `work:branch-reserve` | `work:start` と同じフローで、現在のブランチ完了後に次のブランチを予約 |
| 3 | `work:branch-show` | 次のブランチ候補を 3 カテゴリ（着手可能 / 他で進行中 / 条件あり）で表示 |
| 4 | `work:merge` | 現在のブランチをマージし、関連イシューをクローズ、タスクドキュメントをアーカイブ |
| 5 | `work:qa-wizard` | 未解決の QA 項目を提示してユーザーの判断を収集 |
| 6 | `work:issue-create` | `.work/issues/` 配下にイシューファイルを作成 |
| 7 | `work:issue-scan` | `work:issue-scanner` サブエージェントを並列起動して観点をスキャンし、発見をイシューとして記録して自動マージ |
| 8 | `work:issue-review` | 未レビューイシューを捌く（`## 意思` と各 `## QA` の `**回答**:` を 1 つに絞る）— スマホ主用途・AskUserQuestion |
| 9 | `work:issue-resolve` | ループ駆動: レビュー済みイシューを消化 — accept→`issue-resolver` サブエージェント、reject→`chore/rejected-issues` |
| 10 | `work:impl-review` | タスクドキュメントに照らして実装をレビュー |
| 11 | `work:setup` | テンプレートから `.work/` ディレクトリ構造を初期化 |
| 12 | `work:plugin-migrate` | `.work/` 静的テンプレートを現在の work バージョンに更新 |
| 13 | `work:worktree-create` | ブランチ用の git ワークツリーを作成 |
| 14 | `work:vscode-workspace-sync` | VS Code の `.code-workspace` ファイルを git ワークツリーと同期 |
| 15 | `work:branch-index-cleanup` | `.work/tasks/index.yaml` から古いエントリを削除 |
| 16 | `work:conversation-to-claude` | セッションを解析し成果物を自動生成（skill / rule / hook / CLAUDE.md / incidents / glossary）。claude-kit creator スキルに委譲 |
| 17 | `work:plugin-config` | work プラグインの env トグルをインタラクティブに設定（ブランチ強制、マージ提案、ワークツリー、コミットタイプなど） |

## エージェント

| # | エージェント | 役割 |
|---|---|---|
| 1 | `work:issue-scanner` | 1 つの観点（フォルダ / grep / レイヤー / ファイル群）を ref-inject の reference と照合してスキャンし、ISSUE ファイルを書き出す。`work:issue-scan` が起動する |
| 2 | `work:issue-resolver` | accept された 1 件のイシューを対応: `work:start` でブランチを切り、修正を実装し、マージ待ち最終コミットで止まる。`work:issue-resolve` が起動する |

## フック

| # | イベント | トリガー | スクリプト / プロンプト |
|---|---|---|---|
| 1 | `PreToolUse` | Edit / Write / MultiEdit / Read | `hooks/scripts/inject_references.py` — リファレンス自動注入 |
| 2 | `PreToolUse` | Bash | `hooks/prompts/master-commit-guard.md` — 保護ブランチへのコミットをブロック |
| 3 | `PreToolUse` | Bash | `hooks/prompts/git-guard.md` — `git push` / `git merge` を確認 |
| 4 | `UserPromptSubmit` | — | `hooks/prompts/user-prompt-submit.md` — 各プロンプト前にブランチコンテキストを注入 |
| 5 | `Stop` | — | `hooks/prompts/stop.md` — タスク更新リマインド / マージ提案 |
| 6 | `PreCompact` | — | `hooks/prompts/pre-compact.md` — `/compact` 前に `/work:conversation-to-claude` を実行 |

## 環境変数

**太字** = デフォルト値（キー未設定時に適用）。真偽値は `true` / `false` のみ記載（`1` / `yes` / `on` も truthy として扱われる）。

| 変数名 | 説明 | 値 |
|---|---|---|
| `${WORK_USE_WORKTREE}` | 新規ブランチごとに git ワークツリーを作成するか | - **true**<br>- false |
| `${WORK_GUARD}` | git-guard フックを有効化（push / merge を確認） | - **true**<br>- false |
| `${WORK_PROTECTED_BRANCHES}` | master-commit-guard が保護するブランチ（カンマ区切り） | **master,main,develop** |
| `${WORKSPACE_STOP_REMINDER}` | Stop 時にタスク更新リマインダーを表示するか | - **true**<br>- false |
| `${WORKSPACE_MERGE_PROPOSAL}` | Stop 時に `/work:merge` の実行を提案するか | - **true**<br>- false |
| `${WORK_BRANCH_AUTHOR}` | ブランチ名に挿入する著者セグメント（`{type}/{author}/{title}`）。任意の名前を設定すると有効 | **(未設定)** |
| `${WORK_BASE_BRANCH}` | 新規ワークツリーのベースブランチ。設定時は `git worktree add` が `HEAD` ではなくこの commit-ish から分岐 | **(未設定)** |
| `${CLAUDE_KIT_INJECTION_DISABLE}` | キルスイッチ — truthy で claude-kit のリファレンス注入を無効化 | - true<br>- **false** |
| `${DEV_KIT_INJECTION_DISABLE}` | キルスイッチ — truthy で dev-kit のリファレンス注入を無効化 | - true<br>- **false** |
| `${WORK_COMMIT_LANG}` | コミットメッセージの言語（`JP`=日本語 / `EN`=英語） | - **JP**<br>- EN |
| `${WORK_COMMIT_TYPE}` | Conventional Commits のタイププレフィックス（`feat:` / `fix:` / `chore:` など）を付与するか | - **true**<br>- false |
| `${ISSUE_SCAN_AGENTS}` | `issue-scan` 1 回あたりのスキャン観点数（= 並列 `issue-scanner` サブエージェント数）。整数 | **1** |
| `${WORK_PRECOMPACT_CONV2CLAUDE}` | `PreCompact`（`/compact` 前）で `/work:conversation-to-claude` を実行するか | - **true**<br>- false |
| `${WORK_MERGE_CONV2CLAUDE}` | `work:merge` 中にワークツリー内で `/work:conversation-to-claude` を実行するか | - **true**<br>- false |

## タスクドキュメント構造

各ブランチは `.work/tasks/{YYMMDD}_{title}/{YYMMDD}-{日本語タイトル}.task.md` の単一ファイルを使用し、以下のセクションを持つ：

- `## 作業内容` — タスク説明とチェックリスト
- `## QA` — 実装前に解決すべき質問
- `## テスト` — テスト項目
- `## 変更内容` — 実装メモ

ブランチ名はデフォルト `{type}/{title}`（PR 番号プレフィックスなし）。`${WORK_BRANCH_AUTHOR}` が設定されている場合は `{type}/{author}/{title}` になる。内部 ID は `index.yaml` で管理。

## 変更履歴

| # | バージョン | 日付 | 概要 |
|---|---|---|---|
| 1 | 2.67.0 | 2026-06-02 | イシューのユーザー回答欄を再設計: `# ユーザー回答欄`（`## 意思` / `## QA`）をファイル**上部**へ移動（スクロールせず回答済みか分かる）、AI 記入のイシュー本文は下に。各 QA に番号・タイトル・選択肢・AI `**推奨**:` を必須化。`## 自由記述` を廃止（自由補足は `## 意思` の回答に inline）。`回答候補`/空 `回答` 方式を廃止し、AI が各 `**回答**:` に全候補を事前記入→ユーザーが 1 つに絞る方式に。`イシュー.md` テンプレート・`issue-create` / `issue-review` / `issue-resolve` / `issue-scan`・`issue-scanner` / `issue-resolver` エージェント・本 CLAUDE.md を更新 |
| 1 | 2.66.0 | 2026-06-02 | `work:plugin-config` スキルを復活 — work プラグイン変数のインタラクティブな env トグル設定 |
| 2 | 2.65.1 | 2026-06-02 | `## スキル` テーブルの古いスキル名を修正: `work:pr-handoff` → `work:branch-reserve`、`work:pr-show` → `work:branch-show` |
| 2 | 2.65.0 | 2026-06-02 | 対話式 `work:plugin-config` スキルを削除（env トグルは `settings.json` を直接編集）。`## 環境変数` テーブルを統一 3 列形式（変数名 / 説明 / 値、デフォルトは太字）に再フォーマット |
| 1 | 2.64.0 | 2026-06-02 | 用語集記述ガイドのリファレンス `references/conversation/` を日本語ファイル名 `用語集.md`（+ `.jp.md`）にリネーム（カタカナ名を廃止）。`injection_rules` / `_index` / 相互リンク・各ポインタを更新 |
| 1 | 2.63.0 | 2026-06-02 | イシューファイル形式を刷新: YAML フロントマターを廃止し、2 分割の Markdown（AI 記入の上半分 + `# ユーザー回答欄`〔`## 意思` / `## QA` / `## 自由記述`、回答候補を用意し `**回答**:` は空〕）に。`## 修正案`→`## 対応案` に改名し 問題点/詳細 セクションを廃止（背景/現状 で代替）。`status` / `branches` を `_index.yaml` へ移管（`issue-tool.py` に `add-branch` 追加）。`issue-create` / `issue-review` / `issue-resolve` / `issue-scan`・`issue-scanner` / `issue-resolver` エージェント・`work:start` のイシュー連携を更新 |
| 2 | 2.61.0 | 2026-06-02 | `${WORK_BASE_BRANCH}` env var を追加 — 新規ワークツリー作成時のベースブランチを指定可能に |
| 2 | 2.60.0 | 2026-06-01 | イシューのレビュー/対応ワークフロー: ISSUE にフロントマター（`decision` / `status` / `branches` / 自由記述 `instruction`）を追加し QA をイシューへ移設。`work:issue-review`（スマホ主用途・AskUserQuestion で捌く）+ `work:issue-resolve`（ループ駆動・1 起動 1 イシュー: accept→`issue-resolver` サブエージェント。そのモデルはイシュー難易度で選択＝sonnet/opus・haiku 不使用、reject→共有 `chore/rejected-issues`）+ `work:issue-resolver` エージェントを追加。`work:start` がイシュー連携（`status: in_progress` 設定・`branches` 追記・`## 関連イシュー` 記入）。`issue-tool.py` に `set-status` を追加、`close --linked-branch` は任意のブランチ名に変更。work ライフサイクルを CLAUDE.md に文書化 |
| 2 | 2.59.0 | 2026-06-01 | `work:setup-wizard` スキルと `SessionStart` フック（`setup_check.py`）を削除 |
| 2 | 2.56.0 | 2026-05-31 | `issue-scan` を並列 `work:issue-scanner` サブエージェント（新規エージェント）へ委譲するオーケストレーターに再設計。観点（フォルダ/grep/レイヤー/ファイル群）でスキャン・`${ISSUE_SCAN_AGENTS}` 追加。`issue-save` スキルを削除し、イシューファイルのフォーマットを `work-dir/イシュー` リファレンスへ集約（`issue-create`・`issue-scanner` が直接記述） |
| 2 | 2.55.0 | 2026-05-31 | `plugins/work/templates/` と `setup-task.py` を削除。テンプレート／フォルダ別構成定義を `references/work-dir/`（`タスクドキュメント` / `タスクインデックス` / `イシュー` / `ワークディレクトリ構成`）へ移し、該当 `.work/` パスの作成・編集時に ref-inject で注入。`work:start` は注入テンプレートを元にブランチドキュメントを直接作成。ブランチドキュメントのファイル名に `.branch.md` 拡張子を付与。`ドットワークディレクトリ構成`→`ワークディレクトリ構成` にリネーム・`TODOテンプレート同期` を削除 |
| 3 | 2.54.0 | 2026-05-31 | index.yaml のブランチ索引を `branch` キー化（id/last_id/tags 撤廃）、`created` サロゲート追加、レガシー分を `index.archive.yaml` へ移行、`next-id` 撤廃・`set-completed` を `--branch` 化 |
| 4 | 2.53.1 | 2026-05-31 | `references/` をカテゴリ別サブフォルダへ分割：`notes/`・`work-dir/`・`skill-sync/` |
| 2 | 2.53.0 | 2026-05-31 | ノートを「現在の仕様書」に再定義（スナップショット。本文に履歴を書かず `## 変更履歴` テーブルのみ・frontmatter 無し）、`ノート記述内容ルール` リファレンス追加、`.work/specs` を notes へ統合しフォルダ削除 |
| 2 | 2.52.0 | 2026-05-31 | ブランチ文書ファイル名を日本語タイトル基準に変更（`{YYMMDD}-{日本語タイトル}.md`）、`index.yaml` に `branch` フィールド追加 |
| 2 | 2.51.0 | 2026-05-31 | `${WORK_COMMIT_LANG}` / `${WORK_COMMIT_TYPE}` env var を追加 — コミットメッセージの言語とタイププレフィックスを設定可能に |
| 2 | 2.50.0 | 2026-05-31 | `${WORK_BRANCH_AUTHOR}` env var を追加 — ブランチ名に作者名セグメントを挿入 |
| 2 | 2.48.0 | 2026-05-30 | `work:notes-to-claude` スキルを削除 — プラグイン間依存を排除 |
| 3 | 2.47.0 | 2026-05-30 | `work:plugin-config` 管理対象トグルに `${CLAUDE_KIT_INJECTION_DISABLE}` / `${DEV_KIT_INJECTION_DISABLE}` を追加 |
| 4 | 2.46.2 | 2026-05-30 | `issue-scan` スキルの古い `py-kit`/`next-kit` 記述を削除、`_injection_rules.yaml` に更新 |
| 5 | 2.46.0 | 2026-05-30 | Stop フックのインライン python を `hooks/scripts/stop.py` + `_common.py` に抽出 |
| 6 | 2.44.0 | 2026-05-30 | ブランチドキュメントを単一ファイル（`{branch-hyphenated}.md`）に統合；`plugin-migrate` スキルにリネーム |
| 7 | 2.43.0 | 2026-05-30 | `${WORKSPACE_MERGE_PROPOSAL}` env トグルを追加 |
| 8 | 2.42.0 | 2026-05-30 | `WORKSPACE_PROTECTED_BRANCHES` env トグルを追加 |
| 9 | 2.41.0 | 2026-05-30 | `impl-review` Step 4 をバッチ AskUserQuestion 方式に変更（最大 4 件/回） |
| 10 | 2.40.0 | 2026-05-30 | `guard-kit` を work プラグインに統合 |
| 11 | 2.39.0 | 2026-05-30 | env トグルを対話的に設定する `work:plugin-config` スキルを追加 |
| 1 | 2.62.0 | 2026-06-02 | `work:conversation-to-claude` を復活（元は claude-kit、PR181 で削除）— セッションを解析し成果物を自動生成（skill / rule / hook / CLAUDE.md / incidents / glossary）。claude-kit creator スキルに委譲。glossary/incidents の取り込み基準を厳格化（CLAUDE.md / rule / フォルダ構造で既出の内容をスキップ）。`PreCompact` フック（`pre-compact.py`、トグル `${WORK_PRECOMPACT_CONV2CLAUDE}`）を追加し `/compact` 前に実行。`work:merge` 内ワークツリーで実行するステップを復活（トグル `WORK_MERGE_CONV2CLAUDE`）。`references/conversation/用語集.md` + `インシデント.md`（glossary/incidents 記述ガイド）を追加し、`.claude/rules/glossary.md` / `.claude/rules/incidents.md` / `.claude/references/incidents/**` 編集時に ref-inject で自動注入 |
| 1 | 2.57.0 | 2026-05-31 | タスクフォルダ名を日本語化（`{YYMMDD}_{日本語タイトル}`）。既存217件を一括リネームし、`index.archive.yaml` の `task:` を追従（8→6桁正規化）、`work:start`・`work-dir` リファレンスのフォルダ名記述を日本語名方針へ統一 |
| 2 | 2.56.0 | 2026-05-31 | `issue-scan` を並列 `work:issue-scanner` サブエージェント（新規エージェント）へ委譲するオーケストレーターに再設計。観点（フォルダ/grep/レイヤー/ファイル群）でスキャン・`${ISSUE_SCAN_AGENTS}` 追加。`issue-save` スキルを削除し、イシューファイルのフォーマットを `work-dir/イシュー` リファレンスへ集約（`issue-create`・`issue-scanner` が直接記述） |
| 3 | 2.55.0 | 2026-05-31 | `plugins/work/templates/` と `setup-task.py` を削除。テンプレート／フォルダ別構成定義を `references/work-dir/`（`タスクドキュメント` / `タスクインデックス` / `イシュー` / `ワークディレクトリ構成`）へ移し、該当 `.work/` パスの作成・編集時に ref-inject で注入。`work:start` は注入テンプレートを元にブランチドキュメントを直接作成。ブランチドキュメントのファイル名に `.branch.md` 拡張子を付与。`ドットワークディレクトリ構成`→`ワークディレクトリ構成` にリネーム・`TODOテンプレート同期` を削除 |
| 4 | 2.54.0 | 2026-05-31 | index.yaml のブランチ索引を `branch` キー化（id/last_id/tags 撤廃）、`created` サロゲート追加、レガシー分を `index.archive.yaml` へ移行、`next-id` 撤廃・`set-completed` を `--branch` 化 |
| 5 | 2.53.1 | 2026-05-31 | `references/` をカテゴリ別サブフォルダへ分割：`notes/`・`work-dir/`・`skill-sync/` |
| 3 | 2.53.0 | 2026-05-31 | ノートを「現在の仕様書」に再定義（スナップショット。本文に履歴を書かず `## 変更履歴` テーブルのみ・frontmatter 無し）、`ノート記述内容ルール` リファレンス追加、`.work/specs` を notes へ統合しフォルダ削除 |
| 3 | 2.52.0 | 2026-05-31 | ブランチ文書ファイル名を日本語タイトル基準に変更（`{YYMMDD}-{日本語タイトル}.md`）、`index.yaml` に `branch` フィールド追加 |
| 3 | 2.51.0 | 2026-05-31 | `${WORK_COMMIT_LANG}` / `${WORK_COMMIT_TYPE}` env var を追加 — コミットメッセージの言語とタイププレフィックスを設定可能に |
| 3 | 2.50.0 | 2026-05-31 | `${WORK_BRANCH_AUTHOR}` env var を追加 — ブランチ名に作者名セグメントを挿入 |
| 3 | 2.48.0 | 2026-05-30 | `work:notes-to-claude` スキルを削除 — プラグイン間依存を排除 |
| 4 | 2.47.0 | 2026-05-30 | `work:plugin-config` 管理対象トグルに `${CLAUDE_KIT_INJECTION_DISABLE}` / `${DEV_KIT_INJECTION_DISABLE}` を追加 |
| 5 | 2.46.2 | 2026-05-30 | `issue-scan` スキルの古い `py-kit`/`next-kit` 記述を削除、`_injection_rules.yaml` に更新 |
| 6 | 2.46.0 | 2026-05-30 | Stop フックのインライン python を `hooks/scripts/stop.py` + `_common.py` に抽出 |
| 7 | 2.44.0 | 2026-05-30 | ブランチドキュメントを単一ファイル（`{branch-hyphenated}.md`）に統合；`plugin-migrate` スキルにリネーム |
| 8 | 2.43.0 | 2026-05-30 | `${WORKSPACE_MERGE_PROPOSAL}` env トグルを追加 |
| 9 | 2.42.0 | 2026-05-30 | `WORKSPACE_PROTECTED_BRANCHES` env トグルを追加 |
| 10 | 2.41.0 | 2026-05-30 | `impl-review` Step 4 をバッチ AskUserQuestion 方式に変更（最大 4 件/回） |
| 11 | 2.40.0 | 2026-05-30 | `guard-kit` を work プラグインに統合 |
| 12 | 2.39.0 | 2026-05-30 | env トグルを対話的に設定する `work:plugin-config` スキルを追加 |
