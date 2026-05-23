# merge-archive-step-zero-bug

## What happened

`work-kit:merge` スキルの archive ステップ（旧 Step 5）が常に 0 件を返し、`index.archive.yaml` が PR ブランチに含まれずマージ後に master 直接コミットになっていた。

## Root causes

### 原因 1: archive 実行前に `completed: true` が設定されていない

archive コマンドは `completed: true` のエントリのみを移動する。merge フロー内で `completed: true` を設定するステップが存在しなかったため、archive は常に 0 件を返していた。

### 原因 2: `index.yaml` は gitignored のためワークツリーに存在しない

git worktree は **git 追跡済みファイルのみ**をコピーする。gitignored ファイル（`index.yaml`）はワークツリーに存在しない。そのため、ワークツリーのパスで archive を実行しても入力ファイルが見つからない。

`index.yaml` はメインリポジトリのみに存在するローカルファイルである。

## Fix (PR86)

1. `index-tool.py` に `set-completed --id N` サブコマンドを追加
2. merge SKILL.md に **Step 4** を追加:
   - メインリポジトリで `set-completed` を実行し `completed: true` にセット
3. merge SKILL.md の **Step 5** を修正:
   - archive コマンドをメインリポジトリで実行
   - 書き込み先を `../$(basename $(pwd))-wt-PR{N}/.work/tasks/index.archive.yaml`（ワークツリーの追跡済みファイル）に変更
   - ワークツリー内で `git -C ...` でコミット → PR ブランチに含まれる

## General principle

**git worktree に gitignore ファイルは存在しない。** ワークツリー内で何かが「ない」と気づいたとき、gitignore されているかどうかを最初に確認すること。
