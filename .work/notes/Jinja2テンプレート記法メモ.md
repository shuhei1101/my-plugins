---
created_at: 2026-05-31
updates:
  - 2026-05-31 — 初版作成（PR227）
related_notes: []
related_branches:
  - feat/claude-kit-jinja2-authoring-rule
---

# Jinja2 テンプレート記法メモ — .j2 ファイル記述時の既知の罠と対処法

## 概要

claude-kit / dev-kit の注入フックは `trim_blocks=True` / `lstrip_blocks=True` を有効にした
Jinja2 エンジンでテンプレートをレンダリングする。この設定の副作用として、
いくつかの Markdown 記法が壊れるケースが PR201 で発見・修正された。
このノートにその知見を集約する。

## 前提: inject_references.py の Jinja2 設定

```python
Environment(
    trim_blocks=True,    # ブロックタグ直後の改行を削除
    lstrip_blocks=True,  # ブロックタグ行の先頭空白を削除
)
```

両オプションとも有効な状態を前提として記載する。

## 既知の罠

### 1. `{% %}` 直後に `---` を置くと setext heading になる

#### 現象

```jinja2
{% if optional %}
---
## Optional references
```

`trim_blocks=True` によって `{% if optional %}` 直後の改行が消えるため、
`---` が直前の何かの行の下に続いてしまい、setext heading（アンダーライン型見出し）として
レンダリングされる場合がある。

#### 対処法

`{% %}` タグの後に空行を挿入する。または `{% %}` とコンテンツの間に空行を明示的に残す:

```jinja2
{% if optional %}

---
## Optional references
```

### 2. `## {{ ref.path }}` ヘッダー内の Jinja2 式

#### 現象

`## {{ ref.path }} — {{ ref.description }}` のように `##` ヘッダーに `{{ }}` が含まれると、
Markdown パーサーがヘッダーとして認識しない・または表示が崩れることがある。

#### 対処法

ヘッダー末尾に `<!-- -->` を追加して Markdown の setext heading バグを抑制する:

```jinja2
## {{ ref.path }} — {{ ref.description }}<!-- -->
```

### 3. `{% if not jp_mirror %}` 通知後の改行

#### 現象

```jinja2
{% if not jp_mirror %}
> 通知テキスト

{% endif %}
```

`trim_blocks=True` 下では `{% if not jp_mirror %}` の直後の改行が消え、
`> 通知テキスト` が直接続く形になる。出力の先頭にブロッククォートが突然現れると
Markdown レンダラの解釈が乱れることがある。

#### 対処法

`{% if %}` ブロックの直後に空行を明示する:

```jinja2
{% if not jp_mirror %}

> 通知テキスト

{% endif %}
```

### 4. `lstrip_blocks=True` によるインデント除去

#### 現象

インデントされた `{% for %}` などのブロックタグは、行頭の空白が除去される。
テンプレートのインデントで見栄えを整えても、実際の出力にはインデントが反映されない。

#### 対処法

インデントが出力に必要な場合は、ブロックタグ外で明示的に空白を記述する。
または `lstrip_blocks` が不要なら無効化することも検討（ただし inject_references.py を
両 kit で変更する必要がある）。

## 確認済み修正 (PR201)

| # | ファイル | 修正内容 |
|---|---|---|
| 1 | `plugins/claude-kit/hooks/templates/injection.md.j2` | `{% if optional %}` 直後 `---` の setext heading バグを修正 |
| 2 | 〃 | `## {{ ref.path }}` 末尾に `<!-- -->` を追加 |
| 3 | 〃 | `{% if not jp_mirror %}` 後の空行を明示 |
| 4 | `plugins/claude-kit/hooks/templates/injection.jp.md.j2` | 同上の JP 版 |
