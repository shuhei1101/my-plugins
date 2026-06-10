---
paths:
  - "**/app/(authenticated)/**/*ListScreen.tsx"
  - "**/hooks/use*.ts"
---

# hooks/use{Feature}.ts / use{Feature}s.ts — useQuery パターン

TanStack Query で読み取りデータを取得する hook。

---

## 必須テンプレ（単体取得）

```ts
// app/(authenticated)/resources/[id]/hooks/useResource.ts
'use client'

import { useQuery } from "@tanstack/react-query"
import { getResource } from "@/app/api/v{N}/resources/[id]/client"

type Args = {
  resourceId: string
  initialData?: Awaited<ReturnType<typeof getResource>>
}

/** リソース本体を取得（view / edit 共通） */
export const useResource = ({ resourceId, initialData }: Args) => {
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

---

## 必須テンプレ（一覧取得）

```ts
// app/(authenticated)/resources/hooks/useResources.ts
'use client'

import { useQuery } from "@tanstack/react-query"
import { getResources } from "@/app/api/v{N}/resources/client"
import type { fetchResources, ResourceFilter, ResourceSort } from "@/app/api/v{N}/resources/query"

type Args = {
  filter: ResourceFilter
  sort: ResourceSort
  page: number
  pageSize: number
  initialData?: Awaited<ReturnType<typeof fetchResources>>
}

export const useResources = ({ filter, sort, page, pageSize, initialData }: Args) => {
  const query = useQuery({
    queryKey: ["resources", filter, sort, page, pageSize],
    queryFn: () => getResources({ ...filter, column: sort.column, order: sort.order, page, pageSize }),
    initialData,
    staleTime: 0,
    refetchOnMount: "always",
  })

  return {
    rows: query.data?.data ?? [],
    totalRecords: query.data?.meta?.totalRecords ?? 0,
    isFetching: query.isFetching,
    refetch: query.refetch,
  }
}
```

---

## queryKey 設計

```ts
queryKey: ["resources", filter, sort, page, pageSize]
```

| 要素 | 理由 |
|---|---|
| `"resources"` | namespace（invalidation の prefix） |
| `filter` | 異なるフィルタ = 異なる結果 |
| `sort` | 並び順違い = 別キャッシュ |
| `page`, `pageSize` | 異なる slice |

mutation 後の invalidation:

```ts
queryClient.invalidateQueries({ queryKey: ["resources"] })
```

prefix マッチで全 variant を invalidate。

---

## staleTime デフォルト

グローバル設定は **`staleTime: 0`**（QueryClient 側、`frontend/クエリクライアントセットアップ.md`）。

- 常にサーバーを真実扱い
- 古いデータを見せる事故を防ぐ
- 頻繁にアクセスする一覧でフェッチを抑えたい場合だけ個別 hook で長くする

```ts
useQuery({
  queryKey: ["categories"],
  queryFn: getCategories,
  staleTime: 60 * 60 * 1000,    // マスター系は 1 時間 fresh で OK
})
```

---

## initialData の使い方

Server Component で取得した値を Client Hook の初期値に流す:

```tsx
// page.tsx (Server)
const initial = await fetchResources({ db, userId, params })
return <ListScreen initial={initial} />
```

```tsx
// ListScreen.tsx (Client)
const { rows } = useResources({ ..., initialData: initial })
```

→ 初回 render で即表示、操作後の再フェッチはクライアントから。

---

## エラーハンドリング

```tsx
const { error, data } = useQuery({ ... })
if (error) handleAppError(error, router)
```

または `<error.tsx>` （route boundary）に任せる。

詳細: `shared/エラークライアントハンドラー.md`

---

## 命名

| Pattern | Purpose |
|---|---|
| `use{Feature}` | 単体取得 |
| `use{Feature}s` / `use{Feature}List` | 一覧 |
| `use{Feature}View` | View 専用フィールドがある場合のみ |
| `use{Feature}By{Key}` | 特定キーでの取得 |

---

## ルール

- **1 hook = 1 ファイル**、ファイル名 = export 名
- 先頭に **`'use client'`**
- 戻り値は **オブジェクト**（タプル禁止）
- `initialData` を受け取れるよう Props で許容
- `queryKey` に結果を変える全パラメータを含める
- View / Edit で同じ API を呼ぶなら **`[id]/hooks/useResource.ts`** に共通化（PR135、QA-052）
- `staleTime: 0` を基本に、必要なら個別に伸ばす

## 関連 references

- `frontend/useMutationパターン.md` — 書き込み hook
- `frontend/クエリクライアントセットアップ.md` — QueryClient 設定
- `backend/クエリ-ts.md` — 取得関数（fetchXxx）
- `backend/クライアント-ts.md` — client.ts の fetch wrapper

## 禁止

- `useState` でサーバーデータを抱える
- `queryKey` のパラメータ欠落（フィルタ変更でキャッシュが混ざる）
