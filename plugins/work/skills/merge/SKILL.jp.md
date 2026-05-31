---
name: merge
description: |
  ブランチをマージ：TODOチェックリスト検証、インデックスアーカイブ、関連イシューのクローズ、
  --no-ff でマージ、ワークツリーとブランチの削除、ブランチドキュメント内の残存QAエントリ確認。
  「マージして」「merge して」「ブランチをマージしたい」でトリガー。
disable-model-invocation: true
---

<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->

# work:merge — ブランチをマージ

完全なマージフローを実行：TODO チェックリスト検証 → master 互換性確認 → 関連イシューのクローズ →
インデックスアーカイブ → `--no-ff` マージ → ワークツリークリーンアップ →
ブランチドキュメント内の残存 QA エントリ確認 → 次ブランチ候補用の branch-reserve 自動実行。

> **命名規則**: 新しいブランチは `{type}/{title}` を使用（`PR{N}/` プレフィックスなし）。
> 新しいワークツリーは `{repo}-wt-{type}-{title}` を使用します。
> レガシーブランチは引き続き `PR{N}/{type}/{title}` で記録されており、ワークツリーは `{repo}-wt-PR{N}` です。
> これらの記録された名前で処理してください — `index.yaml` と `git worktree list` から実際のブランチ/ワークツリーパスを読み取ってください。

---

## タスク

### ステップ 1: マージするブランチを特定

#### 条件

- 常に実行 — 最初に実行

#### 処理

1. マージするブランチが現在の会話セッション内で既に特定されている場合、それを使用して Step 2 に進みます
2. それ以外の場合、以下のコマンドを実行してアクティブエントリをリストアップします：

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py list-active .work/tasks/index.yaml
```

   各出力行は：`branch|title|type|task` — `title` は記録されたブランチ名です
   （新しいブランチ：`{type}/{title}`、レガシーエントリ：`PR{N} — {title}` の形式もサポート）
3. 複数のアクティブエントリが存在する場合、マージするエントリをユーザーに確認
4. 実際のブランチ名とワークツリーパスを解決します：
   - **新形式**（記録されたタイトルが `{type}/{title}`）：ブランチ = タイトル、
     ワークツリー = `{repo}-wt-{type}-{title}`（スラッシュをハイフンで置き換え）
   - **レガシー形式**（記録されたタイトルが `PR{N} — {title}` でブランチが `PR{N}/{type}/{title}` として存在）：
     リテラル `PR{N}/{type}/{title}` と `{repo}-wt-PR{N}` を使用
   - 不明な場合は `git worktree list` と `git branch --list` とクロスチェック

→ ステップ 2 へ

#### 出力

- ブランチドキュメントパス、ブランチ名、ワークツリーパスが確認されました

---

### ステップ 2: タスクチェックリストを検証

#### 条件

- Step 1 完了

#### 処理

1. `.work/tasks/{date}_{title}/{YYMMDD}-{日本語タイトル}.md` のブランチドキュメント内の
   `## 作業内容` テーブルを読み込み
2. すべての行の `完了` 列に `済` があることを確認

→ すべての行が `済` の場合のみ Step 3 に進む

#### 注記

##### 分岐

- 未完了の行が残っている → マージしない。ユーザーに報告して終了

---

### ステップ 3: マージ先ブランチをこのブランチに取り込む（ワークツリー内）

#### 条件

- Step 2 完了

#### 処理

このステップのすべてのコマンドは、メインリポジトリ（master ブランチ）ではなく、**ワークツリー内**（`{WORKTREE_PATH}`）で実行すること。

1. マージ先ブランチ（`PARENT_BRANCH`）を特定する — このブランチがマージされる先のブランチ。
   通常は `master`。`develop` ベースのブランチなら `develop`。
   不明な場合は Step 7 を参照（Step 7 でマージ実行前に親ブランチを確認する）。

2. 常にマージ先ブランチをこのブランチに取り込む — **事前の `git log` チェックやスキップは禁止**：

```bash
git -C {WORKTREE_PATH} merge <PARENT_BRANCH>
```

   既に最新の場合は harmless な no-op（`Already up to date.`）で終わる。
   新コミットがある状態でスキップすると、コンフリクトが master 上で表面化してしまう。

3. マージがクリーンに完了したか確認：

```bash
git -C {WORKTREE_PATH} status
```

   - **コンフリクトなし**（クリーンなマージ / `Already up to date.`）→ Step 4 に進む
   - **コンフリクトあり** → ここで停止。コンフリクトが発生しているファイルをユーザーに報告し、
     手動での解消を待ってから続行

→ ステップ 4 へ

#### 注記

##### 禁止事項

- このステップをスキップしない — マージ先に戻す前にマージ先ブランチの内容を取り込むことは必須
- **`git log` の出力を見てスキップを判断することを禁止** — `git merge <PARENT_BRANCH>` は必ず無条件で実行する

### ステップ 4: 関連イシューをクローズ（ワークツリー内）

#### 条件

- Step 3 完了

#### 処理

1. ワークツリーの `.work/tasks/{date}_{title}/{YYMMDD}-{日本語タイトル}.md`
   ブランチドキュメントの `## 関連イシュー` セクションを読み込み
2. **セクションが存在しない、空である、またはテンプレートプレースホルダー行のみを含む**
   （`| ISSUE-{N} | ... |`）→ このステップの残りをスキップして Step 5 に進む
3. テーブルの各行について、**ワークツリー内** でクローズコマンドを実行します：

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/issue-tool.py" close \
  --issues-dir {WORKTREE_PATH}/.work/issues \
  --issue-id ISSUE-{NNN} \
  --resolution {resolved|wontfix} \
  --linked-pr {N}
```

   スクリプトは以下を実行：
   - `.work/issues/ISSUE-{NNN}.md` → `.work/issues/closed/ISSUE-{NNN}.md` に移動
   - `_index.yaml` からエントリを削除（gitignored — コミット不要）
   - `_index.archive.yaml` に `closed_issues` エントリを追加（`linked_pr` 付き）
4. プロジェクトに `.work/issues/` が存在しない場合（イシュー管理を採用していない）、
   スクリプトはスキップメッセージを出力 — これを no-op として扱う
5. ワークツリー内の変更をコミット：

```bash
git -C {WORKTREE_PATH} add .work/issues/
git -C {WORKTREE_PATH} commit -m "chore: close related issues"
```

→ ステップ 5 へ

#### 注記

- イシューファイル移動は git 追跡リネーム。`_index.yaml` は gitignored のまま
- このコミットは Step 7 の `--no-ff` マージに含まれます
- イシュー行が処理されない場合、空のコミットを作成しないでください

##### set-completed/archive の前に実行する理由

このステップを **前に** `set-completed` / `archive` を実行すると、
イシュー クローズ コミットがブランチに残ります（意味的にはそこに属します）。
インデックス管理と混ぜない。

---

### ステップ 5: ブランチを index.yaml で完了とマーク

#### 条件

- Step 4 完了

#### 処理

1. 以下のコマンドを実行して、メインリポの `index.yaml` 内のエントリを
   `completed: true` としてマークします：

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py" set-completed \
  .work/tasks/index.yaml --branch {full-branch-name}
```

→ ステップ 6 へ

#### 注記

- **メインリポジトリ** ディレクトリから実行してください（ワークツリーではなく） —
  `index.yaml` は gitignored で、メインリポのみに存在
- `index.yaml` 自体にはコミットは不要 — gitignored のまま

---

### ステップ 6: 完了したインデックスエントリをアーカイブ

#### 条件

- Step 5 完了

#### 処理

1. 以下のコマンドを実行して、完了したエントリを **ワークツリーの** `index.archive.yaml`
   に移動します：

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py" archive \
  .work/tasks/index.yaml \
  {WORKTREE_PATH}/.work/tasks/index.archive.yaml
```

コマンドは移動されたエントリの数を出力します。`0` を出力した場合、
このステップの残りをスキップしてください。

2. エントリが移動された場合、ワークツリー内の `index.archive.yaml` をコミット：

```bash
git -C {WORKTREE_PATH} add .work/tasks/index.archive.yaml
git -C {WORKTREE_PATH} commit -m "chore: archive to index.archive.yaml"
```

→ ステップ 7 へ

#### 注記

- `index.yaml` は gitignored のまま — コミットは不要
- `index.archive.yaml` は git 追跡 — **ブランチ** にコミット（親ブランチではなく）。
  Step 7 の --no-ff マージに含まれます
- アーカイブコマンドはメインリポの `index.yaml` から読み込み、ワークツリーの
  `index.archive.yaml` に書き込み

---

### ステップ 7: マージを実行

#### 条件

- Step 6 完了

> ⚠️ **マージ前チェック必須**
> Step 6 でワークツリー内に `index.archive.yaml` がコミットされなかった場合、
> アーカイブ変更がマージコミットから欠落します。
> **Step 6 内のワークツリー内の `git commit` が完了してからマージコマンドを実行してください。**
> （Step 6 が 0 エントリ移動を報告した場合のみこのチェックをスキップしてください —
> コミットは不要でした）

#### 注記

##### 禁止事項

> このスキルが **ユーザーの最新メッセージで** 実行された場合のみマージしてください。
> スキルコンテキストが前のターンから残っている場合（現在のメッセージからではない）、
> マージしないでください — 前の実行の許可は引き継がれません。

> **このステップを実行する前に、Step 3 がクリーンに完了していること。** ワークツリー内で `git merge <PARENT_BRANCH>` が実行され、コンフリクトなし（クリーンなマージ / `Already up to date.`）と確認されている必要がある。Step 3 がスキップされた、またはコンフリクトが未解消の場合は進まず、先に Step 3 を修正すること。

#### 処理

1. 現在のブランチがこのブランチが分岐した親ブランチであることを確認します
   （例えば master から分岐した場合は `master`、develop から分岐した場合は `develop`）
2. `--no-ff` でマージ：

```bash
git merge --no-ff -m "{type}: {title}" {BRANCH_NAME}
```

   ここで `{BRANCH_NAME}` は実際のブランチ名です（新形式：`{type}/{title}`、
   レガシー：`PR{N}/{type}/{title}`）。

→ ステップ 8 へ

---

### ステップ 8: ワークツリーとブランチを削除

#### 処理

1. ワークツリーとブランチを削除：

```bash
git worktree remove {WORKTREE_PATH}
git branch -d {BRANCH_NAME}
```

→ ステップ 9 へ

#### 注記

##### 禁止事項

- ワークツリールートで `Remove-Item -Recurse` または `rm -rf` を実行しないでください

---

### ステップ 9: 残存 QA エントリを確認

#### 処理

1. `.work/tasks/{date}_{title}/{YYMMDD}-{日本語タイトル}.md`
   ブランチドキュメントの `## QA` セクションを確認し、残存する未解決エントリを
   ユーザーと確認
2. 変更がある場合はコミット：

```bash
git add .work/
git commit -m "docs: post-merge update"
```

→ ステップ 10 へ

---

### ステップ 10: 次ブランチ候補を branch-reserve に委譲

#### 条件

- `WORK_MERGE_AUTO_HANDOFF` が `false`/`0`/`no`/`off` ではない場合
  （デフォルト：有効）。無効な場合 → このステップをスキップしてステップ 11 に進む

#### 処理

1. マージされたブランチドキュメントを読み込み、その `## 次ブランチ候補` セクションを検査
2. **次ブランチ候補が存在する場合**：`/work:branch-reserve` を実行
   （ユーザー確認は不要）。すべての分類と予約ロジックをそのスキルに委譲
3. **次ブランチ候補が空の場合**: branch-reserve をスキップ

→ ステップ 11 へ

---

### ステップ 11: マージ完了を報告

#### 処理

1. ユーザーにマージが完了したことを報告
   - マージされたブランチ名とタスクフォルダを含める

→ ステップ 12 へ

---

### ステップ 12: 次ブランチ候補を 3 カテゴリで提示

#### 処理

マージされたブランチドキュメントパスをデータソースとして `/work:branch-show` を実行します。

#### 注記

完全なロジック（`## 次ブランチ候補` テーブル読み込み、各候補分類、
タイトルでのブランチ検索）は `branch-show` スキルで定義されています。
