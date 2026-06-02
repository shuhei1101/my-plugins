# ISSUE-184: claude-kit / work の plugin.json バージョンが marketplace.json と乖離

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugin.json` の `version` フィールドと `marketplace.json` 内の対応エントリの `version` が一致していない。

- `plugins/claude-kit/.claude-plugin/plugin.json`: `3.56.0` ⇔ marketplace.json: `3.55.0`
- `plugins/work/.claude-plugin/plugin.json`: `2.74.0` ⇔ marketplace.json: `2.73.0`

プラグインのオーサリングガイド（`プラグイン構造.md`）では `plugin.json` / `marketplace.json` / `CLAUDE.md` の 3 ファイルは常に同一バージョンを保つことが必須とされている。

注: スキャン時点の値であり、対応着手時に最新の差分を再確認すること（バージョンは進行中の可能性あり）。

## 対応方針

`marketplace.json` の該当エントリの `version` を `plugin.json`（source of truth）に合わせて更新する。

## 対象ファイル

- `.claude-plugin/marketplace.json`: claude-kit / work エントリの version を plugin.json に揃える

## QA

### QA-1: 修正方法

A) marketplace.json を plugin.json の最新バージョンに揃える / B) plugin.json を marketplace.json に合わせてロールバック（非推奨）

**推奨**: A — plugin.json が source of truth

**回答**: <!-- A / B -->

