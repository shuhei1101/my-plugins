---
paths:
  - "**/frontend/pages/**/index.html"
---

# index.html の作り方

各画面の `index.html` は `_layout.html` を継承し、`<app-shell>` の中に画面の中身だけを書く。継承の基本は `html/html/ページ雛形.md`。

ブロックの使い分け:

| ブロック  | 入れるもの                                           |
| --------- | ---------------------------------------------------- |
| `title`   | `画面名 — AITuber Dev` で統一                        |
| `head`    | 画面固有 CSS の link。`screen.css` が無ければ省く    |
| `body`    | `<app-shell>` を 1 つ。その中に画面コンテンツ        |
| `scripts` | `screen.js` を読む `<script type="module">` 1 つだけ（`screen.ts` から `tsc` が生成した `.js`。ブラウザは `.ts` を読めないので必ず `.js` を指す） |

組み立てのルール:

- `<app-shell>` に `page-title` と `data-debug-files`（この画面の html/js/css の実パス）を付ける（`components/共通シェル.md`）。
- 中身は共通レイアウトクラス（`.stack` で縦積み、`.card` でセクション）を使う。画面で独自の骨格を組まない（`layout/レイアウトパターン.md`）。
- モーダル・開閉・日付入力などはネイティブ要素を第一選択にする（`html/html/ネイティブ要素.md`）。
- JS が参照する要素には `id`、連携する値は `data-*`。意図をコメントする（`html/html/コメント.md`）。

禁止:

- インライン `<script>` ブロック・`onclick=` 等。ロジックは `screen.ts`（生成 `.js` を読み込む）+ `addEventListener`。
- importmap・共通 CSS を各 index.html に書く（`_layout` に集約済み）。
- `<app-shell>` を使わず独自ヘッダ / 枠を組む。
