---
paths:
  - "**/frontend/**/*.ts"
---

# バニラ TS 方針

このスタック固有（汎用 TS は `html/typescript/` を参照）。

## クラスは Custom Element だけ

関数指向で書く。アロー関数 + クロージャで組み、状態はモジュールスコープ変数かクロージャで持つ。クラスを作るのは Custom Element を定義するときだけ（`html/components/カスタムエレメント.md`）。それ以外でクラスを使わない。

## ランタイムライブラリを足さない

ブラウザに出す依存を増やさない。フレームワーク（React/Vue）・状態管理ライブラリ・UI ライブラリは使わない。外部依存がどうしても必要なときだけ vendoring する（`html/shared/vendor.md`）。dev ツール（tsc / eslint / vitest 等）は別（`html/tooling/tsc運用.md`）。

## API 型は生成物から参照する

バックエンド FastAPI の型は openapi から生成した `shared/api/schema.d.ts` を `import type` で引く（手書きしない。`html/js/api層.md`）。

```ts
import type { components } from "shared/api/schema"
type ConfigResponse = components["schemas"]["ConfigResponse"]
```

例外は握りつぶさない（`html/core/エラーは握りつぶさない.md`）。
