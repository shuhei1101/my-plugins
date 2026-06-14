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
- テーブルの各行について `issue_close` MCP ツール（work-tools サーバー）を実行:
  - issues_dir: `{WORKTREE_PATH}/.work/issues/progress` / issue_id: `ISSUE-{NNN}` / resolution: `resolved|wontfix` / linked_branch: `{BRANCH_NAME}`
- 変更内容を現在の作業ブランチでコミットする

### ステップ 4: index.yaml で完了とマーク

`index_set_completed` MCP ツール（work-tools サーバー）を実行する:
- branch: `{full-branch-name}`
- `index.yaml` は gitignored でメインリポのみに存在するため、コミットは不要

### ステップ 5: 完了したインデックスエントリをアーカイブ

1. `index_archive` MCP ツール（work-tools サーバー）を実行する:
   - archive_path: `{WORKTREE_PATH}/.work/tasks/index.archive.yaml`
   - メインリポの `index.yaml` から完了エントリを読み込み、ワークツリーの `index.archive.yaml` に移動する
2. エントリが移動された場合、ワークツリー内の `index.archive.yaml` をコミット

### ステップ 6: マージ先ブランチをこのブランチに取り込む（ワークツリー内）
コンフリクトが master 上に流れ込むことを防止するため、先にマージ先ブランチを現在のブランチに取り込む
```bash
git -C {WORKTREE_PATH} fetch origin <PARENT_BRANCH>
git -C {WORKTREE_PATH} merge origin/<PARENT_BRANCH>
```

#### コンフリクト時の取り扱い（AI 自身で解消）

コンフリクトが出たら **AI 自身で考えて安全に解消する**。ユーザーへ聞くのは最後の手段（ユーザーは状況の詳細を把握していない前提）。

手順:
1. `git status -s` でコンフリクトファイル一覧を取得し、左 2 文字（XY コード）で分類する
2. 種類別に **ファイル単位で判断**して解消する。代表的な判断指針:

| コード | 意味 | 基本方針 |
| --- | --- | --- |
| `UU` | 両側で変更 | 両ファイルを `Read` で読み、両方の意図を反映するようマージしてから `git add` |
| `AA` | 両側で追加 | 両側の内容を統合してから `git add` |
| `DD` | 両側で削除 | `git rm <file>` で削除確定 |
| `DU` | 自分側で削除 / 相手側で変更 | 基本は **相手側を採用**: `git checkout --theirs -- <file>` → `git add <file>`（自分のブランチが分岐後に master で追加されたファイルが「自分側で削除扱い」になっているだけのケースが大半。内容を `git show :3:<file>` で確認して判断） |
| `UD` | 自分側で変更 / 相手側で削除 | 自分の変更に意味があるか `git diff :2:<file>` で確認。残すなら `git checkout --ours -- <file>` → `git add`、不要なら `git rm <file>` |

3. 全ファイル解消したら `git status` で残りがないことを確認し `git commit`

禁止事項（事故の元なので必ず守る）:
- `-X ours` / `-X theirs` / `--strategy-option=ours/theirs` などの **一括自動解消は禁止**（ファイル単位で判断していないため master 側追加ファイルを誤削除する）
- **ファイル指定なし**の `git checkout --ours` / `git checkout --theirs` も禁止（一括解消相当）
- サブエージェントを起動してコンフリクト解消を委譲してはならない（自分のコンテキストで判断する）

最終手段（どうしても判断できないとき）:
- 当該ファイルの履歴を `git log --all --oneline -- <file>` で確認
- それでも判断できないファイルだけまとめて、`git status -s` の全行と各ファイルの 3-way 状態（`:1:`/`:2:`/`:3:`）を添えてユーザーに報告

### ステップ 7: マージを実行
1. 現在のブランチがこのブランチが分岐した親ブランチであることを確認します
   （例えば master から分岐した場合は `master`、develop から分岐した場合は `develop`）
2. `--no-ff` でマージ：
```bash
git merge --no-ff -m "{type}: {title}" {BRANCH_NAME}
```

### ステップ 8: ワークツリーとブランチを削除

`worktree_remove` MCP ツール（work-tools サーバー）を実行する:
- branch: `{BRANCH_NAME}`
- ワークツリーとブランチが削除され、Stop リマインダー用のセッショントークンも消える

### ステップ 9: 次ブランチ候補を予約する

- マージされたタスクドキュメントを読み込み、その `## 次ブランチ候補` セクションを確認
   - 次ブランチ候補が存在する場合：`/branch-reserve`スキル を実行
   - 次ブランチ候補が空の場合: branch-reserve をスキップ
