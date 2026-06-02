# ISSUE-180: dev-kit injection.md.j2 / injection.jp.md.j2 が Jinja2 Pitfall 1/2/3 をすべて踏んでいる（claude-kit との drift）

**作成日**: 2026-06-02

# ユーザー回答欄

## 意思

- [x] 対応する
- [ ] 対応しない

---

<!-- ここから下は AI 記入欄（イシュー本文）。ユーザーは通常編集しない -->

## 問題

`plugins/dev-kit/hooks/templates/injection.md.j2` と `injection.jp.md.j2` が Jinja2 × Markdown の 3 つの既知 Pitfall をすべて踏んでいる。claude-kit の対応テンプレートにはすべての修正が適用済みで、dev-kit だけ取り残された状態（キット間 drift）。なお claude-kit 側は ISSUE-166（Pitfall 3）で別途報告済み。

### Pitfall 3 — `}}` で終わる見出しに `<!-- -->` がない

```jinja2
## {{ ref.path }} — {{ ref.description }}       ← 現状
## {{ ref.path }} — {{ ref.description }}<!-- --> ← 期待
```

### Pitfall 1 — `{% for ref in required %}` 直後の `---` が setext heading になる

`trim_blocks` が `%}` 直後の改行を食うため、前 ref の最終行と `---` が隣接し setext heading に誤解釈される。`{% for %}` ブロック内先頭に空行を挿入する。

### Pitfall 2 — `{% if optional %}` 直後の `---` が setext heading になる

`{% if optional %}` ブロック内先頭に空行を挿入する。

## 対応方針

claude-kit の `injection.md.j2` / `injection.jp.md.j2` と同一になるよう dev-kit の EN・JP 両テンプレートを修正する。`/ref-inject:plugin-migrate` での伝播も検討。

## 対象ファイル

- `plugins/dev-kit/hooks/templates/injection.md.j2`: 見出しに `<!-- -->` 追加、`{% for %}` 内・`{% if optional %}` 内に空行挿入
- `plugins/dev-kit/hooks/templates/injection.jp.md.j2`: 同上
