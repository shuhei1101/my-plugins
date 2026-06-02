# ISSUE-167: py-project/SKILL.md が存在しない（英語版 SKILL.md 欠落）

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [ ] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/dev-kit/skills/py-project/` に `SKILL.jp.md` のみが存在し、英語版 `SKILL.md` が欠落している。他のすべてのスキルは英語版 `SKILL.md` を source of truth として持ち、`SKILL.jp.md` はそのミラーという構造を取っている。`py-project` だけがこの構造を満たしていない。

## 対応方針

`SKILL.jp.md` の内容を英語に翻訳して `SKILL.md` を新規作成し、`SKILL.md` を source of truth・`SKILL.jp.md` をミラーとする標準構造に戻す。`SKILL.jp.md` には冒頭の mirror 警告コメントと YAML frontmatter を追加する。

## 対象ファイル

- `plugins/dev-kit/skills/py-project/SKILL.md`: 新規作成（`SKILL.jp.md` の英語翻訳）
- `plugins/dev-kit/skills/py-project/SKILL.jp.md`: mirror 警告コメント・YAML frontmatter を追加

