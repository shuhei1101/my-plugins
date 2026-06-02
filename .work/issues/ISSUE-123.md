# ISSUE-123: provenance.md が複数箇所から参照されているが実体が存在しない

**作成日**: 2026-05-31

## 概要

`references/provenance.md` は実在しないのに、複数のリファレンス・スキルファイルから参照されており、死リンク・循環参照・存在しない注入ルール記述を生んでいる。

## 背景

provenance（JP ミラー警告コメントのフォーマット／スタンプ手順）という概念が文書群に散在しているが、その中核となるはずの `provenance.md` が存在しない。

## 現状

以下の参照が存在するが、`references/provenance.md` は実在しない。

- `references/common/共通ガイド.md` 行 86: `(see `provenance.md`)` — JP ミラー警告コメントの補足として参照
- `references/skill/スキル.md` 行 7: `the provenance-stamping step` と記述
- `references/skill/スキル.md` 行 70: `(provenance step in `共通ガイド.md`)` — 共通ガイド.md が provenance.md を参照しているため循環的な死リンク
- `references/skill/スキル.md` 行 153（最終チェックリスト）: `Both files stamped per `provenance.md` (auto-injected when you write the file)` — provenance.md が自動注入されると書かれているが `_injection_rules.yaml` に対応ルールが存在しない

さらに、`skills/*/SKILL.md` 複数ファイルにも `references/provenance.md` への参照が残っている（リファレンス文書側の参照が源泉）。

## 期待される状態

provenance に関する記述が一貫し、死リンク・循環参照・存在しない注入ルール記述が解消されている。

## 対応案

| 案 | 内容 | メリット | デメリット |
|---|---|---|---|
| A | `provenance.md` を実際に作成し、JP ミラー警告コメントのフォーマットとスタンプ手順を記述。`_index.yaml` 追加と書き込みイベント用注入ルール追加も実施 | provenance の概念を文書として確立 | 新規ファイル + 注入ルールの保守コスト |
| B | provenance.md という概念を削除し、JP ミラー警告コメントのフォーマットを `共通ガイド.md` の JP/EN ミラールールセクションに直接統合。`スキル.md` 等の参照記述も削除/書き換え | ファイルを増やさず一箇所に集約 | 複数ファイルの参照記述を一斉修正する必要 |

**推奨: 案B**（概念を共通ガイドへ統合し、参照を整理）

## 横展開

`skills/claude-creator/SKILL.md`、`skills/skill-creator/SKILL.md`、`skills/rule-creator/SKILL.md`、`skills/hook-creator/SKILL.md`、`skills/plugin-creator/SKILL.md` の各ファイルにも同様の参照が残っており、同時に修正が必要。

---

# ユーザー回答欄

> 回答方法: 各 `**回答**:` 行で不要な選択肢を消し、1 つだけ残す（`{回答を入力}` は自由記入）。
> AI は選択肢・推奨と、候補を並べた `**回答**:` 行まで用意する。

## 意思

このイシューに対応するか。

**回答**: 対応する / 対応しない

## QA

### QA-1: provenance.md を作成するか概念ごと統合するか

A) `provenance.md` を作成して注入ルールに登録 / B) 概念を `共通ガイド.md` に統合し参照記述を整理

**推奨**: B — 概念を共通ガイドへ統合すればファイルを増やさず、散在する参照を一箇所に集約できる。

**回答**: A / B
