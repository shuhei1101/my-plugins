# issue-resolver ワークツリー未作成バグ修正

> ブランチ: fix/issue-resolve-worktree-bug

## 概要

`work:issue-resolver` エージェントが `git worktree add` でワークツリーを作成せず、メインリポジトリ上に直接ブランチを切ってコミットしてしまうバグを修正する。

### 実施条件

即時実施可

## 作業内容

| # | タスク | 状態 |
|---|---|---|
| 1 | `issue-resolver.md` のワークツリー作成手順を明確化・具体化 | 済 |
| 2 | `issue-resolver.jp.md` を英語版に合わせて更新 | 済 |
| 3 | QA を記録する | 済 |
| 4 | ノートを更新する | 済 |

## 変更内容

| # | ファイル | 変更内容 |
|---|---|---|
| 1 | `plugins/work/agents/issue-resolver.md` | Procedure を2ディレクトリモデルで書き直し、`git worktree add` 必須・`git checkout` 禁止を明記 |
| 2 | `plugins/work/agents/issue-resolver.jp.md` | 英語版に合わせて JP ミラーを同期更新 |

## テスト

| # | 項目 | 結果 |
|---|---|---|
| - | - | - |

## QA

（なし）

## 参考ドキュメント

- [issue-resolverワークツリー未作成バグ.md](../../notes/バグ・不具合/issue-resolverワークツリー未作成バグ.md)

## 関連ブランチ

（なし）

## 次ブランチ候補

（なし）
