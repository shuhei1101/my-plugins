# ISSUE-135: dev-kit: references/ ルート直下に マークダウン編集.md の重複ファイルが残存

**作成日**: 2026-06-02

# ユーザー回答欄

> 各 `**回答**:` 行で不要な選択肢を消して 1 つだけ残す。

## 意思

このイシューに対応するか。

**回答**: 対応する / 対応しない / 様子見

---

## 概要

`plugins/dev-kit/references/マークダウン編集.md`（ルート直下）が `plugins/dev-kit/references/markdown/マークダウン編集.md`（`markdown/` サブフォルダ）と完全に同一内容で残存している。ルート直下のファイルはどのパターンにもバインドされていない孤立ファイルであり、`_index.yaml` にも未登録。

## 背景

dev-kit v4.7.0 (PR198) で `markdown/` サブフォルダが新設され `マークダウン編集.md` が移動した際、移動元ファイルが削除されずに残ったと推測される。

## 現状

- `plugins/dev-kit/references/マークダウン編集.md` — 546 bytes、孤立（`_index.yaml` 未登録・パターン未バインド）
- `plugins/dev-kit/references/markdown/マークダウン編集.md` — 546 bytes、`_index.yaml` の `markdown/マークダウン編集.md` として登録済み・パターン `**/*.md` にバインド済み

`diff` の結果、2 ファイルは完全一致（Exit code 0）。JP mirror ファイル（`マークダウン編集.jp.md`）もルート直下に残存している。

## 原因

ファイル移動時にソースファイルの削除が漏れた。

## 期待される状態

ルート直下の `マークダウン編集.md` と `マークダウン編集.jp.md` が削除され、`markdown/` 配下のファイルのみが残っていること。

## 対応案

`plugins/dev-kit/references/マークダウン編集.md` と `plugins/dev-kit/references/マークダウン編集.jp.md` を削除する（1 コマンドで完結）。
