<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

---
name: plugin-update
description: |
  カレントプロジェクトのプラグイン生成物を、現在インストール済みのプラグインバージョンに合わせて更新する:
  work の静的 `.work/` テンプレ（CLAUDE.md・.gitignore）を上書きし、
  `index.yaml` を最新スキーマへ移行する。他プラグインの生成物は対象外（各プラグインが
  同等のスキルを持っている場合はそれを使う）。
  手動起動のみ — `/work:plugin-update` を使う。
---

# work:plugin-update — プラグイン生成物を最新版に揃える

旧 `update` スキルからの置き換え（PR168）。スコープは **work 自身の静的テンプレ** のみ:
`.work/` の CLAUDE.md・`.gitignore`・`index.yaml` のスキーマ移行。

他プラグインの diff ロジックは意図的に対象外 — 各プラグインが自分の更新パスを所有し、
必要なら同等のスキル（例: `/{plugin}:plugin-update`）を提供する。
このスキルは決してプラグイン境界を跨がない。

---

## タスク

### ステップ 1: .work/ が存在することを確認し、作業ブランチを準備

#### 条件

- 必ず最初に実行

#### 処理

1. カレントプロジェクトに `.work/` が存在することを確認
2. 存在しない場合、ユーザーに `/work:setup` を先に実行するよう案内して終了
3. `/work:start` を実行してこの同期用の作業ブランチを作成
   （生成されたファイル編集が確認可能なブランチにランディングするよう）
4. worktree とブランチが作成されるまで待機

→ ステップ 2 へ

#### 出力

- `.work/` が確認済み。作業ブランチ / worktree が準備完了
- 以降のすべてのファイル編集とコミットはこのworktree上の作業ブランチ内で実行される

---

### ステップ 2: `.work/` 内のワークスペーステンプレートを上書き

#### 条件

- Step 1 完了

#### 処理

1. work プラグインテンプレートルート `${CLAUDE_PLUGIN_ROOT}/templates/.work/` を探索
2. テンプレートから以下のファイルをプロジェクトにコピー（上書き）:
   - `CLAUDE.md` → `.work/CLAUDE.md`
   - `CLAUDE.jp.md` → `.work/CLAUDE.jp.md`
   - `tasks/.gitignore` → `.work/tasks/.gitignore`
   - `issues/.gitignore` → `.work/issues/.gitignore`（テンプレートに存在する場合）
3. どのファイルが上書きされたかを報告

→ ステップ 3 へ

#### 出力

- `.work/CLAUDE.md`、`.work/CLAUDE.jp.md`、`.work/tasks/.gitignore` が最新版に更新済み

---

### ステップ 3: `.work/tasks/index.yaml` のマイグレーション（`last_id` がない場合は追加）

#### 条件

- Step 2 完了
- `.work/tasks/index.yaml` が存在

#### 処理

1. `.work/tasks/index.yaml` を読む
2. `last_id` が既に存在する → このステップをスキップ
3. `last_id` が存在しない場合:
   - `last_id` = すべてのエントリから `max(id)` を計算（空の場合は 0）
   - インデックスファイルの先頭に `last_id: {N}` を追加
   - 更新ファイルを書き込む

→ ステップ 4 へ

#### 出力

- `index.yaml` に `last_id` が存在
- 既に存在する場合：「index.yaml は既に last_id を持っています — スキップしました」と報告

#### 注記

- `index.yaml` は gitignore されている — コミット不要
- これはこのスキルが実行する唯一のスキーママイグレーション。
  より深い書き直しは、バージョンバンプに伴うワンオフスクリプトとして提供される

---

### ステップ 4: 確認とコミット

#### 条件

- Step 3 完了

#### 処理

1. worktree の `git status` と `git diff` をユーザーに表示
2. グループ化した変更を説明的なメッセージでコミット:
   - `chore: sync work .work/ templates to v{version}`

→ ステップ 5 へ

---

### ステップ 5: 完了を報告

#### 処理

1. 更新されたすべてのファイルをリスト化
2. ファイルに変更がない場合、「work プラグインの成果物はすべて最新版です」と報告
3. ユーザーに準備完了後に `/work:merge` を実行して同期ブランチをマージするよう提案

→ 完了
