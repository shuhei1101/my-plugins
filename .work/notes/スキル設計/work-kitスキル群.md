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

## merge スキル — Step 10/11 順序入れ替え（#238）

### 問題

`work:merge` の Step 10（完了報告）でターンが終了するため、その後のストップフックが
`notify-aituber` を呼んで新ターンが開始される。このため、Step 11（`branch-reserve` →
`work:start`）で発生するノートコミットが次のターンに分離してしまっていた。

### 変更

Step 11（`branch-reserve` 自動呼び出し）を Step 10（完了報告）より前に移動。

| 変更前 | 変更後 |
|---|---|
| Step 9: QA確認・コミット | Step 9: QA確認・コミット（変更なし） |
| Step 10: 完了報告 → ターン終了 | Step 10: branch-reserve 呼び出し（ノートコミット） |
| Step 11: branch-reserve（次ターンで実行） | Step 11: 完了報告 → ターン終了 |
| Step 12: branch-show | Step 12: branch-show |

これにより全コミットがターン終了前に完了し、ストップフック後のターンではコミットが発生しなくなる。

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

## ブランチドキュメントの H1 をタイトル（日本語）に変更（#233）

### 変更前

```markdown
# chore/update-branch-doc-h1-title
```

H1 見出しにブランチ名（`{type}/{title}`）を機械的に埋め込んでいた。

### 変更後

```markdown
# {日本語タイトル}
```

H1 はそのブランチ作業を表す日本語タイトルを書くプレースホルダーに変更。
`work:start` の Step 7 で Claude が適切な日本語タイトルを記入する。

### 変更ファイル

- `plugins/work/templates/.work/tasks/yymmdd_xxx/yymmdd-branch-name.md`: H1 プレースホルダーを変更
- `plugins/work/scripts/setup-task.py`: `{ブランチ名}` 置換エントリを削除
- `plugins/work/skills/start/SKILL.md` / `SKILL.jp.md`: Step 7 に H1 記入指示を追記

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

### v2.48.0 以降の変更（#232 追記）

- `.work/CLAUDE.md` / `.work/CLAUDE.jp.md` は **削除対象**（ref-inject に移行済みで不要）
- `plugin-update` スキルの Step 2 を改訂:
  - 旧: CLAUDE.md・CLAUDE.jp.md を上書きコピー
  - 新: CLAUDE.md・CLAUDE.jp.md が存在すれば `git rm` で削除し、`.gitignore` のみを同期

## work:start テンプレートの行4削除と QA 観点補強（#245）

### 変更前

`## 作業内容` の必須行に「ルール / CLAUDE.md を更新」（行4）が含まれていた。

### 変更後

ブランチ作業中に CLAUDE.md やルールを更新する指示がない限り更新不要なため、
行4を削除してテンプレートをシンプルにした。

あわせて以下も改善：

- 行1の「開いている質問」→「未解決の質問」に改め、意図を明確化
- Step 2 の「未解決の質問」洗い出し観点を具体化（保守性・コスト・パフォーマンス・ライブラリ選定・代替実装等）

### 変更ファイル

- `plugins/work/skills/start/SKILL.jp.md`: 行4削除・Step 2 観点補強・行1文言改善
- `plugins/work/skills/start/SKILL.md`: 同上（EN 版）

## ブランチドキュメントテンプレートのテスト表列更新（#247）

### 変更前

`## テスト` セクションが手動テスト・動作確認の記録向けで、列は「確認内容・実測結果・判定」だった。

### 変更後

単体テストのメソッド単位記録向けに列を変更した：

| # | ファイル名 | メソッド名 | 期待値 | 実値 | 判定 | 補足 |

セクション説明文も「手動テスト・動作確認の実施記録」に更新。

### 変更ファイル

- `plugins/work/templates/.work/tasks/yymmdd_xxx/yymmdd-日本語タイトル.md`: テスト表の列を更新

## branch-index-cleanup スキル — 現行仕様

git ブランチと `index.yaml` / `index.archive.yaml` の乖離を整理するワークフロー。`git branch` に存在し両 index に未登録のブランチを「未登録ブランチ」として収集し、A/B/C に分類して処置する。

| 分類 | 意味 | 処置 |
|---|---|---|
| A | 完了済み・不要 | ブランチ削除のみ |
| B | 完了済み・記録したい | `index.archive.yaml` に追記 → ブランチ削除 |
| C | 作業中・継続 | `index.yaml` に追記（`completed: false`） |

- B はブランチ名（例 `PR42/feat/some-feature`）から `id` / `title` / `type` を自動推定し（`summary` は空欄）、ユーザーが確認・修正できるインタラクティブフロー。

## merge フロー — index archive の現行仕様

| ファイル | git 管理 | 存在場所 |
|---|---|---|
| `index.yaml` | gitignore（非追跡） | メインリポジトリのみ |
| `index.archive.yaml` | 追跡済み | メインリポジトリ・worktree 双方 |

- archive は `completed: true` のエントリのみを移動するため、merge では先に `set-completed` で `true` をセットする。
- archive コマンドはメインリポジトリの `index.yaml` を読み、worktree の `index.archive.yaml` に書き込む。worktree でコミットし `--no-ff` マージで master に取り込む。
- `python index-tool.py set-completed [index_yaml] --id N` で対象エントリの `completed` を `true` に更新して上書き保存（対象が無ければエラー終了）。

## issue-create / issue-scan — イシューファイルフォーマット

### 修正案セクションの構造

`## 修正案` を含める場合、以下の3サブセクションが必須。内容なしは「なし」と記載する。

```markdown
## 修正案

### 暫定対応

{暫定対応の説明。なければ「なし」}

### 恒久対策

{恒久対策の説明。なければ「なし」}

### 再発防止

{再発防止策。なければ「なし」}
```

### 横展開セクション

`## 水平展開` は `## 横展開` に改名。提供されなかった場合はセクション自体を省略する。

## タスクドキュメント拡張子・用語統一と work:quick-task（v2.68.0）

### 拡張子変更

ブランチごとの正本ドキュメントのファイル拡張子を `.branch.md` → `.task.md` に変更（`.work/tasks/`
フォルダ名と整合）。既存 266 件を `git mv` で一括リネーム。ref-inject の注入パターンも
`.work/tasks/**/*.task.md` に更新。consumer プロジェクト向けに `work:plugin-migrate` が
`.branch.md`→`.task.md` リネームを行う（Step 4 追加）。

### 用語統一

概念名を「ブランチドキュメント / branch document / ブランチ文書」→「タスクドキュメント /
task document」に統一（全カレント仕様の references / skills / agents / hooks / CLAUDE.md）。
changelog・変更履歴の過去エントリは事実記録として不変。git の「ブランチ」概念（`> ブランチ:`
ヘッダー、ブランチ名等）は対象外。

### work:quick-task スキル新設

git ブランチ/コミットを必要としない軽量作業向けの新スキル。対象は (1) 調査・確認のみ、
(2) gitignore 除外・未追跡ファイルだけの編集。worktree / ブランチ / index 登録 / QA ゲート /
merge は行わない。UserPromptSubmit フックの Step 3 が「追跡ファイルへのコミットを伴うか」で
`work:start`（伴う）と `work:quick-task`（伴わない）を振り分ける。

## 変更履歴

| # | 日付 | 変更内容 | 関連タスク |
|---|---|---|---|
| 1 | 260531 | branch-index-cleanup / merge archive フローの現行仕様を specs から追記 | 260531_notes-spec-and-ref-inject |
| 2 | 260531 | 修正案サブセクション細分化・横展開改名を追記 | 260531_issueスキル改善 |
| 3 | 260602 | 拡張子 .branch.md→.task.md・用語をタスクドキュメントに統一・work:quick-task 新設を追記 | 260602_ブランチ文書拡張子をtaskへ変更 |
