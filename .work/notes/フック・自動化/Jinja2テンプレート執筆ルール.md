# Jinja2 テンプレート執筆ルール — Markdown 出力時の注意事項

`hooks/templates/*.j2`（Markdown を出力する Jinja2 テンプレート）を書く際の
落とし穴と対処法。`claude-kit` references として明文化（PR222）。

参照: `plugins/claude-kit/references/jinja2/templates.md`（+ `.jp.md`）

## 背景

PR201（`claude-kit-jp-mirror-env`）で `injection.md.j2` / `injection.jp.md.j2` を
編集中に、Jinja2 のホワイトスペース除去と Markdown のブロック要素間スペーシングの
相互作用で発生する 3 つのレンダリングバグに遭遇した。テンプレートのソースを見ても
原因が分かりにくく、出力を見て初めて気付くタイプのバグ。

## 3 つのバグパターン

### 1. `trim_blocks=True` が `{% %}` 直後の改行を 1 つ食う

```jinja
{% if note %}
> {{ note }}
{% endif %}
## 次の見出し
```

`{% endif %}` 直後の改行が消えるので、blockquote と heading が隣接行で衝突する。

**対処**: 空行を `{% endif %}` の **内側** に置く。

### 2. `{% endif %}{% if X %}` 連鎖 + `---` で setext 見出し化

```jinja
{% for ref in required %}
- {{ ref.name }}
{% endfor %}
{% endif %}
{% if optional %}
---
```

`{% endif %}{% if optional %}` の連鎖で改行が全部消え、`- last_ref_name` の次行が
`---` になり、`last_ref_name` が setext 見出し（dash 下線）として解釈される。
`---` セパレータも消える。

**対処**: 空行を `{% if optional %}` の **内側** の先頭に置く。

### 3. 見出し末尾の `}}` が Handlebars 系パーサーを混乱させる

```jinja
## {{ ref.path }} — {{ ref.description }}
```

行末の生の `}}` を Handlebars / Mustache / Jinja2 系記法を使う下流ツール
（IDE プレビュー等）が template 終端と誤認識し、後続コンテンツが消える。

**対処**: `## {{ ... }} — {{ ... }}<!-- -->` のように末尾を HTML コメントで閉じる。

## 注入対象

`_injection_rules.yaml` に以下のルールを追加し、任意プラグインの Jinja2
テンプレート編集時に自動注入されるようにした。

```yaml
- pattern: "**/hooks/templates/*.j2"
  required:
    - jinja2/templates.md
  optional: []
```

既存の `plugins/*-kit/hooks/templates/*.j2` ルール（`kit-hooks-sync.md` を注入）
とは additive に並ぶ。注入フック側で reference は dedup される。

## 一般的なオーサリングガイダンス

- テンプレートは末尾改行 1 つで終わらせる
- `{%- ... -%}` の dash 付き変種は `trim_blocks` / `lstrip_blocks` との組み合わせが
  悪く、推論しづらいので避ける
- テンプレート構文だけでなくレンダリング結果をテストする
- 制御タグは 1 行 1 タグに保つ（`{% endif %}{% endfor %}` を 1 行に詰めない）

## 関連

- PR201: バグ修正の本体（`f6d1b205 fix: injection テンプレートの Markdown レンダリングバグを修正`）
- PR222: 本ルールのドキュメント化と自動注入登録
