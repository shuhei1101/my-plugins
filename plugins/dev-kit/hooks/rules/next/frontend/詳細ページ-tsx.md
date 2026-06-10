---
paths:
  - "**/app/(authenticated)/*/[id]/page.tsx"
---


# app/(authenticated)/{feature}/[id]/page.tsx — View Server Component

レコード詳細（読み取り）のエントリポイント。`[id]/page.tsx` は **View 画面そのもの**（PR135、`view/` サブルート廃止）。

---

## 必須テンプレ

```tsx
// app/(authenticated)/resources/[id]/page.tsx
import { notFound } from "next/navigation"
import { ResourceViewScreen } from "./ResourceViewScreen"
import { fetchResource } from "@/app/api/v{N}/resources/[id]/query"
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

詳細: `frontend/SEO.md`

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

詳細: `frontend/404-tsx.md`

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

- **async function**（Server Component。`'use client'` / `useState` / `useQuery` を付けない）
- `params` は **`await`** 必須
- 型ヘルパー **`PageProps<'/resources/[id]'>`**
- 取得関数は `query.ts` の `fetchResource` を直接 import（`fetch("/api/v{N}/...")` 経由しない）
- 該当なし → `notFound()`
- 認証必須（**`getAuthContext()`**）
- `canEdit` フラグはサーバーで計算されてレスポンスに含まれる（`backend/クエリ-ts.md`）
- redirect だけのプレースホルダにしない（PR135 で `view/` サブルート廃止、`[id]/page.tsx` が View 本体）

## 権限ガード

ここでは行わない（View は誰でも見られる前提）。
編集は `[id]/edit/page.tsx` で行う（`frontend/編集ページ-tsx.md`）。

## 関連 references

- `frontend/詳細スクリーン-tsx.md` — Client Screen 側
- `frontend/IDルーティング.md` — `[id]/` 構成
- `frontend/SEO.md` — generateMetadata
- `frontend/404-tsx.md`
- `backend/クエリ-ts.md` — fetchResource
