# dev-kit リファレンス関数型スタイル規約 — function-first / type 優先の徹底

## 概要

dev-kit の全リファレンス（Next.js + Python）が示すコード例・記述は、**function-first + `type` 優先スタイル**で統一されている。振る舞いはモジュールレベルの関数に置き、クラスは限定された例外のみに使う。本規約はその基準と、許容されるクラス使用の境界をまとめたもの。

## 基準ドキュメント（正典）

| # | 言語 | ファイル | 役割 |
|---|---|---|---|
| 1 | Next.js/TS | `plugins/dev-kit/references/next/frontend/conventions/型規約.md` | `type` 優先・`interface` はライブラリ拡張のみ |
| 2 | 〃 | `plugins/dev-kit/references/next/frontend/conventions/命名規約.md` | 関数命名（`fetch{Feature}` 等） |
| 3 | Python | `plugins/dev-kit/references/python/architecture/TypeScriptスタイル適用.md` | Function-First の中心ドキュメント |
| 4 | 〃 | `plugins/dev-kit/references/python/architecture/設計原則.md` | クラス vs 関数の優先順位 |

## 規約

### 振る舞いは関数で書く

- Service / Repository / Provider / Validator / Manager 等は **すべて関数**で実装する。
- 依存は関数型エイリアスで受けて注入する（TS: `type FetchResource = (args: {...}) => Promise<...>` / Python: `type FindUser = Callable[[UserId], User | None]` を `partial` で注入）。
- データアクセスは `fetch{Feature}` / `insert{Feature}` / `update{Feature}` のような素の関数。引数はオブジェクト渡し。
- 継承によるポリモーフィズムは使わない（TS: 構造的型・関数注入 / Python: `Protocol` のダックタイピング）。

### 型定義

- TS: 型・関数型は `type` エイリアスで定義。`interface` はライブラリの宣言マージ（例: styled-components の `DefaultTheme` 拡張）のみ許容。
- Python: DTO は `@dataclass(frozen=True, slots=True, kw_only=True)` / `pydantic.BaseModel` / `TypedDict`。

### クラスが許容される例外

| # | 例外 | 例 |
|---|---|---|
| 1 | エラークラス | `class AppError extends Error` とそのサブクラス |
| 2 | テスト用 Page Object | Playwright の `class CartPage` / `class LoginPage` |
| 3 | DTO（Python） | `@dataclass` / `pydantic.BaseModel` / `Enum` |
| 4 | 構造的型（Python） | `Protocol`（継承宣言不要のダックタイピング） |
| 5 | ライブラリ要求 | FastAPI Middleware、CLI Command、Pydantic 継承、DB 接続プール等の長命ランタイム状態 |

## 監査状況

2026-06-01 時点で dev-kit の全リファレンスを精読監査済み（Next.js 約89ファイル + Python 約42ファイル、計131ファイル）。**真の違反は 0 件**。検出された `class` / `interface` / `extends` はすべて上記の許容例外、または「やってはいけないこと」節の意図的アンチパターン例だった。

## 変更履歴

| 日付 | 内容 | ブランチ |
|---|---|---|
| 2026-06-01 | 初版作成。全リファレンス精読監査の結果（違反0件）と基準をまとめた | docs/reference-functional-style-audit |
