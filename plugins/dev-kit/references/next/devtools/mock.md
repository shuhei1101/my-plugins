# Next.js App Router — Mocking (MSW)

> **対象**: 開発中・テスト中の API モック。MSW で fetch をネットワークレイヤで intercept する。

---

## なぜ MSW

- アプリのコードを変えずに API レスポンスを差し替えできる
- ブラウザ Service Worker (dev) と Node.js (test) の両方で動作
- 同じ handler 定義を Storybook・Vitest・Playwright で再利用
- バックエンドが未完成でも UI を開発できる

---

## セットアップ

```bash
pnpm add -D msw
```

```bash
# Service Worker を public/ に配置
pnpm dlx msw init public/ --save
```

```ts
// mocks/handlers.ts
import { http, HttpResponse } from "msw"

export const handlers = [
  http.get("/api/v1/resources", () => {
    return HttpResponse.json({
      data: [{ id: "r1", name: "Mock Resource" }],
      meta: { totalRecords: 1, page: 1, pageSize: 20 },
    })
  }),

  http.get("/api/v1/resources/:id", ({ params }) => {
    return HttpResponse.json({
      data: { id: params.id, name: "Mock Detail", canEdit: true },
    })
  }),

  http.post("/api/v1/resources", async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json({ data: { id: "new-id" } }, { status: 201 })
  }),

  http.patch("/api/v1/resources/:id", async () => {
    return new HttpResponse(null, { status: 204 })
  }),

  http.delete("/api/v1/resources/:id", () => {
    return new HttpResponse(null, { status: 204 })
  }),
]
```

---

## ブラウザ（dev mode）で有効化

```ts
// mocks/browser.ts
import { setupWorker } from "msw/browser"
import { handlers } from "./handlers"

export const worker = setupWorker(...handlers)
```

```tsx
// app/(shared)/providers/MswProvider.tsx
'use client'

import { useEffect, useState } from "react"

export const MswProvider = ({ children }: { children: React.ReactNode }) => {
  const [ready, setReady] = useState(process.env.NEXT_PUBLIC_API_MOCKING !== "enabled")

  useEffect(() => {
    if (process.env.NEXT_PUBLIC_API_MOCKING !== "enabled") return
    ;(async () => {
      const { worker } = await import("@/mocks/browser")
      await worker.start({ onUnhandledRequest: "bypass" })
      setReady(true)
    })()
  }, [])

  if (!ready) return null
  return <>{children}</>
}
```

```bash
# .env.local
NEXT_PUBLIC_API_MOCKING=enabled
```

---

## Node.js（test mode）で有効化

```ts
// tests/helpers/server.ts
import { setupServer } from "msw/node"
import { handlers } from "@/mocks/handlers"

export const server = setupServer(...handlers)
```

```ts
// tests/setup.ts
import { server } from "./helpers/server"

beforeAll(() => server.listen({ onUnhandledRequest: "error" }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

---

## Test 内で handler を上書き

```ts
import { http, HttpResponse } from "msw"
import { server } from "@/tests/helpers/server"

it("API 失敗時にエラー表示", async () => {
  server.use(
    http.get("/api/v1/resources", () => new HttpResponse(null, { status: 500 }))
  )
  // ... テスト
})
```

`afterEach(() => server.resetHandlers())` で上書きが他テストに漏れない。

---

## Storybook で使う

```ts
// .storybook/preview.ts
import { initialize, mswLoader } from "msw-storybook-addon"
import { handlers } from "../mocks/handlers"

initialize()

const preview: Preview = {
  loaders: [mswLoader],
  parameters: {
    msw: { handlers },
  },
}
```

```ts
// Story 個別で handler 上書き
export const Empty: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get("/api/v1/resources", () => HttpResponse.json({ data: [], meta: { totalRecords: 0, page: 1, pageSize: 20 } })),
      ],
    },
  },
}
```

---

## Playwright で MSW を使う

通常 E2E は **本物の API（dev server）** に対して走るので MSW は不要。

ただし「特定のレスポンスを返したい・障害をシミュレート」したい時は `page.route()` で fetch を intercept:

```ts
test("API 500 のときエラー画面", async ({ page }) => {
  await page.route("/api/v1/resources*", (route) => route.fulfill({ status: 500 }))
  await page.goto("/resources")
  await expect(page.getByText("エラーが発生しました")).toBeVisible()
})
```

MSW の handler を共有したいなら `pmcwhirter/playwright-msw` 等の連携ライブラリ。

---

## 設計指針

- **`mocks/handlers.ts` を 1 つの source of truth** にする
- 真のレスポンス形式（封筒 `{ data, meta }` / `{ error }`）に合わせる
- 「成功 / 失敗 / 空 / ネットワーク遅延」のバリエーションを用意
- 各画面で必要なエンドポイントを網羅
- バックエンド未完成時のフロント開発 → handlers を先に書いて UI 開発

---

## アンチパターン

- handler を散在的に書く → `mocks/handlers.ts` に集約
- 開発で MSW、テストでは別 mock → 同じ handlers を共有
- レスポンス形式を間違える → backend の API ルートと同じ封筒を使う
- 永久に MSW で開発 → バックエンドができたら切り替え（フィーチャフラグで）

---

## Constraints

- handler 定義は `mocks/handlers.ts` に集約
- ブラウザ dev は `NEXT_PUBLIC_API_MOCKING=enabled` の時のみ有効化
- Node.js は test setup で起動
- Storybook は `msw-storybook-addon`
- Playwright は本物 API、必要時のみ `page.route()` で intercept
- レスポンス形式は backend の封筒（`{ data, meta }` / `{ error }`）に合わせる
- `onUnhandledRequest: "error"` で漏れを検知（test）
