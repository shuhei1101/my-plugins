# ISSUE-142: dev-kit の plugin.json description が marketplace.json より古い（v4.11.1 で止まっている）

**作成日**: 2026-06-02

## 概要

`plugins/dev-kit/.claude-plugin/plugin.json` の `description` フィールドが `v4.11.1` の変更記述で終わっており、`v4.13.0` 以降の変更（setup-wizard 削除、plugin-config 削除と復元）が反映されていない。一方 `.claude-plugin/marketplace.json` の同エントリは `v4.13.0` まで含んだより新しい本文になっており、両ファイルの description が乖離している。

## 背景

`plugin.json` と `marketplace.json` の description は同一内容を保つべきである。version は双方とも `4.15.0` で一致しているが、description が異なるため、`plugin.json` 単体を読んだ場合に最新の変更履歴が確認できない。

## 現状

**`plugins/dev-kit/.claude-plugin/plugin.json`** の description 末尾:
```
... v4.11.1: remove redundant branch-check step from plugin-migrate.
```
（v4.12.0 以降の記述が存在しない）

**`.claude-plugin/marketplace.json`** の dev-kit エントリの description 末尾:
```
... v4.13.0: remove setup-wizard skill and SessionStart hook.
```
（v4.13.0 までは含まれているが、v4.14.0・v4.15.0 の変更は marketplace.json にも未記載）

実際の最新変更（CLAUDE.md の Changelog より）:
- v4.14.0: dev-kit:plugin-config スキル削除 + 環境変数テーブル形式統一
- v4.15.0: dev-kit:plugin-config スキル復元

つまり plugin.json は v4.11.1 止まり、marketplace.json は v4.13.0 止まりで、両者とも最新の v4.15.0 の状態と一致していない。

## 原因

バージョンアップ時に `plugin.json` の description を更新せず、`marketplace.json` 側のみ部分的に更新したため乖離が生じた。どちらも v4.15.0 には追いついていない。

## 期待される状態

`plugin.json` と `marketplace.json` の dev-kit description が同一の本文を持ち、かつ現バージョン（v4.15.0）時点の変更履歴まで含んでいる。

## 対応案

`plugins/dev-kit/.claude-plugin/plugin.json` の description を `marketplace.json` の本文に合わせた上で、v4.14.0・v4.15.0 の変更行を両ファイルに追記して揃える。

---

# ユーザー回答欄

> 各 `**回答**:` 行で不要な選択肢を消して 1 つだけ残す。

## 意思

このイシューに対応するか。

**回答**: 対応する / 対応しない / 様子見
