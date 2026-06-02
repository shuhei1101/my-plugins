# ISSUE-174: py-project / py-script が references/python/index.yaml を参照しているが当該ファイルは存在しない

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`dev-kit:py-script` の `SKILL.md` と `dev-kit:py-project` の `SKILL.jp.md`（SKILL.md は欠落）が Step 1 で `{plugin_root}/references/python/index.yaml` の読み込みを指示しているが、このファイルは存在しない。

また `SKILL.jp.md` の Step 10 は `{plugin_root}/references/python/injection_rules.yaml` も参照しているが存在しない（Python サブフォルダには `_injection_rules.yaml` も置かれていない）。

実際に存在するインデックスは `plugins/dev-kit/references/_index.md`（全体 Markdown インデックス）。

## 対応方針

`index.yaml` の参照を `{plugin_root}/references/_index.md`（全体インデックス）に置き換える。`injection_rules.yaml` 参照もルートの `_injection_rules.yaml` に修正する。

## 対象ファイル

- `plugins/dev-kit/skills/py-script/SKILL.md`: `references/python/index.yaml` の参照先を修正
- `plugins/dev-kit/skills/py-project/SKILL.jp.md`: `index.yaml`・`injection_rules.yaml` 参照を修正

## QA

### QA-1: index の参照先

A) `references/_index.md`（全体インデックス）を参照する / B) `references/python/index.md` を新規作成して参照する

**推奨**: A — 既存の `_index.md` に Python セクションが網羅されており、新規ファイル作成なしで解決できる

**回答**: <!-- A / B -->
