---
paths:
  - "**/shared/css/**"
---

# shared/css

コンポーネントに属さない基盤スタイルだけを置く。コンポーネント CSS は `shared/components/` に置く。

| ファイル      | 役割                                                               |
| ------------- | ------------------------------------------------------------------ |
| layers.css    | `@layer` 順序宣言 + 各 css を `@import` で集約（エントリポイント） |
| reset.css     | normalize                                                          |
| tokens.css    | デザイントークン（詳細は `css/トークン.md`）                       |
| base.css      | 要素デフォルト・タイポグラフィ                                     |
| layout.css    | ページ骨格・グリッド（詳細は `layout/レイアウトパターン.md`）      |
| utilities.css | 単一目的ユーティリティ・バッジ等                                   |
