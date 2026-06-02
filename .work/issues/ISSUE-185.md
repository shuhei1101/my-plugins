# ISSUE-185: dev-kit の plugin.json description が marketplace.json より古い（v4.13.0 記述欠落）

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`dev-kit` の `plugin.json` の `description` と `marketplace.json` の対応エントリの `description` が一致していない。バージョン自体は両ファイルともに一致しているが、`plugin.json` 側が `v4.13.0` のチェンジログ追記（`remove setup-wizard skill and SessionStart hook`）を受け取っていない。

オーサリングガイドでは `plugin.json` の description 変更時は `marketplace.json` 側も同期することが要求される。現状は marketplace.json 側が新しく、plugin.json 側が古い。

注: スキャン時点の値であり、対応着手時に最新差分を再確認すること。

## 対応方針

`plugin.json` の description 末尾に欠落している `v4.13.0` のサフィックスを追記して marketplace.json と揃える。

## 対象ファイル

- `plugins/dev-kit/.claude-plugin/plugin.json`: description 末尾に `v4.13.0` のサフィックスを追加
