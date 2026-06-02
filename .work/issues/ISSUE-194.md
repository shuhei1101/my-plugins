# ISSUE-194: dev-kit の next/backend/ローカルYAML開発DB.md が _index.md（人間向け）に未掲載

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/dev-kit/references/.ref-inject/_index.yaml`（機械可読インデックス）には `next/backend/ローカルYAML開発DB.md` が登録されており、ファイルも実在するが、`plugins/dev-kit/references/_index.md`（人間向けインデックス）には掲載されていない。

人間が `_index.md` を見てリファレンスを探す際に、このファイルの存在に気づけない。

注: 同スキャンで検出された `E2Eテスト.jp.md` 誤登録は ISSUE-149/136、`url-state.md` 欠落は ISSUE-148/133 で既出のため、本イシューは `ローカルYAML開発DB.md` の `_index.md` 未掲載に絞る。

## 対応方針

`ローカルYAML開発DB.md` を `_index.md` の Next.js バックエンドセクションに追記する。

## 対象ファイル

- `plugins/dev-kit/references/_index.md`: `next/backend/ローカルYAML開発DB.md` のエントリを追記

