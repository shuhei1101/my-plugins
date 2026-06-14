# master-commit-guard — 保護ブランチへの直接操作を完全ブロック

## 概要

PreToolUse(Bash) フック。`master` / `main` / `develop` 上での `git add` / `git commit` を完全にブロックする（再実行しても通らない）。

## 通過する条件

| 条件 | 理由 |
|---|---|
| マージ中（`MERGE_HEAD` 存在） | コンフリクト解消ステージングとマージコミット完成を阻まない |
| env `WORK_ALLOW_MASTER_COMMIT` が truthy | 例外作業用の明示的な解除手段（ユーザー確認のうえ `WORK_ALLOW_MASTER_COMMIT=1 git add/commit ...`） |
| 非保護ブランチ | 対象外 |

保護ブランチは env `WORK_PROTECTED_BRANCHES`（カンマ区切り）で上書き可。

## ブロック時の挙動

- `git status` をブロック理由に添えて Claude に提示する
- 対応方法（cwd 確認・`git -C {ワークツリー}` での実行し直し・`/work:start`）をメッセージで案内する

## 参考リンク

- `plugins/work/hooks/master-commit-guard.py`: フック本体
- `plugins/work/hooks/master-commit-guard.md`: ブロック時メッセージ
