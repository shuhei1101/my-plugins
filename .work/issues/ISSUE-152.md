# ISSUE-152: dev-kit:plugin-config の DEV_KIT_MARKDOWN_CHECK が ${}ラッパーなし・work Notes からも漏れ

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`dev-kit:plugin-config` SKILL.md において `DEV_KIT_MARKDOWN_CHECK` の記述が複数箇所で `${}` ラッパーなし（lines 34, 64, 138, 176）になっており、`${DEV_KIT_NEXT_TS_CHECK}` など他の変数と表記が不統一である。

さらに `work:plugin-config` の Notes（SKILL.md line 188）が dev-kit トグルの参照リストとして「`${DEV_KIT_PYTHON}` / `${DEV_KIT_HTML}` / `${DEV_KIT_NEXT}` / `${DEV_KIT_MARKDOWN}` / `${DEV_KIT_NEXT_TS_CHECK}`」と記述しているが、`DEV_KIT_MARKDOWN_CHECK` が抜けている。

## 対応方針

1. `dev-kit/skills/plugin-config/SKILL.md` の `DEV_KIT_MARKDOWN_CHECK` を全箇所 `${DEV_KIT_MARKDOWN_CHECK}` に統一する
2. `work/skills/plugin-config/SKILL.md` の Notes で `${DEV_KIT_MARKDOWN_CHECK}` を追記する
3. 各 JP ミラーを同期する

## 対象ファイル

- `plugins/dev-kit/skills/plugin-config/SKILL.md`: lines 34, 64, 138, 176 の `DEV_KIT_MARKDOWN_CHECK` を `${DEV_KIT_MARKDOWN_CHECK}` に修正
- `plugins/dev-kit/skills/plugin-config/SKILL.jp.md`: 同 JP ミラー修正
- `plugins/work/skills/plugin-config/SKILL.md`: line 188 の dev-kit トグルリストに `${DEV_KIT_MARKDOWN_CHECK}` を追記
- `plugins/work/skills/plugin-config/SKILL.jp.md`: 同 JP ミラー修正

