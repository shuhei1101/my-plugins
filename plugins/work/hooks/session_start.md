[work] 現在のプロジェクトでは work プラグインが有効になっています。以下の規約に従ってください。

## 作業フロー

1. 実装・修正の依頼を受けたら `/work:start` を実行する（質問・調査のみなら不要）
2. ワークツリー内で実装し、タスクドキュメントを更新する
3. 完了したら `/work:merge` を提案し、ユーザー承認後にマージする

## やってはいけないこと

以下は常時ブロックされています。ブロックされたら原因を確認してから対処すること（無確認の再実行は禁止）。

- `master` / `main` / `develop` ブランチに直接コミットしないこと（マージコミットのみ可）
- `master` / `main` / `develop` ブランチ上で直接ファイルを Edit / Write しないこと（`/work:start` でワークツリーを作る）
- `master` / `main` / `develop` ブランチ上で work プラグインの `index-tool.py` / `issue-tool.py` / `trim-index.py` を実行しないこと（worktree から呼ぶ）
- `.git/` 配下のファイルを Edit / Write / `rm` / `rmdir` しないこと（Git CLI 経由でのみ操作）
- `.gitignore` / `.gitattributes` を Edit / Write / `rm` / `rmdir` しないこと（ユーザー手動でのみ更新）
- `.claude/` ディレクトリを `rm` / `rmdir` しないこと
- パッケージマネージャの lock ファイル（`package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` / `npm-shrinkwrap.json` / `Cargo.lock` / `Gemfile.lock` / `Pipfile.lock` / `poetry.lock` / `uv.lock` / `composer.lock` / `go.sum`）を Edit / Write / `rm` しないこと（CLI 経由で再生成）
- `git worktree remove --force` / `--force` 付き worktree 削除をしないこと
- `git merge` に `-X ours` / `-X theirs` / `--strategy-option=ours/theirs` を渡さないこと
- `git rm` で `.git` / `.claude` / `.gitignore` / `.gitattributes` / lock ファイル等の重要ファイルを消さないこと
- `git push` / `git merge` 実行時に表示される確認は読まずに再実行しないこと（一度ブロックされる仕様。再実行前に意図を再確認する）
- master へのマージ前に `pre-merge-check` で出る master 取り込み・コンフリクト確認をスキップしないこと

## 補足

- `master/main/develop` への直接コミットでブロックされる典型原因は cwd ずれ。`git -C {ワークツリーパス}` 形式で実行し直す
- 直近コミットで N 件以上のファイル削除があると Stop フックで警告コンテキストが注入される（実害がなければ続行可）

## 規約

- メインリポジトリは常に master を踏んだ状態を維持し、ブランチ作業は必ずワークツリー（`.claude/worktrees/` 配下）で行う
- シェルの cwd はコマンドごとにリセットされることがあるため、ワークツリー内での git 操作は `git -C {ワークツリーパス}` 形式を使う
