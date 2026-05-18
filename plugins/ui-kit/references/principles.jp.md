# UI 規約 — ui-kit 共通リファレンス(日本語ミラー)

> このファイルは `principles.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更時は JP ミラーを先に更新し、その後 `principles.md` にも反映する。

開発支援画面(管理画面・内部ツール・デバッグ画面)向け規約。
ui-kit の全スキルがこの文書を参照する。UI コードを書くときは必読。

---

## 1. 共通化原則(DRY)— 初日から拡張性を設計する

最重要ルール: **同じ概念を 2 箇所以上に書かない**。

- デザイン値(色・余白・タイポ)→ Foundation 層の CSS Custom Properties(コード上の `constants` ビュー)
- DOM セレクタ → 共有モジュールの定数に集約、ハンドラ内に生文字列を散らかさない
- ネットワーク呼び出し先 → `api/` レイヤーに集約、UI コード内で `fetch('...')` しない
- 繰り返す DOM 構造 → 小さなコンポーネント化、マークアップのコピペは禁止
- **ルーティング**: 全ルート定義を 1 ファイルに集約(例: `static/js/routes.js`)。
  UI / API モジュールはここからインポートする。画面内に URL ハードコード禁止。
- **定数**: 全定数(色トークン名・API エンドポイント・デフォルト値)を 1 ファイルに集約(例: `static/js/constants.js`)。
  任意の発展: アプリ内に「デザイン設定画面」を用意し、トークン値をランタイムから調整できるようにする。

同じ文字列・パターンが 3 回以上現れたら抽出する。重複監査は `.claude/rules/` 配下の
コンパニオンルール(関連ファイルを触ったときに読み込まれる)で行う。

### なぜ「初日から拡張性を入れる」(YAGNI ではなく)

実装は Claude / AI エージェントが行うため、拡張性を最初から設計する追加コストはほぼゼロ。
一方、ハードコードで絡まった画面を後でリファクタするコストは大きい。

そのため:
- 「とりあえずハードコード」は禁止。一回限りの画面でもトークン / 定数 / ルート経由で書く
- インターフェース(JSDoc `@typedef`)を実装より先に決める。実装はそこから派生する
- 新しい要件は既存の拡張ポイントに収まるべき。「この場合は想定外だから書き直す」は避ける

### 画面状態を URL クエリストリングに反映する — 必須

**画面切替系のインタラクションすべて**で URL クエリストリングを更新し、アクティブ状態を
URL に反映する。**例外なし**。

- トップタブ                → `?tab=settings`
- サイドバーメニュー        → `?nav=tools`
- 一覧 ↔ 詳細遷移            → `?view=detail&id=42`
- ページネーション / フィルタ / ソート → `?page=3&filter=active&sort=name`

#### なぜ

- 開発者が Claude Code に URL を貼るだけで、どの画面・タブ・選択について話しているかが伝わる
- ブラウザの戻る / 進むで状態が復元される
- URL を共有・ブックマークできる
- DOM 状態と URL が同期する — 「タブ X にいるが URL はデフォルトのまま」が起こらない

#### どう実装するか

URL 状態のロジックは 1 モジュールに集約(例: `static/js/url-state.js`):

```js
// @ts-check
/** @typedef {Record<string, string>} UrlState */

/** @returns {UrlState} */
export const readState = () =>
  Object.fromEntries(new URLSearchParams(location.search));

/** @param {Partial<UrlState>} patch */
export const writeState = (patch) => {
  const params = new URLSearchParams(location.search);
  for (const [k, v] of Object.entries(patch)) {
    if (v == null || v === "") params.delete(k);
    else params.set(k, /** @type {string} */ (v));
  }
  const next = params.toString();
  const url = next ? `${location.pathname}?${next}` : location.pathname;
  history.pushState(null, "", url);
  window.dispatchEvent(new CustomEvent("urlstatechange"));
};
```

各切替ウィジェットは `writeState({ tab: "..." })` を呼び、`urlstatechange`(と `popstate`)を
購読して再描画する。ウィジェットが自前の「アクティブ状態」を単独で保持しない —
URL が唯一の真実の源(single source of truth)。

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

エクスポート関数・公開変数・複雑なオブジェクトには JSDoc 型を付ける。
`JSDoc + // @ts-check` をプロジェクトの型システムとして扱う —
ビルドステップなしで TypeScript の大半の機能が使える。

#### 使える機能

| TypeScript 機能 | JSDoc 相当 |
|---|---|
| 型エイリアス `type X = {...}` | `/** @typedef {{ ... }} X */` |
| リテラルユニオン `"a" \| "b" \| "c"` | `@typedef {"a"\|"b"\|"c"} ABC` |
| 通常ユニオン `string \| number` | `@param {string\|number} id` |
| インターセクション `A & B` | `@typedef {Readable & Writable} RW`(`@typedef` を組み合わせる) |
| ジェネリクス `<T>` | 関数 / typedef に `@template T` |
| Readonly / Partial / Pick / Omit | `@type` / `@typedef` 内で `Readonly<T>` / `Partial<T>` / `Pick<T, K>` / `Omit<T, K>` |
| `keyof T` | `@type {keyof T}` |
| インデックスアクセス `T[K]` | `@type {T[K]}` |

```js
// @ts-check

/** @typedef {"draft"|"published"|"archived"} PostStatus */
/** @typedef {{ id: string; title: string; status: PostStatus }} Post */

/**
 * @param {string} postId
 * @param {Partial<Post>} patch
 * @returns {Promise<Post>}
 */
export const updatePost = async (postId, patch) => { /* ... */ };
```

裸の `any` は避ける。本当に型不明なら `unknown` を使って絞り込む。

### 関数指向 > クラス指向

JSDoc 型が形状定義を担うので、**クラスはほぼ不要**。

- **アロー関数を `const` に代入**するのをデフォルトに: `const fn = (...) => { ... }`
- `function ...` 宣言はホイスティングが本当に必要なときだけ(稀)
- 構成は小さな関数 + クロージャ、継承チェーンなし
- 「コンストラクタ注入」 → **関数引数注入**(依存をパラメータで渡す)

```js
// 悪い例 — コンストラクタ付きのクラス
class UserService {
  constructor(api, logger) { this.api = api; this.logger = logger; }
  async load(id) { /* this.api / this.logger を使う */ }
}

// 良い例 — 依存を関数引数で注入
/**
 * @param {{ api: UserApi; logger: Logger }} deps
 * @returns {{ load: (id: string) => Promise<User> }}
 */
export const createUserService = ({ api, logger }) => ({
  load: async (id) => {
    logger.info("user.load", { id });
    return api.get(`/users/${id}`);
  },
});
```

ファクトリ関数がクロージャで閉じ込めた依存を共有するオブジェクト(関数群)を返す。
クラスの DI と同じ利点を `this` なしで得られ、JSDoc で完全に型チェックできる。

### レイヤー分離

| レイヤー | 役割 |
|---|---|
| **UI**    | DOM アクセス・イベントハンドラ・レンダリング。state と api をインポートする。`fetch` 直叩き禁止 |
| **State** | メモリ上の状態・派生計算。可能な限り純関数。DOM 触らない |
| **API**   | 通信 I/O 全般。`fetch` のラッパー。型付き Promise を返す。DOM 触らない |

呼び出しは下方向のみ(UI → State → API)。State と API は UI をインポートしない。

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

---

## 5. 併読: `ui-design.md`

レイアウトパターン(サイドバー / 2 ペイン / タブ)、画面タイプ別テンプレート(トップ / 設定 / 一覧+詳細)、
フォーム / ダイアログ / ショートカット規約、状態フィードバック、
アクセシビリティ、ダークモード、モーション詳細は同階層の `ui-design.md` に置かれている。
UI を設計するときは両方を併読する。
