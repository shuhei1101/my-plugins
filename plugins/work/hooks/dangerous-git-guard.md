# 危険な git コマンド: ブロック

以下の git コマンドは事故誘発につながるため永久ブロックされています。

- `git worktree remove --force` / `-f` — 作業中ワークツリーを強制削除して in-progress 作業が消える
- `git rm .gitignore` / `git rm .gitattributes` / `git rm .claude/...` — 重要ファイルの追跡削除
- `git checkout -- .gitignore` 等 — 重要ファイルの上書き復元
- `git merge -X ours/theirs` / `--strategy-option=ours/theirs` — 自動コンフリクト解消（master 側追加ファイル誤削除の原因）
- `git checkout --ours/--theirs` — 同上

このブロックは解除できません。コンフリクトは手動で個別に解消し、`git status -s` で全体を確認してください。
