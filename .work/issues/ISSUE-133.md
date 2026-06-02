# ISSUE-133: dev-kit: next/frontend/url-state.md と python/scripts/launchers-windows.md の英語ファイル本体が欠落

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

## QA

### QA-1: どの案で進めるか

A) JP mirror (.jp.md) から逆翻訳して EN ファイルを復元する / B) injection_rules / _index.yaml から参照を削除し、JP mirror も削除する

**推奨**: A — JP mirror は存在しており内容が確認できるため、EN ファイルを復元する方がリファレンスとして活用できる

- [x] A
- [ ] B


---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 概要

`_injection_rules.yaml` と `_index.yaml` に登録されている 2 つの英語リファレンスファイルが実際には存在しない。JP mirror ファイル（`.jp.md`）は残っているが EN 本体が欠落しており、注入実行時にファイル読み込みエラーが発生する。

## 背景

インシデント `orphan-references-not-checked`（No.2）と同一原因。JP mirror のみが残り EN ファイルが消えたケースで、通常の orphan チェックでは検出されにくい（`_index.yaml` には登録されているため）。

## 現状

以下のファイルが `_injection_rules.yaml`・`_index.yaml` に登録されているがディスクに存在しない:

| 参照パス | 状態 | JP mirror |
|---|---|---|
| `next/frontend/url-state.md` | **欠落** | `url-state.jp.md` は存在（8794 bytes） |
| `python/scripts/launchers-windows.md` | **欠落** | `launchers-windows.jp.md` は存在（5480 bytes） |

`url-state.md` は `_injection_rules.yaml` 行 515（`**/hooks/use*UrlState.ts` パターンの optional）、`launchers-windows.md` は行 180（`**/*.bat` パターンの required）で参照されている。

## 原因

ファイルの誤削除または命名変更ミスにより EN ファイルが消失したと推測される。

## 期待される状態

両 EN ファイルが存在し、`_injection_rules.yaml` / `_index.yaml` の参照と一致していること。

## 対応案

A 案（推奨）: JP mirror の内容をもとに EN ファイルを復元する。`url-state.jp.md` は 8794 bytes の実質的なコンテンツを持つため翻訳コストは低い。

B 案: EN ファイルの復元が困難な場合、`_injection_rules.yaml` / `_index.yaml` / `_index.jp.yaml` から参照を削除し、JP mirror も整理する。
