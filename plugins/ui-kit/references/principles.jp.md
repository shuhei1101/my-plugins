# UI 規約 — ui-kit 共通リファレンス(日本語ミラー)

> このファイルは `principles.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更時は JP ミラーを先に更新し、その後 `principles.md` にも反映する。

開発支援画面(管理画面・内部ツール・デバッグ画面)向け規約。
ui-kit の全スキルがこの文書を参照する。UI コードを書くときは必読。

---

## 1. 共通化原則(DRY)

最重要ルール: **同じ概念を 2 箇所以上に書かない**。

- デザイン値(色・余白・タイポ)→ Foundation 層の CSS Custom Properties
- DOM セレクタ → 共有モジュールの定数に集約、ハンドラ内に生文字列を散らかさない
- ネットワーク呼び出し先 → `api/` レイヤーに集約、UI コード内で `fetch('...')` しない
- 繰り返す DOM 構造 → 小さなコンポーネント化、マークアップのコピペは禁止

同じ文字列・パターンが 3 回以上現れたら抽出する。重複監査は `.claude/rules/` 配下の
コンパニオンルール(関連ファイルを触ったときに読み込まれる)で行う。

---

## 2. CSS アーキテクチャ — FLOCSS + Design Tokens

### レイヤーモデル

| レイヤー | プレフィックス | 役割 |
|---|---|---|
| Foundation | (なし) | リセット + Design Tokens(`:root` カスタムプロパティ) |
| Layout     | `l-`   | ページレベルのレイアウト・グリッド(`l-grid`, `l-sidebar`) |
| Object — Component | `c-` | 再利用可能な小コンポーネント(`c-button`, `c-card`) |
| Object — Project   | `p-` | プロジェクト固有コンポーネント(`p-userList`) |
| Object — Utility   | `u-` | 単機能ユーティリティ(`u-mt8`, `u-textCenter`) |

コンポーネント内部は BEM 風命名: `c-button__icon--large`。

### Design Tokens

全デザイン値は Foundation 層の CSS Custom Properties から取得する:

```css
:root {
  /* color */
  --color-bg:        #fff;
  --color-text:      #111;
  --color-primary:   #2e7fff;
  --color-danger:    #ff6b6b;

  /* spacing (8px grid) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 16px;
  --space-4: 24px;

  /* typography */
  --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  --font-mono: ui-monospace, Menlo, Consolas, monospace;

  /* radius / shadow */
  --radius-md: 8px;
  --shadow-md: 0 4px 16px rgba(0,0,0,.12);
}
```

`c-*` / `p-*` / `l-*` のルール内で 16 進カラー・ピクセル値・フォントスタックをハードコードしない。
必ず `var(--token)` 経由で参照する。

### 依存方向

外側(Utility)→ 内側(Foundation)。`c-*` ルールから Foundation トークンは使えるが、
他の `c-*` や `p-*` コンポーネントには手を出さない。横断的な変更はトークン経由で行う。

---

## 3. JavaScript 規約

### 必須ファイルヘッダ

すべての JS ファイルの先頭に以下を入れる:

```js
// @ts-check
```

これでビルドなしに、エディタの TypeScript Server で型チェックが効く。

### JSDoc による型注釈

エクスポート関数・公開変数・複雑なオブジェクトには JSDoc 型を付ける:

```js
/**
 * @param {string} userId
 * @param {{ includeDeleted?: boolean }} [opts]
 * @returns {Promise<User>}
 */
export async function fetchUser(userId, opts = {}) { ... }

/** @typedef {{ id: string; name: string; createdAt: string }} User */
```

共有型は `@typedef`、ジェネリクスは `@template` を使う。裸の `any` は避ける。

### レイヤー分離

| レイヤー | 役割 |
|---|---|
| **UI**    | DOM アクセス・イベントハンドラ・レンダリング。state と api をインポートする。`fetch` 直叩き禁止 |
| **State** | メモリ上の状態・派生計算。可能な限り純関数。DOM 触らない |
| **API**   | 通信 I/O 全般。`fetch` のラッパー。型付き Promise を返す。DOM 触らない |

呼び出しは下方向のみ(UI → State → API)。State と API は UI をインポートしない。

### 関数指向 > クラス指向

デフォルトは普通の関数 + クロージャ。インスタンス同一性が真に必要な場合(バニラ DOM コードでは稀)
のみクラスを使う。継承チェーンは作らない。

### インラインスクリプトは最小限

HTML 内の `<script>` ブロックや `onclick="..."` 属性は避ける。
外部 `.js` ファイル + `addEventListener` を使う。
例外: メインモジュールをロードするための小さな起動スニペットは許容。

### CSS クラス ↔ JS DOM アクセスの紐付け

DOM 取得セレクタは CSS で定義された FLOCSS クラスと一致させる。
`.claude/rules/` のコンパニオンルールが関連ファイル編集時に読み込まれ、同期を確認する。

FLOCSS クラスでクエリするのを優先:

```js
const btn = document.querySelector(".c-button");           // OK
const list = document.querySelector(".p-userList__items"); // OK
```

または安定 ID をトークン / 定数で公開:

```js
const SELECTORS = {
  userListItems: ".p-userList__items",
  userListEmpty: ".p-userList__empty",
};
```

ハンドラ内に魔法文字列を散らかさない。

---

## 4. 必須: `frontend-design` スキル

UI のあらゆるビジュアル / UX 作業 — コンポーネント・ページ・レイアウト判断・タイポグラフィ・配色・モーション — では
`frontend-design:frontend-design` スキルを**例外なく**呼び出す。

このスキルが担保するもの:
- 明確なコンセプト/美的方向性(AI 汎用デフォルトに陥らない)
- 特徴あるタイポグラフィと配色の選択
- 意図のあるモーション・空間構成
- 美的ビジョンと釣り合った実装グレード

その場のセンスで UI を書かない。あらゆる視覚的判断はこのスキル経由で行う。
