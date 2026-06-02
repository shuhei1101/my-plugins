# issue-resolver ワークツリー未作成バグ — 原因と修正

## 現象

`work:issue-resolve` + `/loop` でイシューを消化すると、`issue-resolver` サブエージェントが
ワークツリーを作成せずメインリポジトリ上にブランチを切り、直接コミットしてしまう。
メインリポジトリの HEAD が master を離れ、他のワークツリー操作と競合する。

## 根本原因

`issue-resolver.md` の Procedure セクションのステップ2が曖昧だった。

- `git worktree add` を使うとは書いていたが、ワークツリーパス変数（`WT`）の定義がなかった
- ステップ2以降の全操作をワークツリーで行う旨が明記されていなかった
- `git checkout` / `git switch -c` の禁止が明示されていなかった
- 「`work:start` スキルフローに従う」という記述が残っており、`Skill` ツールを持たないエージェントが混乱する余地があった

## 修正内容

`issue-resolver.md` および `issue-resolver.jp.md` の Procedure セクションを書き直し：

- **2ディレクトリモデル**を冒頭の callout で明記（`MAIN_DIR` = メインリポジトリ、`WT` = ワークツリー）
- ステップ2を具体的なシェルコマンド付きサブステップ（a〜e）に分解
- `git worktree add -b "$BRANCH" "$WT"` を明示し、`git checkout` / `git switch -c` を禁止
- ステップ2d以降は全 Write/Edit・git コマンドを `$WT` で実行することを明文化

## 変更履歴

| # | 日付 | 概要 |
|---|---|---|
| 1 | 2026-06-02 | 初版作成（fix/issue-resolve-worktree-bug） |
