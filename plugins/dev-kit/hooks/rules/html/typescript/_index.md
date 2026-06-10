---
paths:
  - "**/*.{ts,tsx}"
---

# 汎用 TypeScript 規約

TypeScript を使う全プロジェクト共通の言語規約。`paths` を `**/*.{ts,tsx}` にしてあり、バニラ TS でも Next.js でも適用される（フレームワーク非依存の型・関数・コメントの書き方のみ）。

| No | ファイル | 範囲 |
| --- | --- | --- |
| 1 | `型システム.md` | type 既定・union/リテラル・関数型エイリアス・generics・戻り値導出・import type・型の置き場所 |
| 2 | `関数とオブジェクト引数.md` | オブジェクト引数・関数型での依存注入 |
| 3 | `コメント.md` | 宣言の 1 行説明・型注釈は書かない・変更履歴・TODO |

スタック固有の話はここに入れない。
- バニラ TS（FastAPI 配信・Custom Element・バンドルしない）→ `html/`（`js/バニラTS方針.md`・`tooling/tsc運用.md`・`js/エンドポイント.md` ほか、`frontend/**` スコープ）
- Next.js（App Router・Server Actions・Zod・Drizzle 等）→ `next/`（`app/**` スコープ）
