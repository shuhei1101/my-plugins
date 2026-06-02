# ISSUE-136: dev-kit: _index.yaml に JP mirror ファイル（E2Eテスト.jp.md）が誤登録

**作成日**: 2026-06-02

# ユーザー回答欄

> 各 `**回答**:` 行で不要な選択肢を消して 1 つだけ残す。

## 意思

このイシューに対応するか。

**回答**: 対応する / 対応しない / 様子見

---

## 概要

`plugins/dev-kit/references/.ref-inject/_index.yaml` に `next/testing/E2Eテスト.jp.md` がエントリとして登録されている。JP mirror は注入対象でなく、`_index.yaml` には EN ファイルのみを登録するという規約に反する。同じ `_index.yaml` に `.jp.md` が登録されているエントリはこの 1 件のみ。

## 背景

`_index.yaml` はフック (`inject_references.py`) が参照するリファレンス一覧で、EN ファイルのパスと説明を管理する。JP mirror は `_index.jp.yaml` 側で管理し、EN のインデックスに混在させないのが規約である。

## 現状

`_index.yaml` の行 391–393:
```yaml
- path: next/testing/E2Eテスト.jp.md
  lang: next
  description: JP mirror of E2Eテスト.md
```

`next/testing/E2Eテスト.jp.md` はディスクに存在するが（10427 bytes）、このエントリが注入フックに読み込まれると JP mirror が `required`/`optional` の候補として扱われうる。

## 原因

`E2Eテスト.jp.md` 追加時に誤って `_index.yaml` に記入した可能性がある。

## 期待される状態

`_index.yaml` の `E2Eテスト.jp.md` エントリが削除され（必要なら `_index.jp.yaml` に移動され）、EN エントリのみが `_index.yaml` に残っていること。

## 対応案

`_index.yaml` 行 391–393 の `E2Eテスト.jp.md` エントリを削除する。`_index.jp.yaml` を確認し、JP mirror の記述が欠けていれば追加する。
