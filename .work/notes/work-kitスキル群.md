---
created_at: 2026-05-23
updates:
  - 2026-05-23 — PR91: pr-handoff スキルの追加
  - 2026-05-24 — PR109: pr-show スキルを merge Step 12 から切り出し
  - 2026-05-29 — PR163: worktree-kit を統合（work-add / vscode-workspace-sync を取り込み）
  - 2026-05-30 — PR172: プラグインを work-kit → workspace にリネーム、env var も WORK_KIT_* → WORKSPACE_* に変更
  - 2026-05-31 — #219: merge スキル Step 3 を master 取り込み必須フローに変更
  - 2026-05-31 — #226: タスクドキュメントのファイル名に日付プレフィックスを追加、作業内容テーブル構造を改訂
related_prs:
  - PR91
  - PR109
  - PR163
  - PR172
---

# work-kit スキル群 — 設計メモ

## 概要

work-kit プラグインに含まれるスキルの設計・目的・相互関係を記録するノート。

## スキル一覧

| スキル名 | 目的 |
|---|---|
| `work-start` | 新しいPRを開始：ワークツリー・タスクフォルダ・TODO.md・QA.mdを作成 |
| `merge` | PRをマージ：TODO確認・git merge・index.yaml更新・ワークツリー削除 |
| `update` | work-kit スキルを手動更新する |
| `setup` | `.work/` ディレクトリを初期化する（プロジェクトに初回導入） |
| `branch-index-cleanup` | 古いブランチとindex.yamlエントリをクリーンアップ |
| `branch-reserve` | 次ブランチをコンテキスト付きで予約（PR91で追加、#230でリネーム） |
| `branch-show` | 次ブランチ候補を3カテゴリ（着手可能・進行中・条件あり）で一覧表示（PR109で追加、#230でリネーム） |
| `work-add` | git worktree とブランチを作成（PR163 で worktree-kit から統合） |
| `vscode-workspace-sync` | VS Code `.code-workspace` の `folders` を worktree と同期する PostToolUse フックを設定（PR163 で worktree-kit から統合） |

## worktree-kit 統合（PR163）

worktree-kit プラグインを廃止し、`work-add` / `vscode-workspace-sync` を work-kit に取り込んだ。
work-kit ← worktree-kit の片方向依存しかなく、別プラグインに分ける利点がなかったため。

ワークツリーの利用可否は環境変数 `WORK_KIT_USE_WORKTREE` で切り替える:

- 未設定 / `true` 等 → ワークツリーを使用（デフォルト）
- `false` / `0` / `no` → ワークツリー作成をスキップし `.work/` 管理のみで継続

work-start Step 4 がこの env var を読んで分岐する（従来の「worktree-kit インストール有無」判定を置き換え）。

## branch-reserve スキルの設計（旧 pr-handoff）

### 目的

1つのPRが終わった後、次のセッション（真っさらなコンテキストのClaude）に  
「これまでの経緯」と「次のPRでやってほしいこと」を伝えるための指示書を生成する。

### 出力形式

コードブロックで会話内に出力（ファイル保存なし）。  
ユーザーがClaudeCodeのコピー機能で内容をコピーし、次のセッションに貼り付ける。

### 指示書の構成

1. **これまでの経緯** — 現在のセッションで行った作業の要約
2. **次のPRの依頼** — 次に対応してほしいPR番号・タイトル・具体的な内容
3. **参考情報** — 関連ファイルパス・注意点など

### トリガー条件

- ユーザーが「引き継ぎ書を作って」「次のPRの指示書を作って」「ハンドオフして」などと言ったとき
- ユーザーが「branch-reserve して」「ブランチを予約して」と言ったとき

## merge スキル — Step 3: master 取り込み必須化（#219）

マージ前に master の新しいコミットがある場合、**必ず** `git merge master` を実行してコンフリクトを確認するよう変更。

### 変更前（自律判断フロー）

- 変更の関連性を分析し、「影響なし」「master 優先」「ブランチ優先」「引き分け」の4択で自律判断
- 独立した変更と判断した場合は master 取り込みをスキップする可能性があった

### 変更後（必須フロー）

1. `git log HEAD..master --oneline` で master の進捗を確認
2. 新しいコミットがある → 必ず `git merge master` を実行
3. コンフリクトなし → Step 4 へ進む
4. コンフリクトあり → ユーザーに報告して停止（手動解消を待つ）

## タスクドキュメントのファイル命名規則（#226）

### 変更前

- ファイル名: `{type}-{title}.md`（例: `chore-work-template-update.md`）
- `## 作業内容` テーブル: `| 完了 | 作業内容 | 対象ファイル |`

### 変更後

- ファイル名: `{YYMMDD}-{type}-{title}.md`（例: `260531-chore-work-template-update.md`）
  - 日付は `--date` 引数、またはタスクフォルダ名（`YYMMDD_xxx`）から自動抽出
- `## 作業内容` テーブル: `| # | 完了 | 作業内容 |`（`対象ファイル` 列を廃止、`#` 番号列を追加）
- 全テーブルに `#` 番号列（最左列）を標準装備

### 変更ファイル

- `plugins/work/templates/.work/tasks/yymmdd_xxx/type-title.md` → `yymmdd-branch-name.md` にリネーム
- `plugins/work/scripts/setup-task.py`: ファイル名生成ロジックと参照テンプレートパスを更新
- `plugins/work/skills/start/SKILL.md` / `SKILL.jp.md`: 命名規則説明とテーブル仕様を更新

## plugin-update スキルと .work/ テンプレート同期（#232）

`/work:plugin-update` スキルは、work プラグインの `.work/` 内テンプレートファイルを最新版に同期する。

### 対象ファイル

| # | ファイル | 内容 |
|---|---|---|
| 1 | `.work/CLAUDE.md` | ワークスペース CLAUDE 指示（テンプレートが存在する場合） |
| 2 | `.work/CLAUDE.jp.md` | 〃 日本語版（テンプレートが存在する場合） |
| 3 | `.work/tasks/.gitignore` | `index.yaml` を gitignore |
| 4 | `.work/issues/.gitignore` | `_index.yaml` を gitignore |

### v2.48.0 時点の状況

- テンプレートに `CLAUDE.md` / `CLAUDE.jp.md` は存在しないためスキップ
- `tasks/.gitignore` は既存プロジェクトと同一内容
- `issues/.gitignore` は新規追加（既存プロジェクトに `issues/` フォルダが未作成の場合は作成）
