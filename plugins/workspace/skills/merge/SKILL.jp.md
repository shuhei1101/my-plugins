---
name: merge
description: |
  ブランチをマージ: TODO チェックリスト確認 → master 適合確認 → ワークツリー内で conversation-to-claude 実行 → 関連イシューのクローズ → index アーカイブ → `--no-ff` マージ → ワークツリーとブランチの削除 → ドキュメント確認。
  トリガー: ユーザーが「マージして」「merge して」「ブランチをマージしたい」と言ったとき。
disable-model-invocation: true
---

<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->

# workspace:merge — ブランチをマージ

マージフロー全体を実行: TODO チェックリスト確認 → master 適合確認 → ワークツリー内での conversation-to-claude 実行（claude-kit インストール済みの場合） → 関連イシューのクローズ → index アーカイブ → `--no-ff` マージ → ワークツリークリーンアップ → ドキュメント内の残存 QA エントリ確認 → 次ブランチ候補があれば pr-handoff で自動予約。

> **ネーミング**: 新ブランチは `{type}/{title}` 形式（`PR{N}/` プレフィックスなし）を使用。新ワークツリーは `{repo}-wt-{type}-{title}` を使用。
> レガシーブランチは引き続き `PR{N}/{type}/{title}` 形式で、ワークツリーは `{repo}-wt-PR{N}` を使用できます。
> 記録されたブランチ / ワークツリーパスを`{N}` から再構築するのではなく、`index.yaml` と `git worktree list` から実際のパスを読み取ってください。
> 以下で言及する `{N}` は `index.yaml` で追跡される内部 ID です（コミットのクロスリファレンスに使用）。

---

## タスク

### ステップ 1: マージ対象のブランチを特定する

#### 条件

- 常に実行 — 最初に実行

#### 処理

1. 現在の会話セッション内でマージ対象のブランチが既に特定されている場合、そのブランチを使用してステップ 2 に進む
2. 特定されていない場合は、以下コマンドでアクティブエントリを一覧表示:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py list-active .work/tasks/index.yaml
```

   出力形式（1行 1 エントリ）: `id|title|type|task` — `title` は記録されたブランチ名（新形式: `{type}/{title}`、レガシー形式: `PR{N} — {title}`）
3. 複数のアクティブエントリが存在する場合はユーザーにどれをマージするか確認する
4. 実際のブランチ名とワークツリーパスを解決:
   - **新形式**（記録されたタイトルが `{type}/{title}`）: ブランチ名 = タイトル、ワークツリー = `{repo}-wt-{type}-{title}`（スラッシュをハイフンに置換）
   - **レガシー形式**（記録されたタイトルが `PR{N} — {title}` であり、ブランチが `PR{N}/{type}/{title}` として存在）: 文字通りの `PR{N}/{type}/{title}` と `{repo}-wt-PR{N}` を使用
   - 不明な場合は `git worktree list` と `git branch --list` でクロスチェック

→ ステップ 2 に進む

#### 出力

- 内部 ID `{N}`、ブランチドキュメントパス、ブランチ名、ワークツリーパスが確定

---

### ステップ 2: タスクチェックリストを確認する

#### 条件

- ステップ 1 完了

#### 処理

1. ブランチドキュメント（`.work/tasks/{date}_{title}/{branch-hyphenated}.md`）の `## 作業内容` テーブルを読む
2. すべての行の `完了` 列が `済` であることを確認

→ すべて `済` の場合のみステップ 3 に進む

#### 補足

##### 分岐

- 未完了行がある → マージせずユーザーに報告して停止

---

### ステップ 3: master との互換性を確認する

#### 条件

- ステップ 2 完了

#### 処理

1. このブランチが発散した後に master に新しいコミットがあるか確認:

```bash
git log HEAD..master --oneline
```

出力がない場合 → master は進んでいない、ステップ 4 にスキップ。

2. このブランチの変更と master の変更の間に関連性がないか確認。git コマンドは開始点として使い、最終的には文脈的な判断を適用:

```bash
# このブランチが何を変更したかを確認
git diff master...HEAD --name-only

# master のコミットが何をどこで変更したかをスキャン
git log HEAD..master --oneline --stat
```

   ファイル名マッチだけに依存しないこと — 以下の間接的な関連性も考慮:
   - このブランチが変更したファイルを **呼び出している、またはインポートしている側** を master が変更していないか
   - このブランチが依存している **インターフェース、型、スキーマ、または設定** を master が変更していないか
   - master が **命名規則や構造的な変更** を導入していて、このブランチのコードがそれ以前の状態を想定していないか

3. 関連のある master 側の変更内容と背景を読む:

```bash
git log -p HEAD..master -- {関連ファイル}
```

4. 各関連変更について、以下の観点から自律的に優先度を判定:
   - **新しさ**: どちらのコミットがより新しいか
   - **影響範囲**: master の変更は広く依存されている中心的なものか、それとも局所的か。中心的な変更ほど優先度が高い
   - **インターフェース変更**: master が関数シグネチャ、型、またはスキーマを変更した場合、このブランチは古いインターフェースを使用している可能性がある → ブランチ側を更新
   - **方向性の一貫性**: master とこのブランチは同じゴールに向かっているか、それとも逆方向か。逆方向は片方が誤りの可能性
   - **ブランチの目的**: このブランチが master のこの変更を修正するために存在する場合、ブランチを優先

5. 判断に基づいて、以下のいずれかを自律的に実行（ユーザー確認は不要）:
   - **対応不要**: 変更は独立している → ステップ 4 に進む
   - **master を取り込む**: master の関連変更をこのブランチが反映すべき — ブランチに master をマージ:

```bash
git merge master
```

   衝突を解決し、必要に応じてブランチの実装を互換性に適合させる。
   - **ブランチを優先**: このブランチが master を修正するもの、またはブランチのアプローチが明らかに新しく正しい → マージせずに進む
   - **判断が拮抗**: 「安全側」を選択 — master を取り込む（`git merge master`）、その後ブランチの意図に合わせて再適用

→ ステップ 4 に進む

#### 補足

##### 自律判定のタイブレーク順位（判断が不明な場合）

1. 新しさ — より新しいコミットを優先
2. 影響範囲 — より多くが依存する変更を優先
3. ブランチの目的 — ブランチがこの変更を修正するためのものなら、ブランチを優先
4. 安全側 — master を取り込み、その後ブランチを適合させる

---

### ステップ 4: ワークツリー内で conversation-to-claude を実行（claude-kit インストール済みの場合）

#### 条件

- ステップ 3 完了
- `WORKSPACE_MERGE_CONV2CLAUDE` が `false`/`0`/`no`/`off` でない（デフォルト: 有効）。無効の場合 → ステップ 5 にサイレントスキップ

#### 処理

1. 現在のセッションで `/claude-kit:conversation-to-claude` が利用可能なスキルリストに含まれているか確認
2. 含まれていない場合 → このステップをサイレントスキップ → ステップ 5 に進む
3. 含まれている場合 → **まずワークツリーディレクトリに移動してから** スキルを呼び出す:

```bash
cd {WORKTREE_PATH}   # 例: ../{repo}-wt-{type}-{title} （またはレガシー ../{repo}-wt-PR{N}）
```

   その後 `/claude-kit:conversation-to-claude` を呼び出し、完了を待つ。

4. 完了後、スキルが生成した `.claude/` ファイル（ルール / リファレンス / 用語集など）がブランチにコミット済みであることを確認。未コミットの場合、ワークツリー内でコミット:

```bash
git -C {WORKTREE_PATH} add .claude/
git -C {WORKTREE_PATH} commit -m "docs: conversation-to-claude artifacts #{N}"
```

5. メインリポジトリディレクトリに戻る:

```bash
cd -
```

→ ステップ 5 に進む

#### 補足

- このステップはブランチ削除前にセッション知識を永続化するために実行
- 会話が短くても省略しないこと — スキル側に判断させる

##### ワークツリーで実行する理由

メインリポジトリ（master）の cwd から `conversation-to-claude` を実行すると、生成された `.claude/` ファイルが master に直接コミットされ、ブランチの `--no-ff` マージに含まれません。
結果としてブランチ作業とセッション知識が別のコミットに散在します。
ワークツリーで実行することで、セッション知識がブランチに含まれ、マージコミット内での一貫性が保たれます。

##### 禁止事項

- master の cwd から `conversation-to-claude` を実行しないこと（master への直接コミットが発生）

---

### ステップ 5: 関連イシューをクローズする（ワークツリー内）

#### 条件

- ステップ 4 完了

#### 処理

1. ワークツリーの `.work/tasks/{date}_{title}/{branch-hyphenated}.md` から `## 関連イシュー` セクションを読む
2. **セクションが無い、空である、またはテンプレートプレースホルダー行（`| ISSUE-{N} | ... |`）のみを含む場合** → このステップの残りをスキップしてステップ 6 に進む
3. テーブルの各行について、ワークツリー内でクローズコマンドを実行:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/issue-tool.py" close \
  --issues-dir {WORKTREE_PATH}/.work/issues \
  --issue-id ISSUE-{NNN} \
  --resolution {resolved|wontfix} \
  --linked-pr {N}
```

   スクリプトの処理:
   - `.work/issues/ISSUE-{NNN}.md` を `.work/issues/closed/ISSUE-{NNN}.md` に移動
   - `_index.yaml`（gitignore対象 — コミット不要）から該当エントリを削除
   - `_index.archive.yaml` に `linked_pr` 付きで `closed_issues` エントリを追記
4. プロジェクトに `.work/issues/` が存在しない場合（イシュー管理未導入）、スクリプトはスキップメッセージを出力 — no-op として扱う
5. ワークツリー内で変更をコミット:

```bash
git -C {WORKTREE_PATH} add .work/issues/
git -C {WORKTREE_PATH} commit -m "chore: close related issues for #{N}"
```

→ ステップ 6 に進む

#### 補足

- イシューファイルの移動は git の名前変更として追跡される。`_index.yaml` は gitignore のまま
- このコミットはステップ 8 の `--no-ff` マージに含まれる
- イシュー行が処理されなかった場合、空コミットを作成しないこと

##### set-completed / archive より前に実行する理由

このステップを `set-completed` / `archive` より **前** に実行することで、イシュークローズコミットが PR ブランチ上に留まり（意味的にはここに属する変更）、index 管理コミットと混在しないようにします。

---

### ステップ 6: index.yaml でブランチを完了済みにマーク

#### 条件

- ステップ 5 完了

#### 処理

1. 以下を実行して、メインリポジトリの `index.yaml` でエントリを `completed: true` にマーク:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py" set-completed \
  .work/tasks/index.yaml --id {N}
```

→ ステップ 7 に進む

#### 補足

- **メインリポジトリディレクトリで実行する**（ワークツリーではない） — `index.yaml` は gitignore 対象のためワークツリーに存在しない
- `index.yaml` 自体のコミットは不要

---

### ステップ 7: 完了済みエントリを archive する

#### 条件

- ステップ 6 完了

#### 処理

1. 以下を実行して、完了済みエントリを **ワークツリーの** `index.archive.yaml` に移動:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py" archive \
  .work/tasks/index.yaml \
  {WORKTREE_PATH}/.work/tasks/index.archive.yaml
```

コマンドは移動エントリ数を出力。`0` が出力された場合はこのステップの残りをスキップ。

2. エントリが移動された場合、ワークツリー内で `index.archive.yaml` をコミット:

```bash
git -C {WORKTREE_PATH} add .work/tasks/index.archive.yaml
git -C {WORKTREE_PATH} commit -m "chore: archive #{N} to index.archive.yaml"
```

→ ステップ 8 に進む

#### 補足

- `index.yaml` は gitignore 対象 — コミット不要
- `index.archive.yaml` は git 追跡対象 — **ブランチ内にコミット**（親ブランチに直接コミットしない）。ステップ 8 の --no-ff マージに含まれる
- archive コマンドはメインリポジトリの `index.yaml` から読み込み、ワークツリーの `index.archive.yaml` に書き込む

---

### ステップ 8: マージを実行

#### 条件

- ステップ 7 完了

> ⚠️ **マージ前の必須確認**
> ステップ 7 でワークツリー内の `index.archive.yaml` をコミット し忘れたままマージを実行すると、archive の変更がマージコミットに含まれません。
> **マージコマンドを実行する前に、ステップ 7 のワークツリー内 `git commit` が完了していることを確認してください。**
> （ステップ 7 が 0 エントリ移動を報告した場合、このチェックはスキップしてもよい。）

#### 補足

##### 禁止事項

> このスキルが現在のメッセージでユーザーによって **最近呼び出された場合のみ** マージしてください。前のターンのスキルコンテキストが残っているだけの場合（現在のメッセージで呼ばれていない）、マージしないこと — 前回の呼び出し許可は引き継がれません。

#### 処理

1. 現在のブランチが親ブランチ（例: `master` から発散した場合は `master`、`develop` から発散した場合は `develop`）であることを確認
2. `--no-ff` でマージ:

```bash
git merge --no-ff -m "{type}: {title} #{N}" {BRANCH_NAME}
```

   `{BRANCH_NAME}` は実際のブランチ名（新形式: `{type}/{title}`、レガシー形式: `PR{N}/{type}/{title}`）。

→ ステップ 9 に進む

---

### ステップ 9: ワークツリーとブランチを削除

#### 処理

1. ワークツリーとブランチを削除:

```bash
git worktree remove {WORKTREE_PATH}
git branch -d {BRANCH_NAME}
```

→ ステップ 10 に進む

#### 補足

##### 禁止事項

- ワークツリーのルートで `Remove-Item -Recurse` や `rm -rf` を実行しないこと

---

### ステップ 10: QA エントリを確認

#### 処理

1. ブランチドキュメント（`.work/tasks/{date}_{title}/{branch-hyphenated}.md`）の `## QA` セクションを確認し、未解決エントリがあればユーザーに確認
2. 変更があればコミット:

```bash
git add .work/
git commit -m "docs: post-merge update for #{N}"
```

→ ステップ 11 に進む

---

### ステップ 11: マージ完了を報告

#### 処理

1. ユーザーにマージ完了を報告
   - マージされたブランチ名、内部 ID、タスクフォルダを含める

→ ステップ 12 に進む

---

### ステップ 12: 次ブランチ候補を pr-handoff に委譲

#### 条件

- `WORKSPACE_MERGE_AUTO_HANDOFF` が `false`/`0`/`no`/`off` でない（デフォルト: 有効）。無効の場合 → このステップをスキップしてステップ 13 に進む

#### 処理

1. マージされたブランチドキュメントを読み、`## 次ブランチ候補` セクションを確認
2. **次ブランチ候補が存在する場合**: `/workspace:pr-handoff` を呼び出す（ユーザー確認不要）。分類と予約のロジックはすべて pr-handoff に委譲
3. **次ブランチ候補が空の場合**: pr-handoff をスキップ

→ ステップ 13 に進む

---

### ステップ 13: 次ブランチ候補を 3 カテゴリで提示

#### 処理

マージされたブランチドキュメントパスを指定して `/workspace:pr-show` を呼び出す。

#### 補足

`## 次ブランチ候補` テーブルの読み込み、各候補のカテゴリ判定、タイトルによるブランチ検索の詳細なロジックは `pr-show` スキルで定義されています。
