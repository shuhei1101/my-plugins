# ISSUE-150: references/ ルートに マークダウン編集.md / .jp.md の孤立コピーが残っている

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/dev-kit/references/マークダウン編集.md` と `plugins/dev-kit/references/マークダウン編集.jp.md` が `references/` ルートに残っている。これらは `markdown/` サブフォルダに移動されたものと同一内容のコピーであり、`_index.yaml` / `_injection_rules.yaml` には登録されておらず、孤立ファイルとなっている。

存在するファイル:
- `plugins/dev-kit/references/マークダウン編集.md` — `markdown/マークダウン編集.md` と内容一致
- `plugins/dev-kit/references/マークダウン編集.jp.md` — 同様

`_index.yaml` での登録: `markdown/マークダウン編集.md` のみ（ルートパスは未登録）。ルートのファイルはどのパターンにも紐づかない真の孤立ファイル。インシデント #2 (orphan-references-not-checked) の類型。

## 対応方針

ルートの `マークダウン編集.md` と `マークダウン編集.jp.md` を `git rm` で削除する。`_index.yaml` / `_injection_rules.yaml` の変更は不要（すでに `markdown/` パスが登録されている）。

## 対象ファイル

- `plugins/dev-kit/references/マークダウン編集.md`: 削除
- `plugins/dev-kit/references/マークダウン編集.jp.md`: 削除

