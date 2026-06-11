---
name: work:merge
description: ブランチマージするスキル。「マージして」っていったら起動
---

# merge — ブランチをマージ

## タスク

### ステップ 1: マージするブランチを特定

1. マージするブランチが現在の会話セッション内で既に特定されている場合、それを使用して Step 2 に進みます
2. それ以外の場合、ユーザにどのブランチをマージするか聞く

### ステップ 2: タスクチェックリストを検証

- `.work/tasks/{date}_{title}/{YYMMDD}-{日本語タイトル}.task.md` のタスクドキュメントを読む
- `## 作業内容` テーブルを読み込みすべての行の `完了` 列に `済` があることを確認
  - すべての行が `済` の場合、次に進む。
  - 未完了の行が残っている場合、マージを実行せず作業を続行

### ステップ 3: 関連イシューをクローズ

- ワークツリーの `.work/tasks/{date}_{title}/{YYMMDD}-{日本語タイトル}.task.md`を読む
  - タスクドキュメントの `## 関連イシュー` セクションを読み込み
- テーブルの各行について、ワークツリー内 で以下クローズコマンドを実行
```bash
python "/home/shuhei2441/.claude/work-scripts/issue-tool.py" close \
  --issues-dir {WORKTREE_PATH}/.work/issues \
  --issue-id ISSUE-{NNN} \
  --resolution {resolved|wontfix} \
  --linked-branch {BRANCH_NAME}
```

- 変更内容を現在の作業ブランチでコミットする

### ステップ 4: index.yaml で完了とマーク

メインリポジトリ ディレクトリから実行してください（ワークツリーではなく） — `index.yaml` は gitignored で、メインリポのみに存在。コミットは不要。
```bash
python "/home/shuhei2441/.claude/work-scripts/index-tool.py" set-completed \
  .work/tasks/index.yaml --branch {full-branch-name}
```

### ステップ 5: 完了したインデックスエントリをアーカイブ

1. 以下のコマンドを実行して、完了したエントリを ワークツリーの `index.archive.yaml`
   に移動します（メインリポの `index.yaml` から読み込み、ワークツリーの `index.archive.yaml` に書き込み）：
```bash
python "/home/shuhei2441/.claude/work-scripts/index-tool.py" archive \
  .work/tasks/index.yaml \
  {WORKTREE_PATH}/.work/tasks/index.archive.yaml
```
2. エントリが移動された場合、ワークツリー内の `index.archive.yaml` をコミット

### ステップ 6: マージ先ブランチをこのブランチに取り込む（ワークツリー内）
コンフリクトが master 上に流れ込むことを防止するため、先にマージ先ブランチを現在のブランチに取り込む
```bash
git -C {WORKTREE_PATH} merge <PARENT_BRANCH>
```
- コンフリクトなし → 次に進む
- コンフリクトあり → 解消する（極力最新コミットの内容をくみ取りAI側で自動で解消すること）

### ステップ 7: マージを実行
1. 現在のブランチがこのブランチが分岐した親ブランチであることを確認します
   （例えば master から分岐した場合は `master`、develop から分岐した場合は `develop`）
2. `--no-ff` でマージ：
```bash
git merge --no-ff -m "{type}: {title}" {BRANCH_NAME}
```

### ステップ 8: ワークツリーとブランチを削除
```bash
git worktree remove {WORKTREE_PATH}
git branch -d {BRANCH_NAME}
```

### ステップ 9: 次ブランチ候補を予約する

- マージされたタスクドキュメントを読み込み、その `## 次ブランチ候補` セクションを確認
   - 次ブランチ候補が存在する場合：`/branch-reserve`スキル を実行
   - 次ブランチ候補が空の場合: branch-reserve をスキップ
