[master-commit-guard] master/main/develop ブランチへの直接操作（git add / git commit）をブロックしました。再実行しても通りません。

対応方法:
- まず以下の git status と現在のディレクトリを確認し、なぜ保護ブランチ上で操作しようとしたのかを把握してください。
  - 多くの場合、cwd がワークツリーではなくメインリポジトリに戻っているのが原因です。`git -C {ワークツリーパス} add/commit` で実行し直してください。
- 作業ブランチが必要な場合は `git worktree add` でワークツリーを作成してから、そこで作業してください。
- 本当に保護ブランチへ直接操作する必要がある場合のみ、ユーザーに確認を取ったうえで
  `GUARD_KIT_ALLOW_MASTER_COMMIT=1 git add/commit ...` の形で実行してください。
