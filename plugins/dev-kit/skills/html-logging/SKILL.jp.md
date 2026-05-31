<!-- This file is a Japanese mirror of SKILL.md. When updating the English original, update this file too. -->
# SKILL.jp.md — dev-kit:html-logging(日本語ミラー)

> 変更時は JP ミラーを先に更新し、その後 `SKILL.md` にも反映する。

---

**スキル名**: dev-kit:html-logging
**トリガー**: フロントエンドプロジェクトでログ整備が必要なとき。
ロガーモジュール導入(生 `console.log` を廃止)、JSON Lines 出力、レベル別出力指針、ランタイムレベル切替の整備。
「ログ整備して」「console.log 散らかってるのを整理」「操作ログを出すようにして」など。

---

# dev-kit:html-logging — フロントエンド ログ整備

フロントエンドプロジェクトに小さなロガーモジュールを導入し、レベル別の出し分け方を定義し、
JSON Lines 形式で下流ツール(Claude / ログビューア / `jq`)が読める形に統一する。

レベル: `debug` / `info` / `warn` / `error` の 4 段階。
重大事故も `error` で出す(メッセージ内で識別)。Web フロントエンドの実情に合わせた最小構成。

---

## タスク

### ステップ1: 規約を読み込む

参照:

```
{plugin_root}/references/html/principles.md   # セクション 3(JS 規約)とセクション 1(DRY)
```

プラグインルートはこのスキルファイルの2階層上。

→ ステップ2へ

---

### ステップ2: 既存のログを点検する

#### 処理

1. プロジェクト内の `console.log` / `console.info` / `console.warn` / `console.error` 使用箇所を検索する。
2. 既存のロガーモジュールがあれば確認する。
3. ログが出る/出ていないエントリポイント(ページ起動・イベントハンドラ・API 呼び出し等)を把握する。

→ ステップ3へ

---

### ステップ3: ロガーモジュールを作成(なければ)

#### 処理

`static/logger.js` 等に小さなモジュールを配置する。下記テンプレートを使い、パスや
ストレージキーをプロジェクトに合わせて調整する:

```js
// @ts-check
/**
 * ブラウザ向け JSON Lines ロガー(最小)。
 *
 * レベル: debug < info < warn < error
 * デフォルト: 本番 error、開発中 debug。
 * 保存キー: localStorage["log.level"] — デフォルトを上書き。
 *
 * 出力: console.<level>(JSON.stringify({ ts, level, msg, ...ctx }))
 */

/** @typedef {"debug"|"info"|"warn"|"error"} LogLevel */

const ORDER = /** @type {const} */ ({ debug: 10, info: 20, warn: 30, error: 40 });

/** @returns {LogLevel} */
function currentLevel() {
  const stored = /** @type {LogLevel | null} */ (
    /** @type {any} */ (localStorage.getItem("log.level"))
  );
  if (stored && stored in ORDER) return stored;
  return "error";
}

/**
 * @param {LogLevel} level
 * @param {string}   msg
 * @param {Record<string, unknown>} [ctx]
 */
function emit(level, msg, ctx) {
  if (ORDER[level] < ORDER[currentLevel()]) return;
  const record = { ts: new Date().toISOString(), level, msg, ...(ctx || {}) };
  // 1 レコード 1 行 — ディスクには絶対 pretty-print しない
  // eslint-disable-next-line no-console
  console[level](JSON.stringify(record));
}

/** @param {string} msg @param {Record<string, unknown>} [ctx] */
export const debug = (msg, ctx) => emit("debug", msg, ctx);
/** @param {string} msg @param {Record<string, unknown>} [ctx] */
export const info  = (msg, ctx) => emit("info",  msg, ctx);
/** @param {string} msg @param {Record<string, unknown>} [ctx] */
export const warn  = (msg, ctx) => emit("warn",  msg, ctx);
/** @param {string} msg @param {Record<string, unknown>} [ctx] */
export const error = (msg, ctx) => emit("error", msg, ctx);

/** @param {LogLevel} level */
export const setLevel = (level) => localStorage.setItem("log.level", level);
```

→ ステップ4へ

---

### ステップ4: レベル別の使い分けガイドを適用する

#### 処理

ログを出す箇所では、下表に従って適切なレベルを選ぶ。
既存の `console.log` をリファクタするときも、それぞれを下記のどれかに振り分ける:

| レベル | 使いどころ | 例 |
|---|---|---|
| `debug` | 開発時のみ必要な詳細トレース。本番ではデフォルト OFF | 関数の入口/出口と引数、中間状態、「ルート X にマッチ」「キー Y はキャッシュミス」 |
| `info`  | 通常運用・ユーザー操作・状態遷移。本番でも追跡したい | 「ユーザーが保存ボタン押下」「画面描画: user_list」「フォーム送信: { fields: 3 }」 |
| `warn`  | 回復可能な異常。リトライ・フォールバック・廃止予定の経路 | 「API リトライ 2/3」「任意フィールド未指定でデフォルト適用」「廃止予定ルートが呼ばれた」 |
| `error` | 注意が必要な失敗(重大事故含む)。回復不能 | 「API 500」「描画中の未捕捉例外」「データ破損検出 — 保存中止」 |

注意:
- 別レベル `critical` は設けない。ブラウザコンソール・ログ集約基盤の多くが上位を同等に扱うため、
  重大度はメッセージ内で示す: `error("PAYMENT_GATEWAY_DOWN", { incident: "critical" })`
- ユーザー操作・状態遷移には積極的に `info` を出す — デバッグの足跡になる
- 1 ログは 1 行に収める — 巨大オブジェクトを展開しない

→ ステップ5へ

---

### ステップ5: 未捕捉エラーをグローバルに拾う

#### 処理

ページ起動時に未捕捉エラーと unhandled rejection を捕捉する:

```js
// @ts-check
import { error } from "./logger.js";

window.addEventListener("error", (e) => {
  error("uncaught_error", {
    message: e.message,
    file: e.filename,
    line: e.lineno,
    col: e.colno,
  });
});

window.addEventListener("unhandledrejection", (e) => {
  error("unhandled_rejection", { reason: String(e.reason) });
});
```

→ ステップ6へ

---

### ステップ6: 生 console 呼び出しを置換する

#### 処理

1. 非テストコード内の `console.log(...)` をすべて `logger.info(...)`(または別の適切なレベル)に置換する。
2. アドホック作業の `console.debug` は一時的に許容するが、コミット前に削除する。
3. `debug-fab` ウィジェットは `console.<level>` 呼び出しを全て収集するため、
   ロガー経由に切り替えても FAB パネルにエントリが現れる。

→ 完了

#### 出力

- ロガーモジュールが導入され、レベルは `localStorage["log.level"]`(または `setLevel(...)`)で切替可能
- 全呼び出し箇所がロガー経由
- 未捕捉エラーが捕捉済み
- 各行は 1 レコード 1 行の JSON(JSON Lines)

---

## 参考資料

- `{plugin_root}/references/html/principles.md` — セクション 3(JS 規約)とセクション 1(共通化)
- `{plugin_root}/skills/debug-fab/SKILL.md` — ログを画面内に表示するデバッグウィジェット
