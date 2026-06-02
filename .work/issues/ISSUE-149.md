# ISSUE-149: _index.yaml に .jp.md ファイル（E2Eテスト.jp.md）が誤って登録されている

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/dev-kit/references/.ref-inject/_index.yaml`（EN 側）に `next/testing/E2Eテスト.jp.md` という JP ミラーファイルのパスが直接登録されている。JP ミラーは人間参照用で AI 注入対象外のはずであり、`_index.yaml` に含めるべきではない。

```yaml
- path: next/testing/E2Eテスト.jp.md
  lang: next
  description: JP mirror of E2Eテスト.md
```

`_index.jp.yaml` には同エントリなし（非対称）。`E2Eテスト.md`（英語ソース）のエントリはその直前に正しく存在するため、機能的には重複エントリに近い状態となっている。

## 対応方針

`_index.yaml` から `next/testing/E2Eテスト.jp.md` のエントリ（3 行）を削除する。`_index.jp.yaml` への変更は不要（そちらには既に存在しない）。

## 対象ファイル

- `plugins/dev-kit/references/.ref-inject/_index.yaml`: JP ミラーパスのエントリを削除

