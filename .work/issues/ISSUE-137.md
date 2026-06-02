# ISSUE-137: claude-kit: claude-md/記述ルール.md が _injection_rules.yaml のどのパターンにも紐づいていない

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

## QA

### QA-1: どのパターンでバインドするか

A) `.claude/rules/**/*.md` など rules ファイル編集時に注入するパターンを追加する / B) `CLAUDE-md記述ガイド.md` のパターン（`**/CLAUDE{.local,.jp,}.md`）に optional として追加する / C) 利用機会が限定的と判断し削除する

**推奨**: A — `記述ルール.md` はルールファイルの執筆ガイドであり、ルールファイル編集時に注入されるのが最も適切

- [ ] A
- [ ] B
- [ ] C


---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 概要

`plugins/claude-kit/references/claude-md/記述ルール.md` は `_index.yaml` に登録（行 34）されているが、`_injection_rules.yaml` のどのパターンにも `required`/`optional` として紐づいていない。このファイルの内容は「`.claude/rules/<name>.md` の設計・作成・評価方法」であるが、ルールファイルを編集する際に自動注入されない状態になっている。

## 背景

インシデント `orphan-references-not-checked`（No.2）：`_injection_rules.yaml` 編集後は YAML とファイルシステムを突合するチェックを実行し、紐づかない reference を残さないという規約がある。

## 現状

- `plugins/claude-kit/references/claude-md/記述ルール.md` — 6937 bytes、実体のある内容あり
- `_index.yaml` 行 34: 登録済み（description あり）
- `_injection_rules.yaml`: `記述ルール` という文字列はどこにも存在しない（grep で確認済み）

`CLAUDE-md記述ガイド.md` は `**/CLAUDE{.local,.jp,}.md` パターンの `required` に登録されているが、`記述ルール.md` はどこにも参照されていない。

## 期待される状態

`記述ルール.md` が適切な編集パスパターンに `required` または `optional` として紐づいており、該当ファイルを編集する際に自動注入されること。

## 対応案

A 案（推奨）: `.claude/rules/` 配下のファイルを編集する際に注入されるパターンを追加する。
```yaml
- pattern: ".claude/rules/**/*.md"
  required:
    - claude-md/記述ルール.md
```

B 案: 頻度が低い場合は `**/CLAUDE{.local,.jp,}.md` パターンの `optional` に追加するにとどめる。
