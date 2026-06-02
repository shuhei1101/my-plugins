# ISSUE-170: dev-kit:plugin-config に削除済みトグル DEV_KIT_MARKDOWN_CHECK が残存

**作成日**: 2026-06-02

## 問題

`dev-kit:plugin-config` スキルが `DEV_KIT_MARKDOWN_CHECK` を管理対象トグルとして列挙し続けているが、このトグルに対応するフック（`markdown_frontmatter_check.py`）は v4.10.0（2026-05-31）で削除済みである。実際のフックスクリプト群（`hooks/scripts/`）に `DEV_KIT_MARKDOWN_CHECK` への参照はない。

v4.10.0 changelog:
> Remove `markdown_frontmatter_check.py` hook; rule is already enforced via `references/markdown/マークダウン編集.md` auto-injection on `**/*.md`

plugin-config/SKILL.md の「Feature toggles」テーブル（34行目）、Step 2 の numbered list（106行目）、Step 3・Step 4 の Normal polarity vars リストに残存している。

## 対応方針

`DEV_KIT_MARKDOWN_CHECK` に関する記述をすべて `SKILL.md` および `SKILL.jp.md` から削除する。管理対象トグルの数は 6 → 5 になる。なお、ISSUE-152（`DEV_KIT_MARKDOWN_CHECK` の `${}` ラッパー不統一）はこのイシュー対応で自動解消される。

## 対象ファイル

- `plugins/dev-kit/skills/plugin-config/SKILL.md`: `DEV_KIT_MARKDOWN_CHECK` の全記述を削除
- `plugins/dev-kit/skills/plugin-config/SKILL.jp.md`: 同上

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
