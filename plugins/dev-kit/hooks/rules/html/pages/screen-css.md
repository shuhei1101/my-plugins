---
paths:
  - "**/frontend/pages/**/screen.css"
---

# screen.css の作り方

その画面だけのスタイル。共通で足りるなら作らない。原則は `html/css/レイヤー構成.md`・`css/トークン.md`・`css/ネスト.md`・`css/コメント.md`・`naming/cssクラス.md`、本ルールは pages/ での定型。

- 画面固有スタイルも必ず `@layer` の中に入れる（外層は全レイヤーより強く事故になる）。画面ローカル部品は `components`、微調整は `utilities` レイヤー。順序は `shared/css/layers.css` 宣言済みなので再宣言しない。
- 色・間隔・角丸は `var(--token)` 参照。直値を書かない（`dev/マジックナンバー禁止`）。共通に無い画面ローカル値は `.page { --local-x: ... }` に集約してから参照する。
- 命名は kebab-case + BEM 風（`.card__title` / `.button--primary` / `.is-open`）。連結 `&__` は無効なのでフル記述（`css/ネスト.md`）。
- 同じ部品スタイルを 2 画面目で書きたくなったら共通層へ上げる合図（`共通化の判断.md`）。`shared/components/{name}.css` へ。
- 各セレクタの直上にコメント（`css/コメント.md`）。
