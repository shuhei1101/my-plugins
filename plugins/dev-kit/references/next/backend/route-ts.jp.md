<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# app/api/v1/{resource}/route.ts

HTTP ハンドラ（GET / POST / PATCH / DELETE）。`withRouteErrorHandling` でラップし、認証 → Zod パース → `service.ts` 呼び出しの順に書く。

---

## 必須テンプレ

```ts
import { NextRequest, NextResponse } from "next/server"
import { z } from "zod"
import { withRouteErrorHandling } from "@/app/(shared)/errors/handler/server"
import { getAuthContext } from "@/app/(shared)/auth"
import { logger } from "@/app/(shared)/logger"
import { ResourceFormSchema } from "@/app/(authenticated)/resources/form"
import { ResourceSearchParamsSchema, fetchResources } from "./query"
import { registerResource } from "./service"

const log = logger.create("api:resources")

// GET — 一覧取得（service を経由せず query 直接呼びでも OK）
export async function GET(request: NextRequest) {
  return withRouteErrorHandling(async () => {
    const { db, userId } = await getAuthContext()
    const sp = ResourceSearchParamsSchema.parse(Object.fromEntries(request.nextUrl.searchParams))
    const { rows, totalRecords } = await fetchResources({ db, userId, params: sp })
    return NextResponse.json({
      data: rows,
      meta: { totalRecords, page: sp.page, pageSize: sp.pageSize },
    })
  })
}

// POST — 新規作成
export const PostResourceRequestSchema = z.object({ form: ResourceFormSchema })
export type PostResourceRequest = z.infer<typeof PostResourceRequestSchema>

export async function POST(request: NextRequest) {
  return withRouteErrorHandling(async () => {
    log.info("POST received")
    const { db, userId } = await getAuthContext()
    const body = await request.json()
    const { form } = PostResourceRequestSchema.parse(body)
    const { id } = await registerResource({ db, userId, form })
    log.info("resource registered", { id })
    return NextResponse.json({ data: { id } }, { status: 201 })
  })
}
```

---

## `[id]/route.ts`（PATCH / DELETE）

```ts
import { NextRequest, NextResponse } from "next/server"
import { z } from "zod"
import { withRouteErrorHandling } from "@/app/(shared)/errors/handler/server"
import { getAuthContext } from "@/app/(shared)/auth"
import { ResourceFormSchema } from "@/app/(authenticated)/resources/form"
import { editResource, removeResource } from "./service"
import { fetchResource } from "./query"

export async function GET(_: NextRequest, ctx: RouteContext<'/api/v1/resources/[id]'>) {
  return withRouteErrorHandling(async () => {
    const { id } = await ctx.params
    const { db, userId } = await getAuthContext()
    const resource = await fetchResource({ db, userId, id })
    if (!resource) {
      return NextResponse.json(
        { error: { code: "NOT_FOUND", message: "リソースが見つかりません" } },
        { status: 404 },
      )
    }
    return NextResponse.json({ data: resource })
  })
}

export const PatchResourceRequestSchema = z.object({
  form: ResourceFormSchema,
  updatedAt: z.string(),
})

export async function PATCH(request: NextRequest, ctx: RouteContext<'/api/v1/resources/[id]'>) {
  return withRouteErrorHandling(async () => {
    const { id } = await ctx.params
    const { db, userId } = await getAuthContext()
    const body = await request.json()
    const { form, updatedAt } = PatchResourceRequestSchema.parse(body)
    await editResource({ db, userId, id, form, updatedAt })
    return new NextResponse(null, { status: 204 })
  })
}

export async function DELETE(_: NextRequest, ctx: RouteContext<'/api/v1/resources/[id]'>) {
  return withRouteErrorHandling(async () => {
    const { id } = await ctx.params
    const { db, userId } = await getAuthContext()
    await removeResource({ db, userId, id })
    return new NextResponse(null, { status: 204 })
  })
}
```

---

## ルール

- すべての handler を `withRouteErrorHandling` でラップ（try/catch は書かない）
- 認証必須なら `getAuthContext()` を最初に呼ぶ
- リクエストボディ・クエリは Zod で `.parse`（投げると 400）
- レスポンス封筒: `{ data, meta? }` / `{ error: { code, message, field? } }`
- 成功 (mutation) は `204 No Content` を返す（body なし）
- HTTP メソッド: 新規 = POST、部分更新 = PATCH、全置換 = PUT、削除 = DELETE
- `params` / `searchParams` は **`await`** が必須（Next.js 16）
- `RouteContext<'/api/v1/resources/[id]'>` の型ヘルパーを使う

## ログ規約

```ts
const log = logger.create("api:{resource}.{METHOD}")    // 例: "api:resources.POST"
log.info("...")    // リクエスト到着 / 完了
log.debug("...")   // 途中のステップ
log.error("...")   // 失敗（withRouteErrorHandling が自動 catch するので原則不要）
```

詳細: `shared/logger.md`

## 禁止

- `try` / `catch` を直接書く（`withRouteErrorHandling` 内に書く）
- `db.ts` / `query.ts` を `service.ts` 経由せず POST/PATCH/DELETE で呼ぶ
- レスポンス封筒を破る
- `console.log` で出力
- ハードコードした URL
