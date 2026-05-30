# app/(authenticated)/{feature}/page.tsx — 一覧 Server Component

リスト画面のエントリポイント。Server Component で初期データを取得して Client Screen に渡す。

---

## 必須テンプレ

```tsx
// app/(authenticated)/resources/page.tsx
import { ResourceListScreen } from "./ResourceListScreen"
import { fetchResources, ResourceSearchParamsSchema } from "@/app/api/v1/resources/query"
import { getAuthContext } from "@/app/(shared)/auth"

export default async function Page(props: PageProps<'/resources'>) {
  const sp = await props.searchParams
  const params = ResourceSearchParamsSchema.parse(sp)

  const { db, userId } = await getAuthContext()
  const initial = await fetchResources({ db, userId, params })

  return <ResourceListScreen initial={initial} initialParams={params} />
}
```

---

## ルール

- **async function**（Server Component）
- `params` / `searchParams` は **`await`** 必須（Next.js 16）
- 型ヘルパー **`PageProps<'/resources'>`** を使う
- 取得関数は `app/api/v1/{resource}/query.ts` から直接 import（API ルート経由しない）
- URL クエリは `ResourceSearchParamsSchema.parse(sp)` で **Zod パース**
- Server Component で取得したデータを Client Screen に props で渡す

## SEO（必要に応じて）

```tsx
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "リソース一覧",
  description: "登録されたリソースを一覧表示します。",
}
```

詳細: `frontend/seo.md`

## ローディング表示

同階層に `loading.tsx` を置く（Suspense fallback として自動表示）:

```tsx
// app/(authenticated)/resources/loading.tsx
import { Skeleton } from "@/app/(shared)/components/ui/skeleton"

export default function Loading() {
  return (
    <div className="grid grid-cols-3 gap-4 p-6">
      {Array.from({ length: 9 }).map((_, i) => <Skeleton key={i} className="h-32" />)}
    </div>
  )
}
```

詳細: `frontend/conventions/route-files.md`

## エラー時

同階層の `error.tsx` で catch。詳細: `frontend/error-tsx.md`

## 関連 references

- `frontend/list-screen-tsx.md` — Client Screen 側
- `frontend/conventions/server-vs-client.md` — Server / Client 境界
- `backend/query-ts.md` — fetchResources 実装
- `frontend/url-state.md` — URL クエリの扱い

## 禁止

- `'use client'` を付ける（Server Component を保つ）
- `useState` / `useEffect` を使う（Client Component に分離）
- `useQuery` / `useMutation` を直接呼ぶ
- データ取得を fetch(/api/v1/...) 経由でやる（直接 query.ts の関数を呼ぶ）
- `params` / `searchParams` を await せずに使う（Next.js 16 で型エラー）
