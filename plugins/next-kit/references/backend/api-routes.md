# Next.js App Router — API Route Design

## File structure per resource

Each API resource is a folder under `app/api/` mirroring the URL:

```
app/api/{resource}/
├── route.ts        # Next.js handler (exports GET/POST/PATCH/DELETE)
├── client.ts       # Client-side fetch functions (called from frontend hooks)
├── service.ts      # Business logic (called from route.ts)
├── db.ts           # DB queries (Drizzle ORM, called from service.ts)
└── query.ts        # Query parameter types + Zod schemas for request validation
```

Nested resources follow the same pattern:

```
app/api/{resource}/[id]/
├── route.ts
├── client.ts
├── service.ts
├── db.ts
└── query.ts
```

---

## route.ts — handler pattern

Every handler must be wrapped with `withRouteErrorHandling`.
Parse and validate the request body with Zod before using it.

```ts
// app/api/families/route.ts
import { NextRequest, NextResponse } from "next/server"
import { withRouteErrorHandling } from "@/app/(core)/error/handler/server"
import { getAuthContext } from "@/app/(core)/_auth/withAuth"
import { z } from "zod"
import { logger } from "@/app/(core)/logger"
import { createFamily } from "./service"

export const PostFamilyRequestSchema = z.object({
  name: z.string().min(1),
  displayId: z.string().min(1),
})
export type PostFamilyRequest = z.infer<typeof PostFamilyRequestSchema>

export async function POST(request: NextRequest) {
  return withRouteErrorHandling(async () => {
    logger.info("POST /api/families", { path: request.nextUrl.pathname })

    const { db, userId } = await getAuthContext()
    const body = await request.json()
    const data = PostFamilyRequestSchema.parse(body)

    await createFamily({ db, userId, ...data })

    logger.info("family created", { userId })
    return NextResponse.json({})
  })
}
```

### Handler rules

- Always use `withRouteErrorHandling` — never try/catch manually in route.ts
- Always call `getAuthContext()` for authenticated routes
- Always validate the request body with Zod before using it
- Log at the start of the handler (`logger.info`) and at key steps (`logger.debug`)
- Return `NextResponse.json({})` for success with no body, or `NextResponse.json(data)` with body

---

## client.ts — frontend API function

Client functions are thin wrappers around `fetch`. They are called from frontend hooks (not from components directly).

```ts
// app/api/families/client.ts
import { FAMILY_API_URL } from "@/app/(core)/endpoints"
import { AppError } from "@/app/(core)/error/appError"
import type { PostFamilyRequest } from "./route"
import { logger } from "@/app/(core)/logger"

export const postFamily = async (request: PostFamilyRequest) => {
  logger.debug("postFamily", { displayId: request.displayId })

  const res = await fetch(FAMILY_API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  })

  if (!res.ok) {
    const data = await res.json()
    throw AppError.fromResponse(data, res.status)
  }
}
```

### Client function rules

- Import the request type from `route.ts` — do not duplicate the type
- Use URL constants from `app/(core)/endpoints.ts` — no hardcoded strings
- Throw `AppError.fromResponse()` for non-OK responses
- Log with `logger.debug` at the call start

---

## service.ts — business logic

Contains the business logic called from `route.ts`. Receives `db` and other parameters.

```ts
// app/api/families/service.ts
import type { DB } from "@/drizzle/db"
import { insertFamily } from "./db"

export const createFamily = async ({ db, userId, name, displayId }: {
  db: DB
  userId: string
  name: string
  displayId: string
}) => {
  await insertFamily({ db, userId, name, displayId })
}
```

---

## db.ts — DB queries (Drizzle ORM)

Contains raw Drizzle ORM queries. Only called from `service.ts`.

```ts
// app/api/families/db.ts
import { db as dbClient } from "@/drizzle/db"
import { families } from "@/drizzle/schema"

export const insertFamily = async ({ db, name, displayId }) => {
  await db.insert(families).values({ name, displayId })
}

export const selectFamily = async ({ db, id }) => {
  return db.select().from(families).where(eq(families.id, id)).then(r => r[0])
}
```

---

## query.ts — request/query parameter types

Define query string parameter types and Zod schemas for GET requests:

```ts
// app/api/quests/family/query.ts
import { z } from "zod"

export const FamilyQuestQuerySchema = z.object({
  tags: z.array(z.string()).optional(),
  name: z.string().optional(),
  page: z.coerce.number().default(1),
  pageSize: z.coerce.number().default(20),
})
export type FamilyQuestFilterType = z.infer<typeof FamilyQuestQuerySchema>
```

---

## Constraints

- `route.ts` must always use `withRouteErrorHandling`
- `client.ts` imports request types from `route.ts` — never duplicate
- `db.ts` is only called from `service.ts`, never directly from `route.ts`
- All URL strings in `client.ts` must come from `app/(core)/endpoints.ts`
- Use `logger` in all layers — never `console.log`
