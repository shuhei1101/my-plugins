# protected-branch-guard — 保護ブランチへの直接ファイル編集をブロック

## 概要

PreToolUse フックとして動作し、`Edit` / `Write` ツール呼び出し時に対象ファイルが属する git ブランチを確認する。`main` / `master` / `develop` への直接編集をブロックし `/work:start` の使用を促す。

## ブランチ判定ロジック

`resolve_check_dir` でファイルパスの祖先ディレクトリを辿り、最初に存在するディレクトリで `git branch --show-current` を実行する。

- 新規ファイル作成時（親ディレクトリが未存在）でも正しいワークツリーのブランチを検出できる
- 存在するディレクトリが見つからない場合は `cwd` にフォールバック

## 注意事項

- 保護対象: `{"main", "master", "develop"}`
- 保護ブランチ以外はすべて通過（ワークツリー内の作業ブランチは問題なし）

## 参考リンク

- `plugins/work/hooks/protected-branch-guard.py`: フックスクリプト本体
