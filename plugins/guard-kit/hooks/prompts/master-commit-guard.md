master/main ブランチへの直接コミットが検出されました。

**ワークツリー内の PR ブランチでコミットしてください。**

正しいフロー:
1. `git worktree add` で PR ブランチのワークツリーを作成する
2. ワークツリー内でコミットする（`../repo-wt-PR{N}/` 内）
3. `git merge --no-ff` で master にマージする

再度コミットすると 1 回だけ許可されます（post-merge update など、やむを得ないケース用）。
