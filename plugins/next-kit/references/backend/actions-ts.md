# app/(authenticated)/{feature}/actions.ts

Server Action 群。mutation の第一選択。ファイル冒頭に `'use server'` を置けば、export された全関数が Server Action になる。

---

## 必須テンプレ

```ts
'use server'

import { z } from "zod"
import { revalidateTag, refresh } from "next/cache"
import { redirect } from "next/navigation"
import { isRedirectError } from "next/dist/client/components/redirect"
import { ResourceFormSchema } from "./form"
import { getAuthContext } from "@/app/(shared)/auth"
import { registerResource, editResource, removeResource } from "@/app/api/v1/resources/[id]/service"
import { RESOURCE_URL } from "@/app/(shared)/endpoints"
import { logger } from "@/app/(shared)/logger"
import { handleActionError, type ActionResult } from "@/app/(shared)/actions/types"

const log = logger.create("action:resources")

/** 新規作成 */
export async function registerResourceAction(
  input: z.infer<typeof ResourceFormSchema>,
): Promise<ActionResult<{ id: string }>> {
  try {
    const { db, userId } = await getAuthContext()
    const form = ResourceFormSchema.parse(input)
    const { id } = await registerResource({ db, userId, form })
    log.info("registered", { id, userId })
    revalidateTag("resources", "max")
    return { ok: true, data: { id } }
  } catch (e) {
    return handleActionError(e)
  }
}

/** 更新 */
export async function updateResourceAction(
  id: string,
  input: z.infer<typeof ResourceFormSchema>,
  updatedAt: string,
): Promise<ActionResult<void>> {
  try {
    const { db, userId } = await getAuthContext()
    const form = ResourceFormSchema.parse(input)
    await editResource({ db, userId, id, form, updatedAt })
    revalidateTag(`resource:${id}`, "max")
    revalidateTag("resources", "max")
    refresh()
    return { ok: true, data: undefined }
  } catch (e) {
    return handleActionError(e)
  }
}

/** 削除 */
export async function deleteResourceAction(id: string): Promise<ActionResult<void>> {
  let listUrl: string
  try {
    const { db, userId } = await getAuthContext()
    await removeResource({ db, userId, id })
    revalidateTag("resources", "max")
    listUrl = RESOURCE_URL.list
  } catch (e) {
    if (isRedirectError(e)) throw e
    return handleActionError(e)
  }
  redirect(listUrl)    // try の外で redirect（NEXT_REDIRECT 例外を catch しないため）
}
```

---

## ルール

- ファイル先頭に **`'use server'`**
- 戻り値は **`ActionResult<T>`** 形式に統一
- 入力は **必ず Zod で `.parse`**（クライアント信用しない）
- 認証は **`getAuthContext()`**（呼ばないとセキュリティ違反）
- 業務処理は `service.ts` 経由（DB 操作を直接書かない）
- `revalidateTag` は **第 2 引数の cacheLife プロファイル必須**（Next.js 16）
- 必要なら `refresh()` で client router を更新
- `redirect()` は **try の外**、または `isRedirectError(e)` を catch でスキップ

## ファイル配置

- `app/(authenticated)/{feature}/actions.ts` — フィーチャ固有
- `app/(shared)/actions/{name}.ts` — 複数フィーチャ共通（auth 等）

## 命名

- `{verb}{Feature}Action` プレフィックス（`registerResourceAction`, `updateResourceAction`, `deleteResourceAction`）
- 動詞は `register` / `update` / `delete` / `activate` / `archive` / `publish` 等

## ActionResult 型

```ts
// app/(shared)/actions/types.ts
export type ActionResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: { code: string; message: string; field?: string } }
```

## クライアントから呼ぶ

詳細: `frontend/use-action-state.md`（クライアント側パターン）

```tsx
'use client'
import { useTransition } from "react"
import { toast } from "sonner"

const [isPending, startTransition] = useTransition()

startTransition(async () => {
  const result = await updateResourceAction(id, data, updatedAt)
  if (!result.ok) {
    if (result.error.field) form.setError(result.error.field as any, { message: result.error.message })
    else toast.error(result.error.message)
    return
  }
  toast.success("更新しました")
})
```

## 関連 references

- `service-ts.md` — 業務ロジック
- `caching.md` — cacheLife / revalidateTag / updateTag
- `error-action-handler.md` — handleActionError 実装
- `auth-context.md` — getAuthContext

## 禁止

- `'use server'` なしで export
- 入力の Zod パースを省略
- `getAuthContext()` を呼ばずに DB 触る
- service.ts を経由せず `db.ts` / `query.ts` を直接呼ぶ
- `revalidateTag` の cacheLife プロファイル省略（Next.js 16 で型エラー）
- `try` 内で `redirect()` を呼んで catch で `NEXT_REDIRECT` を握り潰す
- 外部公開向けの API ロジックをここに書く（→ `route.ts`）
