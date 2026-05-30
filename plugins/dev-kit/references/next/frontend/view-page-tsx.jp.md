<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# app/(authenticated)/{feature}/[id]/page.tsx — View Server Component

レコード詳細（読み取り）のエントリポイント。`[id]/page.tsx` は **View 画面そのもの**（PR135、`view/` サブルート廃止）。

---

## 必須テンプレ

```tsx
// app/(authenticated)/resources/[id]/page.tsx
import { notFound } from "next/navigation"
import { ResourceViewScreen } from "./ResourceViewScreen"
import { fetchResource } from "@/app/api/v1/resources/[id]/query"
import { getAuthContext } from "@/app/(shared)/auth"

export default async function Page(props: PageProps<'/resources/[id]'>) {
  const { id } = await props.params
  const { db, userId } = await getAuthContext()
  const resource = await fetchResource({ db, userId, id })
  if (!resource) notFound()
  return <ResourceViewScreen resource={resource} />
}
```

---

## SEO（generateMetadata）

```tsx
import type { Metadata } from "next"

export async function generateMetadata(props: PageProps<'/resources/[id]'>): Promise<Metadata> {
  const { id } = await props.params
  const { db, userId } = await getAuthContext()
  const resource = await fetchResource({ db, userId, id })
  return {
    title: resource?.resource.name ?? "リソース",
    description: resource?.resource.description ?? undefined,
    openGraph: {
      title: resource?.resource.name,
      images: resource?.resource.iconUrl ? [{ url: resource.resource.iconUrl }] : [],
    },
  }
}
```

詳細: `frontend/seo.md`

---

## not-found.tsx

同階層に `not-found.tsx` を置く:

```tsx
// app/(authenticated)/resources/[id]/not-found.tsx
import Link from "next/link"
import { Button } from "@/app/(shared)/components/ui/button"
import { RESOURCE_URL } from "@/app/(shared)/endpoints"

export default function NotFound() {
  return (
    <div className="p-6 text-center space-y-4">
      <h2 className="text-xl font-semibold">リソースが見つかりません</h2>
      <Button asChild><Link href={RESOURCE_URL.list}>一覧に戻る</Link></Button>
    </div>
  )
}
```

詳細: `frontend/not-found-tsx.md`

---

## loading.tsx

```tsx
// app/(authenticated)/resources/[id]/loading.tsx
import { Skeleton } from "@/app/(shared)/components/ui/skeleton"

export default function Loading() {
  return (
    <div className="space-y-4 p-6">
      <Skeleton className="h-8 w-64" />
      <Skeleton className="h-32" />
    </div>
  )
}
```

---

## ルール

- **async function**（Server Component）
- `params` は **`await`** 必須
- 型ヘルパー **`PageProps<'/resources/[id]'>`**
- 取得関数は `query.ts` の `fetchResource` を直接 import
- 該当なし → `notFound()`
- 認証必須（**`getAuthContext()`**）
- `canEdit` フラグはサーバーで計算されてレスポンスに含まれる（`backend/query-ts.md`）

## 権限ガード

ここでは行わない（View は誰でも見られる前提）。
編集は `[id]/edit/page.tsx` で行う（`frontend/edit-page-tsx.md`）。

## 関連 references

- `frontend/view-screen-tsx.md` — Client Screen 側
- `frontend/id-routing.md` — `[id]/` 構成
- `frontend/seo.md` — generateMetadata
- `frontend/not-found-tsx.md`
- `backend/query-ts.md` — fetchResource

## 禁止

- `'use client'` を付ける
- redirect だけのプレースホルダにする（PR135 で view/ 廃止）
- `useState` / `useQuery`
- 取得を API ルート経由（`fetch("/api/v1/...")`）でやる
- `params` を await しない
