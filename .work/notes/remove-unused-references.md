---
created_at: 2026-05-30
updates:
  - 2026-05-30 — 初版作成（PR215）
related_specs: []
related_prs:
  - PR215
---

# remove-unused-references — claude-kit の未使用リファレンスファイル削除

## 概要

`plugins/claude-kit/references/glossary.md` と `incidents.md`（およびJPミラー）を削除した。
これらは `.claude/rules/glossary.md` や `.claude/rules/incidents.md` のフォーマットガイドとして追加されたが、
現在そのルールファイル自体が使われておらず、インジェクションでロードされることも不要となったため削除。

## 削除したファイル

- `references/glossary.md` / `glossary.jp.md`
- `references/incidents.md` / `incidents.jp.md`

## クリーンアップした参照箇所

- `references/_index.yaml` / `_index.jp.yaml` — エントリ削除
- `references/CLAUDE.md` / `CLAUDE.jp.md` — インジェクションルールテーブルの該当行を削除
- `skills/plugin-update/SKILL.md` / `SKILL.jp.md` — glossary/incidents の参照を削除
