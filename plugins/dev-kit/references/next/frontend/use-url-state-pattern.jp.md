<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# hooks/use{Feature}UrlState.ts — URL クエリ state hook

タブ・フィルタ・ソート・ページ等を URL クエリと同期させる hook。nuqs 推奨。

---

## 必須テンプレ（nuqs 採用）

```ts
'use client'

import { useQueryState, parseAsString, parseAsInteger, parseAsArrayOf, parseAsStringEnum } from "nuqs"

/** リソース一覧の URL state */
export const useResourceListUrlState = () => {
  const [name, setName] = useQueryState("name", parseAsString.withDefault(""))
  const [tags, setTags] = useQueryState("tag", parseAsArrayOf(parseAsString).withDefault([]))
  const [categoryId, setCategoryId] = useQueryState("categoryId", parseAsString.withDefault(""))
  const [page, setPage] = useQueryState("page", parseAsInteger.withDefault(1))
  const [pageSize, setPageSize] = useQueryState("pageSize", parseAsInteger.withDefault(20))
  const [sortColumn, setSortColumn] = useQueryState("sortColumn", parseAsString.withDefault("createdAt"))
  const [sortOrder, setSortOrder] = useQueryState("sortOrder", parseAsStringEnum(["asc", "desc"]).withDefault("desc"))

  return {
    filter: { name, tags, categoryId },
    sort: { column: sortColumn, order: sortOrder },
    page,
    pageSize,
    setFilter: (f: { name?: string; tags?: string[]; categoryId?: string }) => {
      setName(f.name ?? "")
      setTags(f.tags ?? [])
      setCategoryId(f.categoryId ?? "")
      setPage(1)             // フィルタ変更でページ 1 にリセット
    },
    setSort: (s: { column: string; order: "asc" | "desc" }) => {
      setSortColumn(s.column)
      setSortOrder(s.order)
      setPage(1)
    },
    setPage,
  }
}
```

setup: `app/layout.tsx` に `<NuqsAdapter>` を入れる。

```tsx
// app/layout.tsx
import { NuqsAdapter } from "nuqs/adapters/next/app"

<NuqsAdapter>{children}</NuqsAdapter>
```

---

## nuqs を使わない場合（自前実装）

```ts
'use client'

import { useRouter, usePathname, useSearchParams } from "next/navigation"
import { useCallback, useMemo } from "react"

export const useResourceListUrlState = () => {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  const state = useMemo(() => ({
    filter: {
      name: searchParams.get("name") ?? undefined,
      tags: searchParams.getAll("tag"),
      categoryId: searchParams.get("categoryId") ?? undefined,
    },
    sort: {
      column: searchParams.get("sortColumn") ?? "createdAt",
      order: (searchParams.get("sortOrder") as "asc" | "desc") ?? "desc",
    },
    page: Number(searchParams.get("page") ?? "1"),
    pageSize: Number(searchParams.get("pageSize") ?? "20"),
  }), [searchParams])

  const updateQuery = useCallback((patch: Record<string, string | string[] | null>) => {
    const params = new URLSearchParams(searchParams.toString())
    for (const [k, v] of Object.entries(patch)) {
      if (v === null || v === "") params.delete(k)
      else if (Array.isArray(v)) {
        params.delete(k)
        v.forEach((x) => params.append(k, x))
      } else params.set(k, v)
    }
    router.push(`${pathname}?${params.toString()}`)
  }, [router, pathname, searchParams])

  return {
    ...state,
    setFilter: (f: typeof state.filter) =>
      updateQuery({ name: f.name ?? null, tag: f.tags, categoryId: f.categoryId ?? null, page: "1" }),
    setSort: (s: typeof state.sort) =>
      updateQuery({ sortColumn: s.column, sortOrder: s.order, page: "1" }),
    setPage: (p: number) => updateQuery({ page: String(p) }),
  }
}
```

---

## ルール

- 配置は **`{feature}/hooks/use{Feature}UrlState.ts`**（フィーチャ固有）
- 状態の読み取りと **setter 関数** をオブジェクトで返す
- フィルタ / ソート変更時は **ページ 1 にリセット**（必ず）
- ページ変更はフィルタ・ソートを保持（追加的）
- `useState` で持たない（URL に置く）
- `router.replace` ではなく **`router.push`** がデフォルト（history 残す）
  - 例外: debounced search 等は `router.replace`（履歴汚染防止）
- nuqs を使うとボイラープレートが激減（推奨）

## いつ URL に置く

| 状態 | URL? |
|---|---|
| タブ / フィルタ / ソート / ページ | ✅ |
| 選択中 ID（インライン詳細表示等） | ✅ |
| Modal 開閉（deep link 可能なもの） | ⚠️ |
| Loading / Error UI | ❌ |
| フォーム入力中の値 | ❌ |

PII / フォーム draft / 一時的 UI は URL に置かない。

## 関連 references

- `frontend/list-screen-tsx.md` — URL state hook の利用
- `frontend/use-query-pattern.md` — フィルタを queryKey に含める

## 禁止

- タブ・フィルタ・ページを `useState` で持つ
- フィルタ変更後にページをそのまま（ページ 1 にリセット必須）
- PII を URL に出す
- 高頻度更新（mouse position 等）を URL に出す
