# [id]/ — レコード単位のルーティング

`app/(authenticated)/{feature}/[id]/` 配下の構成。**`[id]/page.tsx` を View 画面そのもの**にする（PR135 で旧 view/ サブルートは廃止）。

---

## 構成

```
app/(authenticated)/{feature}/[id]/
├── page.tsx                       # View (Server Component)
├── {Feature}ViewScreen.tsx        # View (Client Component)
├── components/                    # view/edit 共通
│   └── {Feature}Header.tsx
├── hooks/                         # view/edit 共通
│   └── use{Feature}.ts
└── edit/
    ├── page.tsx                   # Edit (Server Component)
    ├── {Feature}EditScreen.tsx    # Edit (Client Component)
    ├── components/                # edit 専用
    │   └── BasicSettings.tsx
    └── hooks/                     # edit 専用
        └── use{Feature}Form.ts
```

---

## URL マッピング

| URL | ルート | 表示内容 |
|---|---|---|
| `/{feature}/[id]` | `[id]/page.tsx` | **View 画面（読み取り）** |
| `/{feature}/[id]/edit` | `[id]/edit/page.tsx` | **Edit 画面（編集）** |

---

## 権限ガード

「編集権限なしユーザーが `/{feature}/[id]/edit` に直アクセス」した場合:

**選択肢 1**: Edit の `page.tsx` で `redirect`

```tsx
// app/(authenticated)/resources/[id]/edit/page.tsx
import { notFound, redirect } from "next/navigation"
import { fetchResource } from "@/app/api/v1/resources/[id]/query"
import { getAuthContext } from "@/app/(shared)/auth"
import { RESOURCE_URL } from "@/app/(shared)/endpoints"
import { ResourceEditScreen } from "./ResourceEditScreen"

export default async function Page(props: PageProps<'/resources/[id]/edit'>) {
  const { id } = await props.params
  const { db, userId } = await getAuthContext()
  const resource = await fetchResource({ db, userId, id })
  if (!resource) notFound()
  if (!resource.canEdit) redirect(RESOURCE_URL.view(id))    // View に戻す
  return <ResourceEditScreen resource={resource} />
}
```

`fetchResource` の結果を再利用できるのでこちらが推奨。

**選択肢 2**: `proxy.ts` でブロック

軽量チェックなら proxy で。詳細: `backend/proxy.md`

---

## View 画面の詳細

詳細: `frontend/view-page-tsx.md`, `frontend/view-screen-tsx.md`

---

## Edit 画面の詳細

詳細: `frontend/edit-page-tsx.md`, `frontend/edit-screen-tsx.md`

---

## View / Edit 共通の hook

`[id]/hooks/use{Feature}.ts` に置き、両方からインポート:

```ts
// app/(authenticated)/resources/[id]/hooks/useResource.ts
'use client'

import { useQuery } from "@tanstack/react-query"
import { getResource } from "@/app/api/v1/resources/[id]/client"

export const useResource = ({ resourceId, initialData }: {
  resourceId: string
  initialData?: Awaited<ReturnType<typeof getResource>>
}) => {
  return useQuery({
    queryKey: ["resource", resourceId],
    queryFn: () => getResource({ resourceId }),
    initialData,
    enabled: !!resourceId,
    staleTime: 0,
    refetchOnMount: "always",
  })
}
```

View 固有のフィールド（`viewCount` 等）が必要なときだけ View 専用フックを別途作る。

詳細: `frontend/use-query-pattern.md`

---

## View / Edit 共通のコンポーネント

`[id]/components/` に置き、View / Edit の両方からインポート:

```tsx
// app/(authenticated)/resources/[id]/components/ResourceHeader.tsx
'use client'
import { Badge } from "@/app/(shared)/components/ui/badge"

export const ResourceHeader = ({ resource }: { resource: ResourceDetail }) => (
  <div className="flex items-center gap-2">
    <h2 className="text-2xl font-bold">{resource.name}</h2>
    <Badge>{resource.status}</Badge>
  </div>
)
```

---

## 「View がない画面」の扱い

設定画面など、View 不要で Edit のみのフィーチャ:

```
app/(authenticated)/settings/
├── page.tsx                 # ここに直接 SettingsEditScreen を render
├── SettingsEditScreen.tsx
└── form.ts
```

`[id]/page.tsx` パターンに無理に当てはめない。

---

## ルール

- `[id]/page.tsx` は **View 画面そのもの**（PR135、`view/` サブルート廃止）
- 編集は `[id]/edit/page.tsx`
- 権限ガードは Edit `page.tsx` の `redirect` で実装
- view/edit 共通の hook / components は **`[id]/` 直下** に置く
- Edit 専用の hook / components は `[id]/edit/` 配下

## 関連 references

- `frontend/feature-folder.md` — フィーチャ全体構成
- `frontend/view-page-tsx.md`, `frontend/view-screen-tsx.md`
- `frontend/edit-page-tsx.md`, `frontend/edit-screen-tsx.md`
- `frontend/use-query-pattern.md` — 共通 hook
- `backend/proxy.md` — proxy ガード

## 禁止

- `view/` サブルートを作る（PR135 で廃止）
- `[id]/page.tsx` に redirect だけ書く（直接 View Screen を render）
- View 専用フック / コンポーネントを `[id]/` 直下に置く（必ず `view/` 配下 — ただし view/ はないので `[id]/page.tsx` に直接書く or 共通化）
