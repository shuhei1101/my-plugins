---
paths:
  - "**/app/(authenticated)/**/*ListScreen.tsx"
---

# {Feature}ListScreen.tsx — 一覧 Client Component

`'use client'` 必須。URL state + TanStack Query + リスト描画。

---

## 必須テンプレ

```tsx
'use client'

import Link from "next/link"
import { Button } from "@/app/(shared)/components/ui/button"
import { Skeleton } from "@/app/(shared)/components/ui/skeleton"
import { ScreenWrapper } from "@/app/(shared)/components/ScreenWrapper"
import { PageHeader } from "@/app/(shared)/components/PageHeader"
import { EmptyState } from "@/app/(shared)/components/EmptyState"
import { Pagination } from "@/app/(shared)/components/Pagination"
import { RESOURCE_URL } from "@/app/(shared)/endpoints"

import { ResourceFilterBar } from "./components/ResourceFilterBar"
import { ResourceCard } from "./components/ResourceCard"
import { ResourceSortMenu } from "./components/ResourceSortMenu"
import { useResources } from "./hooks/useResources"
import { useResourceListUrlState } from "./hooks/useResourceListUrlState"

import type { fetchResources, ResourceSearchParams } from "@/app/api/v{N}/resources/query"

type Props = {
  initial: Awaited<ReturnType<typeof fetchResources>>
  initialParams: ResourceSearchParams
}

/** リソース一覧画面 */
export const ResourceListScreen = ({ initial, initialParams }: Props) => {
  const { filter, sort, page, pageSize, setFilter, setSort, setPage } = useResourceListUrlState()
  const { rows, totalRecords, isFetching } = useResources({
    filter, sort, page, pageSize, initialData: initial,
  })

  const maxPage = Math.ceil(totalRecords / pageSize)
  const empty = !isFetching && rows.length === 0

  return (
    <ScreenWrapper>
      <PageHeader
        title="リソース一覧"
        actions={
          <Button asChild>
            <Link href={RESOURCE_URL.new}>新規作成</Link>
          </Button>
        }
      />

      <ResourceFilterBar filter={filter} onChange={setFilter} />
      <ResourceSortMenu sort={sort} onChange={setSort} />

      {isFetching ? (
        <div className="grid grid-cols-3 gap-4">
          {Array.from({ length: 9 }).map((_, i) => <Skeleton key={i} className="h-32" />)}
        </div>
      ) : empty ? (
        <EmptyState message="該当するリソースがありません" action={
          <Button variant="outline" onClick={() => setFilter({ name: undefined, tags: [], categoryId: undefined })}>
            フィルタをクリア
          </Button>
        } />
      ) : (
        <div className="grid grid-cols-3 gap-4">
          {rows.map((r) => <ResourceCard key={r.resource.id} resource={r} />)}
        </div>
      )}

      <Pagination value={page} total={maxPage} onChange={setPage} />
    </ScreenWrapper>
  )
}
```

---

## ルール

- **`'use client'`** 必須（先頭）。省略すると動かない
- props で **Server から `initial` データ + `initialParams`** を受け取る。クライアント側初回 fetch は FOUC が出るので禁止
- URL state hook（`useXxxListUrlState`）と data hook（`useXxxs`）を **並列に呼ぶ**。フィルタ・ソート・ページは `useState` で持たず URL state へ
- ローディングは `<Skeleton>`、空は `<EmptyState>` を必ず描画（空状態を描かないと白画面になる）
- 詳細遷移は `<Link href={RESOURCE_URL.view(id)}>` で URL 定数経由（ハードコード禁止）
- `Pagination` は shadcn の薄いラッパー（`コンポーネントカタログ.md` 参照）

## hook の依存

- `useResourceListUrlState` — URL クエリ ↔ state（`frontend/useUrlStateパターン.md`）
- `useResources` — TanStack Query で再取得（`frontend/useQueryパターン.md`）

## 関連 references

- `frontend/一覧ページ-tsx.md` — Server Component 側
- `frontend/useQueryパターン.md`
- `frontend/useUrlStateパターン.md`
- `frontend/コンポーネントカタログ.md` — 共通コンポーネント
- `frontend/空状態.md`
- `frontend/スクリーンラッパー.md`
- `frontend/ページヘッダー.md`
