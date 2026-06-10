---
paths:
  - "**/app/(authenticated)/**/*.tsx"
  - "**/app/(authenticated)/**/*ListScreen.tsx"
  - "**/app/(authenticated)/**/*ViewScreen.tsx"
  - "**/app/(authenticated)/*/[id]/page.tsx"
  - "**/app/(authenticated)/*/page.tsx"
---

# Next.js App Router — Server vs Client Component

> **方針**: データ取得・初期表示・SEO が重要な箇所は **Server Component**、ユーザーインタラクションは **Client Component**。両者を `page.tsx`（Server）と `XxxScreen.tsx`（Client）で物理分離する。

---

## 決定フロー

```
そのコンポーネントは...
  ├─ DB / API / ファイルから直接データを取りたい → Server
  ├─ async function として書きたい → Server
  ├─ Server-only シークレット（DB URL 等）にアクセスする → Server
  ├─ SEO 用 metadata を生成する → Server
  ├─ useState / useEffect / useRef を使う → Client（'use client'）
  ├─ ブラウザ API（window, localStorage, navigator）を使う → Client
  ├─ イベントハンドラ（onClick, onChange）を持つ → Client
  ├─ React Context provider / consumer → Client
  └─ TanStack Query / Zustand / react-hook-form → Client
```

両方の性質を持つ画面は、Server Component を **外殻**、Client Component を **コア** にして組み合わせる。

---

## 標準パターン: page.tsx (Server) + XxxScreen.tsx (Client)

### 一覧画面

```tsx
// app/(authenticated)/resources/page.tsx — Server Component
import { ResourceListScreen } from "./ResourceListScreen"
import { fetchResources } from "@/app/api/v{N}/resources/query"
import { getAuthContext } from "@/app/(shared)/auth"

export default async function Page(props: PageProps<'/resources'>) {
  const sp = await props.searchParams
  const { db, userId } = await getAuthContext()
  const initial = await fetchResources({
    db,
    userId,
    params: ResourceFilterSchema.parse(sp),
  })
  return <ResourceListScreen initial={initial} />
}
```

```tsx
// app/(authenticated)/resources/ResourceListScreen.tsx — Client Component
'use client'

import { useResources } from "./hooks/useResources"
import { useResourceListUrlState } from "./hooks/useResourceListUrlState"

type Props = {
  initial: Awaited<ReturnType<typeof fetchResources>>
}

export const ResourceListScreen = ({ initial }: Props) => {
  const urlState = useResourceListUrlState()
  const { resources, isLoading } = useResources({
    ...urlState,
    initialData: initial,   // Server から受け取った初期データを TanStack Query に流す
  })
  // ... interactive UI
}
```

ポイント:
- Server で初回データを取り、Client にプロップス経由で渡す
- Client は `useQuery` の `initialData` で hydrate → クライアントナビゲーション後の再取得はキャッシュから即時
- Server の関数を直接呼ぶ（API ルートを経由しない、`api/v{N}/{resource}/query.ts` の関数を import）

---

### 詳細画面（View）

```tsx
// app/(authenticated)/resources/[id]/page.tsx — Server Component
import { notFound } from "next/navigation"
import { ResourceViewScreen } from "./ResourceViewScreen"
import { fetchResource } from "@/app/api/v{N}/resources/[id]/query"

export default async function Page(props: PageProps<'/resources/[id]'>) {
  const { id } = await props.params
  const { db, userId } = await getAuthContext()
  const resource = await fetchResource({ db, userId, id })
  if (!resource) notFound()
  return <ResourceViewScreen resource={resource} />
}
```

```tsx
// app/(authenticated)/resources/[id]/ResourceViewScreen.tsx — Client Component
'use client'

import { Button } from "@/app/(shared)/components/ui/button"
import { RESOURCE_URL } from "@/app/(shared)/endpoints"
import Link from "next/link"

type Props = {
  resource: Awaited<ReturnType<typeof fetchResource>>
}

export const ResourceViewScreen = ({ resource }: Props) => {
  return (
    <ScreenWrapper>
      <PageHeader title={resource.name} actions={
        resource.canEdit && (
          <Button asChild><Link href={RESOURCE_URL.edit(resource.id)}>編集</Link></Button>
        )
      } />
      {/* ... read-only UI */}
    </ScreenWrapper>
  )
}
```

---

### 編集画面（Edit）

```tsx
// app/(authenticated)/resources/[id]/edit/page.tsx — Server Component
import { notFound, redirect } from "next/navigation"
import { ResourceEditScreen } from "./ResourceEditScreen"
import { fetchResource } from "@/app/api/v{N}/resources/[id]/query"
import { RESOURCE_URL } from "@/app/(shared)/endpoints"

export default async function Page(props: PageProps<'/resources/[id]/edit'>) {
  const { id } = await props.params
  const { db, userId } = await getAuthContext()
  const resource = await fetchResource({ db, userId, id })
  if (!resource) notFound()
  if (!resource.canEdit) redirect(RESOURCE_URL.view(id))
  return <ResourceEditScreen resource={resource} />
}
```

```tsx
// app/(authenticated)/resources/[id]/edit/ResourceEditScreen.tsx — Client Component
'use client'

import { useResourceForm } from "./hooks/useResourceForm"
import { updateResourceAction } from "@/app/(authenticated)/resources/actions"
// ... form UI with shadcn <Form>
```

---

## Server Component で使える機能

- `async function`（`await fetch`, `await db.query.xxx`, `await getAuthContext()`）
- `notFound()`, `redirect()`
- `cookies()`, `headers()`, `draftMode()` (Next.js 16: 全て `await` 付き)
- Streaming, `<Suspense>`
- `cache()` 関数（リクエスト内メモ化）
- Cache Components の `"use cache"` ディレクティブ

---

## Client Component で使える機能

- `useState`, `useEffect`, `useRef`, `useReducer`, `useMemo`, `useCallback`
- `useRouter`, `usePathname`, `useSearchParams`, `useParams`
- `useQuery`, `useMutation`（TanStack Query）
- `useForm`（react-hook-form）
- `<Form>` `<Dialog>` 等の shadcn/ui コンポーネント
- イベントハンドラ
- Browser API

`'use client'` を付けるとそのモジュール以降は全部クライアントに送られる（境界）。

---

## Server / Client 境界の引き方

ベストプラクティス: **`'use client'` は可能な限り深い葉に置く**。

```
RootLayout (Server)
└── (authenticated)/layout.tsx (Server)
    └── page.tsx (Server, データ取得)
        └── XxxScreen.tsx (Client, インタラクション)
            ├── components/FilterBar.tsx (Client)
            └── components/ResourceCard.tsx (Client)
```

「親が Server, 子が Client」は OK。「親が Client, 子で `'use client'` 削除して Server に戻す」は **不可**（Client tree 内は全部 Client）。

ただし、Client コンポーネントが **children として Server Component を受け取る** ことは可能:

```tsx
'use client'
export const Card = ({ children }: { children: React.ReactNode }) => {
  const [open, setOpen] = useState(false)
  return <div onClick={() => setOpen(!open)}>{children}</div>
}
```

```tsx
// page.tsx (Server) で Server 子を渡せる
<Card>
  <ServerOnlyContent />
</Card>
```

---

## Server Actions の境界

Client Component から Server Actions を呼ぶのは正常な使い方:

```tsx
'use client'

import { useTransition } from "react"
import { updateResourceAction } from "../actions"

export const EditScreen = ({ resource }: Props) => {
  const [isPending, startTransition] = useTransition()
  const onSubmit = (data: ResourceFormType) => {
    startTransition(async () => {
      await updateResourceAction(resource.id, data)
    })
  }
}
```

詳細: `backend/server-actions.md`

---

## データの受け渡し

### Server → Client（props 経由）

Server Component で取得したデータを Client Component に props として渡せる。**シリアライズ可能な値** のみ（関数・Date 以外のクラスインスタンスは渡せない）。

```tsx
// Server
const data = await fetchResource({ db, id })

// Client
<ClientScreen data={data} />  // data は JSON.stringify 可能でなければならない
```

Drizzle の `$inferSelect` は plain object なので OK。Date は ISO 文字列に変換するか、`{ mode: "string" }` で timestamp カラムを定義する（quest-pay でこのパターン）。

### Server → Client（初期データ + TanStack Query）

```tsx
// Server で初期データ取得
const initial = await fetchResources({ db })

// Client でハイドレート
<ListScreen initial={initial} />

// Client 内
const { data } = useQuery({
  queryKey: ['resources', filter],
  queryFn: () => getResources({ filter }),
  initialData: initial,
})
```

---

## SEO / Metadata は Server Component で

```tsx
// app/(authenticated)/resources/[id]/page.tsx
import type { Metadata } from "next"

export async function generateMetadata(props: PageProps<'/resources/[id]'>): Promise<Metadata> {
  const { id } = await props.params
  const resource = await fetchResource({ db, id })
  return {
    title: resource?.name ?? "リソース",
    description: resource?.description,
    openGraph: { images: [resource?.iconUrl ?? "/og-default.png"] },
  }
}
```

`generateMetadata` は Server Component の機能。Client Component では使えない。詳細: `frontend/SEO.md`
