<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# master 直接編集によるマージ競合

**Date**: 2026-05-21
**Category**: wrong-assumption

## What Happened

`SKILL.jp.md` と `SKILL.md` を修正しようとした際、`work-start` でワークツリーを
作成する前に `master` ブランチ上でファイルを直接編集してしまった。その後、
同じファイルをワークツリー内で正しく編集して `git merge --no-ff` を実行しようとしたところ、
master 側に未コミットの変更が残っていたため競合が発生した。
対処は `git restore <files>` で master 側の変更を破棄することだった。

## How to Avoid

master でファイルを編集しない。必ず `/work-kit:work-start` を先に実行して
ワークツリーとブランチを作成し、すべての変更はワークツリー内で行う。
UserPromptSubmit フックでこれは強制されているが、「小さな修正だから」という
思い込みでチェックを飛ばしてしまうことがある。

## Context

`my-plugins` リポジトリに適用。ワークツリーは `../my-plugins-wt-PR{N}` に作成され、
ブランチ名は `PR{N}/{type}/{title}`。
