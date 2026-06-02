# dev-kit references ルート直下孤立ファイル

## 概要

`plugins/dev-kit/references/` ルート直下に `マークダウン編集.md` と `マークダウン編集.jp.md` が残存していた。これらは `markdown/` サブフォルダへのファイル移動時に削除が漏れた孤立ファイルである。

## 原因

dev-kit v4.7.0 (PR198) で `markdown/` サブフォルダが新設され `マークダウン編集.md` が移動した際、移動元（ルート直下）のファイルが削除されずに残った。

## 検証結果

- ルート直下と `markdown/` 配下のファイルは diff で完全一致（exit code 0）
- `_index.yaml` には `markdown/マークダウン編集.md` のみ登録、ルート直下は未登録

## 対処

ISSUE-135 (`fix/delete-dev-kit-orphan-references`) でルート直下の2ファイルを削除した。

## 教訓

ファイル移動時はソースファイルの削除を必ず確認する。`_index.yaml` と実ファイルシステムとの突合チェックを定期的に行うことで孤立ファイルを検出できる。
