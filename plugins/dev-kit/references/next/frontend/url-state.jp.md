<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Next.js App Router — URL-Based Screen State

## 原則

ユーザーが画面で見ているものに影響する state — アクティブタブ、適用中フィルタ、ソート順、ページ、選択中の ID、展開セクション — は URL クエリ string に置く。

メリット:
- URL を貼って他の人に同じ View を見せられる
- ブラウザの戻る/進むが正しく動く
- リフレッシュで同じ状態に戻る
- メール・通知・他アプリからの deep link が機能する

---

## URL に置く / 置かないの基準

| 状態 | URL に? | 理由 |
|---|---|---|
| アクティブタブ | ✅ | 見ている内容の一部 |
| フィルタ（検索・タグ・ステータス） | ✅ | シェア可能 |
| ソート | ✅ | 同上 |
| ページング | ✅ | リフレッシュで保持 |
| 選択された ID（インライン表示時） | ✅ | アイテムへの deep link |
| フォームの draft | ❌ | ノイズ・セキュリティ |
| Loading/Error UI 状態 | ❌ | 一過性 |
| アニメーション・展開 | ❌ | 純粋に視覚 |
| Modal 開閉 | ⚠️ | リンクできるべきなら入れる、そうでなければローカル |

---

## 実装 — 読み取り

Server Component（`searchParams` を直接受け取る、Next.js 16 で `Promise` 化済み）:

```tsx
export default async function Page(props: PageProps<'/resources'>) {
  const sp = await props.searchParams
  const tab    = sp.tab ?? "list"
  const filter = sp.filter ?? ""
  const tags   = Array.isArray(sp.tag) ? sp.tag : sp.tag ? [sp.tag] : []
  const page   = Number(sp.page ?? "1")
  // ...
}
```

Client Component（`useSearchParams`）:

```tsx
'use client'

import { useSearchParams } from "next/navigation"

const searchParams = useSearchParams()

const tab    = searchParams.get("tab")   ?? "list"
const filter = searchParams.get("filter") ?? ""
const tags   = searchParams.getAll("tag")
const page   = Number(searchParams.get("page") ?? "1")
```

`useSearchParams()` は URL 変更で re-render を引き起こす。

---

## 実装 — 書き込み（生 API）

```tsx
'use client'

import { useRouter, usePathname, useSearchParams } from "next/navigation"
import { useCallback } from "react"

const router = useRouter()
const pathname = usePathname()
const searchParams = useSearchParams()

const updateQuery = useCallback((patch: Record<string, string | string[] | null>) => {
  const params = new URLSearchParams(searchParams.toString())
  for (const [key, value] of Object.entries(patch)) {
    if (value === null || value === "") params.delete(key)
    else if (Array.isArray(value)) {
      params.delete(key)
      value.forEach((v) => params.append(key, v))
    } else params.set(key, value)
  }
  router.push(`${pathname}?${params.toString()}`)
}, [router, pathname, searchParams])

// Usage
updateQuery({ tab: "settings" })
updateQuery({ filter: null })
updateQuery({ tag: ["new", "popular"] })
```

### `router.push` vs `router.replace`

| Method | History 追加 | When to use |
|---|---|---|
| `push` | ✅ | デフォルト。戻るで undo |
| `replace` | ❌ | debounced 検索・派生 state など |

---

## 実装 — nuqs 推奨

PR135 で `nuqs` を推奨に追加。型安全な URL state hook で boilerplate を削減できる:

```bash
pnpm add nuqs
```

```tsx
// app/layout.tsx
import { NuqsAdapter } from "nuqs/adapters/next/app"

export default function RootLayout({ children }) {
  return <NuqsAdapter>{children}</NuqsAdapter>
}
```

```ts
'use client'

import { useQueryState, parseAsString, parseAsInteger, parseAsArrayOf, parseAsStringEnum } from "nuqs"

export const useResourceListUrlState = () => {
  const [name, setName] = useQueryState("name", parseAsString.withDefault(""))
  const [tags, setTags] = useQueryState("tag", parseAsArrayOf(parseAsString).withDefault([]))
  const [page, setPage] = useQueryState("page", parseAsInteger.withDefault(1))
  const [sortColumn, setSortColumn] = useQueryState("sortColumn", parseAsString.withDefault("createdAt"))
  const [sortOrder, setSortOrder] = useQueryState("sortOrder", parseAsStringEnum(["asc", "desc"]).withDefault("desc"))

  return {
    filter: { name, tags },
    sort: { column: sortColumn, order: sortOrder },
    page,
    pageSize: 20,
    setFilter: (f) => { setName(f.name ?? ""); setTags(f.tags ?? []); setPage(1) },
    setSort: (s) => { setSortColumn(s.column); setSortOrder(s.order); setPage(1) },
    setPage,
  }
}
```

nuqs を使わない場合は前述の自前実装。

---

## 自前実装の wrap（nuqs を使わない場合）

```ts
// app/(authenticated)/resources/hooks/useResourceListUrlState.ts
'use client'

import { useRouter, usePathname, useSearchParams } from "next/navigation"
import { useCallback, useMemo } from "react"

export const useResourceListUrlState = () => {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  const state = useMemo(() => ({
    tab:    searchParams.get("tab")   ?? "list",
    filter: searchParams.get("filter") ?? "",
    tags:   searchParams.getAll("tag"),
    page:   Number(searchParams.get("page") ?? "1"),
  }), [searchParams])

  const updateQuery = useCallback((patch) => {
    const params = new URLSearchParams(searchParams.toString())
    for (const [k, v] of Object.entries(patch)) {
      if (v === null || v === "") params.delete(k)
      else if (Array.isArray(v)) { params.delete(k); v.forEach((x) => params.append(k, x)) }
      else params.set(k, v)
    }
    router.push(`${pathname}?${params.toString()}`)
  }, [router, pathname, searchParams])

  return {
    ...state,
    setTab:    (v: string)   => updateQuery({ tab: v, page: "1" }),
    setFilter: (v: string)   => updateQuery({ filter: v, page: "1" }),
    setTags:   (v: string[]) => updateQuery({ tag: v, page: "1" }),
    setPage:   (v: number)   => updateQuery({ page: String(v) }),
  }
}
```

Screen は hook 経由でアクセスし、`useRouter` を直接触らない。

---

## Tab integration

```tsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/app/(shared)/components/ui/tabs"

const { tab, setTab } = useResourceListUrlState()

<Tabs value={tab} onValueChange={setTab}>
  <TabsList>
    <TabsTrigger value="list">一覧</TabsTrigger>
    <TabsTrigger value="archive">アーカイブ</TabsTrigger>
  </TabsList>
  <TabsContent value="list">...</TabsContent>
  <TabsContent value="archive">...</TabsContent>
</Tabs>
```

URL: `?tab=archive` — シェア可・履歴対応。

---

## フィルタ変更時はページを 1 にリセット

```ts
setFilter: (v: string) => updateQuery({ filter: v, page: "1" }),
setTags:   (v: string[]) => updateQuery({ tag: v, page: "1" }),
```

ページング変更はフィルタをリセットしない（追加的）。

---

## URL state のバリデーション

外部入力なので Zod で検証:

```ts
import { z } from "zod"

const UrlStateSchema = z.object({
  tab: z.enum(["list", "archive", "shared"]).default("list"),
  page: z.coerce.number().int().min(1).default(1),
  sortOrder: z.enum(["asc", "desc"]).default("desc"),
})

const raw = Object.fromEntries(searchParams.entries())
const state = UrlStateSchema.parse(raw)
```

ガベージ URL（`?tab=hack`）から守り、型付きデフォルトを与える。

---

## 使ってはいけないケース

| Anti-pattern | 理由 |
|---|---|
| フォームの draft | 未確定の値を URL に出さない |
| センシティブなフィルタ値 | PII を URL に入れない（ログ・キャッシュ・Referrer 漏洩） |
| マウス位置・スクロール等の高頻度 state | 履歴を荒らす |
| ナビゲーションでリセットすべきトグル | ローカル state にすべき |

---

## Server Component と URL state

Server Component は `searchParams` を直接受け取れる（Next.js 16 で `Promise`）:

```tsx
export default async function Page(props: PageProps<'/resources'>) {
  const sp = await props.searchParams
  const tab = sp.tab ?? "list"
  return <ResourceListScreen initialTab={tab} />
}
```

Client Component は `useSearchParams` / nuqs で同じ URL を読む。

---

## Constraints

- タブ・フィルタ・ソート・ページは URL（`useState` ではなく）
- 画面別 URL state は `hooks/use{Feature}UrlState.ts` に集約
- 外部入力（URL）は Zod でバリデーション
- フィルタ・ソート変更時はページ 1 にリセット
- デフォルトは `router.push`、debounced は `router.replace`
- フォーム値・PII を URL に入れない
- nuqs を採用するとボイラープレートが激減（PR135 で推奨）
