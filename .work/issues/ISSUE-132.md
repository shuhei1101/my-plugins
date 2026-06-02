# ISSUE-132: dev-kit: python/architecture 配下の 2 ファイル名変更後に injection_rules / _index.yaml が未更新

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

## QA

### QA-1: どの案で進めるか

A) YAML の参照パスを実在するファイル名（依存関係管理.md / 設計原則.md）に書き換える / B) ファイルを旧名（依存パッケージ管理.md / design-基本方針.md）に戻す

**推奨**: A — ディスク側のファイル名が正規化済みのため YAML を追随させる方が自然

- [ ] A
- [ ] B


---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 概要

`python/architecture/` 配下の 2 ファイルがリネームされたが、`_injection_rules.yaml` と `_index.yaml` の参照が旧名のまま残っている。対象ファイル編集時にリファレンスが注入されない。

## 背景

インシデント `orphan-references-not-checked`（No.2）と同一原因。ファイル名変更後に YAML の突合チェックが実施されなかった。

## 現状

`plugins/dev-kit/references/.ref-inject/_injection_rules.yaml` の以下パスが存在しないファイルを指している:

| YAML の参照パス (存在しない) | ディスクの実ファイル名 |
|---|---|
| `python/architecture/依存パッケージ管理.md` | `python/architecture/依存関係管理.md` |
| `python/architecture/design-基本方針.md` | `python/architecture/設計原則.md` |

`_injection_rules.yaml` での参照箇所:
- `python/architecture/依存パッケージ管理.md`: 行 54, 70, 109（3 箇所、`main.py` / `features/**/service.py` / `integrations/**/client.py` パターン）
- `python/architecture/design-基本方針.md`: 行 55, 72（2 箇所、`main.py` / `features/**/service.py` パターン）

`_index.yaml` でも行 31–37 が旧名を登録している。

注意: `python/packaging/依存パッケージ管理.md`（別の「パッケージ依存管理」ファイル、行 172）は実在しており、今回の問題とは別。`python/architecture/依存パッケージ管理.md` は `python/architecture/依存関係管理.md` にリネームされたものと考えられる。

## 原因

ファイルリネームコミット時に `_injection_rules.yaml` / `_index.yaml` / `_index.jp.yaml` の更新が漏れた。

## 期待される状態

`_injection_rules.yaml` の 5 箇所（行 54, 55, 70, 72, 109）と `_index.yaml` の 2 エントリが正しいファイル名に更新されていること。

## 対応案

`_injection_rules.yaml`・`_index.yaml`・`_index.jp.yaml` の該当 path を一括置換する。対応後は `python3 -c "import yaml; yaml.safe_load(open(...))"` でパースが通ることを確認。
