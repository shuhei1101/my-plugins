# ISSUE-123: provenance.md が複数箇所から参照されているが実体が存在しない

**作成日**: 2026-05-31

## 問題
以下の参照が存在するが、`references/provenance.md` は実在しない。

- `references/common/共通ガイド.md` 行86: `(see `provenance.md`)` — JP ミラー警告コメントの補足として参照
- `references/skill/スキル.md` 行7: `the provenance-stamping step` と記述
- `references/skill/スキル.md` 行70: `(provenance step in `共通ガイド.md`)` — これ自体も 共通ガイド.md が provenance.md を参照しているため循環的な死リンク
- `references/skill/スキル.md` 行153（最終チェックリスト）: `Both files stamped per `provenance.md` (auto-injected when you write the file)` — provenance.md が自動注入されると書かれているが `_injection_rules.yaml` に対応ルールが存在しない

さらに、`skills/*/SKILL.md` 複数ファイルにも `references/provenance.md` への参照が残っている（これはリファレンスではなくスキルファイルだが、リファレンス文書側の参照が源泉）。

## 修正案

**案 A**: `provenance.md` を実際に作成して、JP ミラー警告コメントのフォーマットとスタンプ手順を記述する。その場合 `_index.yaml` への追加と、書き込みイベント用の注入ルール追加も必要。

**案 B**: provenance.md という概念を削除し、JP ミラー警告コメントのフォーマットを `共通ガイド.md` の JP/EN ミラールールセクションに直接統合する。`スキル.md` 等の参照記述も削除または書き換える。

## 水平展開
`skills/claude-creator/SKILL.md`、`skills/skill-creator/SKILL.md`、`skills/rule-creator/SKILL.md`、`skills/hook-creator/SKILL.md`、`skills/plugin-creator/SKILL.md` の各ファイルにも同様の参照が残っており、同時に修正が必要。
