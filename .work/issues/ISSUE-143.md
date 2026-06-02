# ISSUE-143: injection.md.j2 / injection.jp.md.j2 テンプレートに Jinja2 Markdown バグが2件

**作成日**: 2026-06-02

## 問題

`plugins/ref-inject/templates/hooks/templates/injection.md.j2`（および `.jp.md.j2`）に、リファレンスが定めた Jinja2 テンプレートの2つのアンチパターンが残っている。claude-kit の消費者側（`plugins/claude-kit/hooks/templates/injection.md.j2`）はすでに修正済みだが、テンプレート側が追いついていない。

### バグ 1 — `}}` で終わる見出し行に `<!-- -->` がない（Pitfall 3）

```jinja2
## {{ ref.path }} — {{ ref.description }}
```

Handlebars/Mustache 系パーサーが `}}` から次のコンテンツへスキャンを続け、後続コンテンツが黙って消える場合がある。claude-kit 側は `<!-- -->` を追記して修正済み。

### バグ 2 — `{% if optional %}` の直後に `---` が来る（Pitfall 1/2）

```jinja2
{% if optional %}
---
```

`trim_blocks=True` によって `%}` 直後の改行が除去され、直前のコンテンツ末尾行＋`---` が setext-style 見出しに化けてセパレーターが消える。正しくは `{% if optional %}` ブロック内の先頭に空行を置く必要がある。claude-kit 側は `{% if optional %}\n\n---` に修正済み。

## 対応方針

1. `injection.md.j2` の `## {{ ref.path }} — {{ ref.description }}` を `## {{ ref.path }} — {{ ref.description }}<!-- -->` に変更する
2. `{% if optional %}` の直後に空行を挿入して `{% if optional %}\n\n---` にする
3. `injection.jp.md.j2` にも同様の修正を適用する
4. `/ref-inject:plugin-migrate` を実行して消費者（dev-kit / work）に伝播させる（claude-kit はすでに修正済み）

## 対象ファイル

- `plugins/ref-inject/templates/hooks/templates/injection.md.j2`: 上記2箇所を修正
- `plugins/ref-inject/templates/hooks/templates/injection.jp.md.j2`: 同様に修正

# ユーザー回答欄

## 意思

**回答**: <!-- 承認 / 却下 / 保留 -->
