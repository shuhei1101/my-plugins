# ISSUE-131: dev-kit: conventions/ ファイル名変更後に _injection_rules.yaml / _index.yaml が未更新（3 ファイル）

**作成日**: 2026-06-02

# ユーザー回答欄

> 各 `**回答**:` 行で不要な選択肢を消して 1 つだけ残す。

## 意思

このイシューに対応するか。

**回答**: 対応する

## QA

### QA-1: どの案で進めるか

A) injection_rules / _index.yaml の参照パスを新しいファイル名（命名規約・コメント規約・型規約）に書き換える / B) ファイル名を旧名（命名規則・コメント・型定義）に戻す

**推奨**: A — ファイル名の日本語化リファクタリングは完了済みで新名が正しい状態のため、YAML 側を追随させる方が自然

**回答**: A / B

---

## 概要

`daff7d40` の「全 references ファイル名を日本語化」コミットで `conventions/` 配下のファイル名が変更されたが、`_injection_rules.yaml` と `_index.yaml` のパス参照が旧名のまま残っている。注入対象ファイルを編集しても参照先が存在しないため、3 ファイル分のリファレンスが一切注入されない。

## 背景

インシデント `orphan-references-not-checked`（No.2）：`_injection_rules.yaml` を編集した後は YAML とファイルシステムを突合する孤立チェックを実行し、紐づかない reference を残さないという規約がある。今回はファイル名変更時にこのチェックが行われなかった。

## 現状

`plugins/dev-kit/references/.ref-inject/_injection_rules.yaml` および `_index.yaml` の以下パスが存在しないファイルを指している:

| YAML の参照パス (存在しない) | ディスクの実ファイル名 |
|---|---|
| `next/frontend/conventions/命名規則.md` | `next/frontend/conventions/命名規約.md` |
| `next/frontend/conventions/コメント.md` | `next/frontend/conventions/コメント規約.md` |
| `next/frontend/conventions/型定義.md` | `next/frontend/conventions/型規約.md` |

`_injection_rules.yaml` では `命名規則.md` が 2 箇所（行 243, なし）、`コメント.md` が 2 箇所（行 244）、`型定義.md` が 3 箇所（行 245, 436）に誤参照が残っている。`_index.yaml` でも行 343–351 が旧名を登録。

## 原因

ファイルリネームコミット `daff7d40` で `.md` ファイルは改名されたが、`_injection_rules.yaml` / `_index.yaml` / `_index.jp.yaml` の更新が漏れた。

## 期待される状態

`_injection_rules.yaml` の 3 つの旧パス参照が新ファイル名（`命名規約.md` / `コメント規約.md` / `型規約.md`）に書き換えられ、`_index.yaml` / `_index.jp.yaml` のエントリも対応する新名に更新されていること。

## 対応案

`_injection_rules.yaml`、`_index.yaml`、`_index.jp.yaml` の該当 path 文字列を一括置換する。

## 横展開

同じリファクタリングコミットで変更されたと思われる他のパス（`python/architecture/依存パッケージ管理.md`、`python/architecture/design-基本方針.md`、`python/scripts/launchers-windows.md` など）も同様の乖離が発生している（別イシューとして立てている）。
