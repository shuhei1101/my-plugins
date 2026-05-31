# fix/merge-skill-branch-first

> 内部 ID: 240（index.yaml 採番用 — クロスリファレンス目的）

## 概要

`work:merge` スキルの Step 3 で、`git merge <PARENT_BRANCH>` を実行するディレクトリが明示されていないため、Claude がマスターリポジトリのコンテキストから実行してしまうことがある。その場合 `git merge master` が master 上での no-op となり、Step 7 で `git merge --no-ff <feature-branch>` を実行した際にコンフリクトが master に流れ込む問題を修正する。

Step 3 の git コマンドに `git -C {WORKTREE_PATH}` プレフィックスを追加し、ワークツリー（フィーチャーブランチ）上で実行されることを明示する。

### 実施条件

即時実施可

## 作業内容

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | 済 | QA を `## QA` に記録 |
| 2 | 済 | ノートドキュメントを更新 |
| 3 | 済 | Step 3 の git コマンドに `git -C {WORKTREE_PATH}` を追加して実行コンテキストを明示 |
| 4 | 済 | ルール / CLAUDE.md 更新（変更なし） |

## 変更内容

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | `plugins/work/skills/merge/SKILL.md` | 編集 | Step 3 の git コマンドにワークツリーパスを明示 | - |
| 2 | `plugins/work/skills/merge/SKILL.jp.md` | 編集 | 同上の日本語ミラー | - |

## テスト

| # | ファイル名 | 新規/編集 | 内容 | 補足 |
|---|---|---|---|---|
| 1 | — | — | テストファイルなし | — |

## QA

なし

## 参考ドキュメント

- `plugins/work/skills/merge/SKILL.md`: 変更対象のマージスキル
- `.work/tasks/260531_merge-skill-force-master-sync/feat-merge-skill-force-master-sync.md`: 関連の先行ブランチドキュメント

## 関連ブランチ

| # | ブランチ | 概要 |
|---|---|---|
| 1 | feat/merge-skill-force-master-sync | Step 3 必須化の先行修正 |

## 次ブランチ候補

| # | タイトル | 概要 | 実施条件 |
|---|---|---|---|
| 1 | — | — | — |
