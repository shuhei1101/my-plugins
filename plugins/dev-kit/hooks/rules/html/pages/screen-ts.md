---
paths:
  - "**/frontend/pages/**/screen.ts"
  - "**/frontend/pages/**/api.ts"
  - "**/frontend/pages/**/state.ts"
---

# screen.ts の作り方

`screen.ts` は画面の UI 層エントリ。DOM 取得・イベント登録・描画・URL 同期を担う。原則は `html/typescript/型システム.md`・`html/typescript/関数とオブジェクト引数.md`・`html/js/バニラTS方針.md`・`html/js/レイヤー分離.md`・`html/typescript/コメント.md`、本ルールは pages/ での定型。

- `.ts` で著作する（`// @ts-check` は不要。`.ts` は常に型検査される）。import は bare specifier（`shared/...`）で共通層を参照する。
- API レスポンス型は `shared/api/schema.d.ts` から `import type` で引く（手書きしない。`html/typescript/型システム.md`）。
- 起動は `init()` を即時呼び出し（`DOMContentLoaded` は待たない。描画済み DOM が返る）。
- DOM 参照は `getElementById`。型は `as HTMLInputElement` 等で必要なときだけ明示する。
- 描画は innerHTML が基本。値は `esc()` を通してから入れる（XSS 対策）。
- 選択状態（タブ・ID・フィルタ）は URL クエリに反映し、更新は `history.replaceState()`（`html/js/状態管理.md`）。
- 例外は握りつぶさない。catch したら `logger.error`（`html/core/エラーは握りつぶさない.md`）。

ファイル内は次の順で並べ、`// ─── 名前 ───` で仕切る:

| No | セクション | 中身 |
| --- | --- | --- |
| 1 | 定数 | モジュールレベルの定数・ラベル辞書 |
| 2 | 型 | この画面ローカルの `type`（export 不要） |
| 3 | DOM refs | `getElementById` を集約 |
| 4 | 状態 | モジュール変数（URL クエリが SoT ならその旨明記） |
| 5 | 起動 | `init()` |
| 6 | 描画 | `render*()` |
| 7 | イベント | `addEventListener` 登録 |
| 8 | ユーティリティ | 小関数 |

複雑画面は層を分ける（`html/共通化の判断.md` の前に、まずファイル分割）:

| ファイル | 入れる | 入れない |
| --- | --- | --- |
| `api.ts` | `apiFetch` 呼び出し・クエリ組み立て・レスポンス型 | DOM・描画 |
| `state.ts` | 定数・型・派生計算・フィルタ（純関数で export） | DOM・`fetch` |

`state.ts`・`api.ts` は UI を import しない（呼び出しは UI → State → API の一方向）。クラスは Custom Element 定義時だけ使う（`html/typescript/関数とオブジェクト引数.md`・`html/js/バニラTS方針.md`）。
