# ISSUE-200: dev-kit _index.yaml の next/testing/E2Eテスト.md の EN/JP description に実質的な内容差異

**作成日**: 2026-06-03

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/dev-kit/references/.ref-inject/_index.yaml`（EN）と `_index.jp.yaml`（JP）の `next/testing/E2Eテスト.md` エントリで、description の内容が翻訳差異を超えた実質的な齟齬がある。

**EN description（現状）**: 古いフォルダ構成（`tests/e2e/`・`tests/pages/`・`tests/helpers/`）を参照
**JP description（現状）**: より新しい構成（`ユースケース駆動設計（scenarios/）`・`utils/data 責務分離`）を記述

どちらかが実際のリファレンスファイル（`E2Eテスト.md`）の内容と乖離している。

## 対応方針

1. `plugins/dev-kit/references/next/testing/E2Eテスト.md` の実際の内容を確認して正しい description を特定する
2. EN と JP の両 description を同じ内容に統一する（JP は EN の翻訳として保つ）

## 対象ファイル

- `plugins/dev-kit/references/.ref-inject/_index.yaml`: `E2Eテスト.md` の description を実ファイルに合わせて修正
- `plugins/dev-kit/references/.ref-inject/_index.jp.yaml`: 上記の日本語訳として統一
