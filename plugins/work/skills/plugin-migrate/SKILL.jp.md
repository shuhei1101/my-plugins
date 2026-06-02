<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

---
name: work:plugin-migrate
description: |
  カレントプロジェクトのプラグイン生成物を、現在インストール済みのプラグインバージョンに合わせて更新する:
  work の `.work/.gitignore` ファイルを同期し、レガシーの `.work/CLAUDE.md` を削除し、
  `index.yaml` を最新スキーマへ移行する。他プラグインの生成物は対象外（各プラグインが
  同等のスキルを持っている場合はそれを使う）。
  手動起動のみ — `/work:plugin-migrate` を使う。
---

# work:plugin-migrate — プラグイン生成物を最新版に揃える

旧 `update` スキルからの置き換え（PR168）。スコープは **work 自身の静的テンプレ** のみ:
`.work/` の `.gitignore` ファイルの同期、レガシー `CLAUDE.md` の削除、`index.yaml` のスキーマ移行。

他プラグインの diff ロジックは意図的に対象外 — 各プラグインが自分の更新パスを所有し、
必要なら同等のスキル（例: `/{plugin}:plugin-migrate`）を提供する。
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

### ステップ 2: レガシー `.work/CLAUDE.md` を削除し、`.gitignore` を同期

#### 条件

- Step 1 完了

#### 処理

1. `.work/CLAUDE.md` が存在する場合、`git rm` で削除する
   - このファイルは ref-inject に移行済みのため不要
   - `.work/CLAUDE.jp.md` が存在する場合も同様に削除する
2. 以下の `.gitignore` ファイルをハードコードされた内容で書き込む（上書き）:
   - `.work/tasks/.gitignore` → 内容: `index.yaml`
   - `.work/issues/.gitignore` → 内容: `_index.yaml`（`.work/issues/` が存在しない場合は作成してから書き込む）
3. どのファイルが変更されたかを報告

→ ステップ 3 へ

#### 出力

- `.work/CLAUDE.md` / `.work/CLAUDE.jp.md` が削除済み（存在した場合）
- `.work/tasks/.gitignore`、`.work/issues/.gitignore` が最新版に更新済み

---

### ステップ 3: `.work/tasks/index.yaml` を branch キースキーマへマイグレーション

#### 条件

- Step 2 完了
- `.work/tasks/index.yaml` が存在

#### 処理

1. `.work/tasks/index.yaml`（および存在すれば `.work/tasks/index.archive.yaml`）を読む
2. どのエントリにも `id`・`tags` がなく、トップレベルに `last_id` もない → 移行済みとしてスキップ
3. それ以外は branch キースキーマへ移行する:
   - 全エントリから `id` と `tags` を除去
   - トップレベルの `last_id` キーを除去
   - `branch`・`title`・`type`・`summary`・`task`・`completed` のみ残す
   - `index.archive.yaml` にも同じ正規化を適用
   - 更新ファイルを書き込む

→ ステップ 4 へ

#### 出力

- `index.yaml`（および `index.archive.yaml`）が branch キースキーマになる（`id` / `last_id` / `tags` なし）
- 既に移行済みの場合：「index.yaml は既に branch キースキーマです — スキップしました」と報告

#### 注記

- ブランチインデックスは `branch` を識別キーとする。数値 `id` や `last_id` は存在しない
- `index.yaml` は gitignore されている — コミット不要。`index.archive.yaml` は git 追跡
- マイグレーションは冪等 — 移行後に再実行しても no-op

---

### ステップ 4: `.branch.md` のタスクドキュメントを `.task.md` にリネーム

#### 条件

- Step 3 完了

#### 処理

1. 旧拡張子のまま git 追跡されているタスクドキュメントを探す:
   ```bash
   git ls-files '.work/tasks/*.branch.md'
   ```
2. 各ファイルを `git mv` でリネーム（履歴を保持）:
   ```bash
   git ls-files '.work/tasks/*.branch.md' | while IFS= read -r f; do
     git mv "$f" "${f%.branch.md}.task.md"
   done
   ```
   - v2.68.0 でタスクドキュメントの拡張子を `.branch.md` → `.task.md` に変更。ref-inject の
     テンプレートは `*.task.md` にマッチするため、残った `.branch.md` はテンプレート注入を受けない。
3. 1 件も無ければ移行済み — スキップ。

→ ステップ 5 へ

#### 出力

- `.work/tasks/**/*.branch.md` をすべて `*.task.md` にリネーム（または「該当なし — スキップ」）

---

### ステップ 5: 確認とコミット

#### 条件

- Step 4 完了

#### 処理

1. worktree の `git status` と `git diff` をユーザーに表示
2. グループ化した変更を説明的なメッセージでコミット:
   - `chore: sync work .work/ templates to v{version}`

→ ステップ 6 へ

---

### ステップ 6: 完了を報告

#### 処理

1. 更新されたすべてのファイルをリスト化
2. ファイルに変更がない場合、「work プラグインの成果物はすべて最新版です」と報告
3. ユーザーに準備完了後に `/work:merge` を実行して同期ブランチをマージするよう提案

→ 完了
