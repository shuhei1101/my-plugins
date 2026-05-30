<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Next.js App Router — Streaming, Suspense, Cache Components

> **Next.js 16** の Cache Components / Partial Pre-Rendering（PPR）・React 19.2 の View Transitions / useEffectEvent を活用したストリーミング設計。

---

## なぜストリーミング

- ページの **静的部分は即座に配信**、動的部分は後追いで埋める
- LCP / TTFB を大幅改善
- ユーザーが「何かが起きている」とすぐ知覚できる
- データ取得をブロックする「全部待ち」を避けられる

---

## `<Suspense>` 境界の設計

```tsx
// app/(authenticated)/dashboard/page.tsx
import { Suspense } from "react"
import { DashboardStats } from "./components/DashboardStats"
import { RecentActivity } from "./components/RecentActivity"
import { Skeleton } from "@/app/(shared)/components/ui/skeleton"

export default async function Page() {
  return (
    <div className="grid grid-cols-2 gap-4">
      <Suspense fallback={<Skeleton className="h-32" />}>
        <DashboardStats />
      </Suspense>

      <Suspense fallback={<Skeleton className="h-32" />}>
        <RecentActivity />
      </Suspense>
    </div>
  )
}
```

各 Suspense 境界の中身は **独立して async で fetch** できる。両方が並列に走り、揃った順にストリーミングされる。

```tsx
// app/(authenticated)/dashboard/components/DashboardStats.tsx
import { getDashboardStats } from "@/app/api/v1/dashboard/query"

export const DashboardStats = async () => {
  const stats = await getDashboardStats({ db })
  return <StatsView stats={stats} />
}
```

---

## `loading.tsx` との関係

```
app/(authenticated)/dashboard/
├── page.tsx           # 内部に Suspense 境界
├── loading.tsx        # page.tsx 全体の fallback
└── components/
    └── DashboardStats.tsx
```

- `loading.tsx` → page 全体のロード中フォールバック（ナビゲーション中）
- `<Suspense>` → page 内部の部分的フォールバック

両方使える。`loading.tsx` でページのスケルトン全体、`<Suspense>` で部分を独立にロードする。

---

## Cache Components（Next.js 16 安定化）

`cacheComponents: true` でオプトイン:

```ts
// next.config.ts
import type { NextConfig } from "next"

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

Cache Components が有効化されると Partial Pre-Rendering（PPR）が標準動作。`"use cache"` ディレクティブで関数レベルでキャッシュ:

```ts
// app/api/v1/categories/query.ts
import { cacheLife, cacheTag } from "next/cache"

export async function getCategories() {
  "use cache"
  cacheLife("max")
  cacheTag("categories")

  return await db.select().from(categories)
}
```

| API | 役割 |
|---|---|
| `"use cache"` | 関数戻り値をキャッシュ |
| `cacheLife(profile)` | キャッシュ寿命プロファイル（`max`, `seconds`, `minutes`, `hours`, `days`, `weeks` etc.） |
| `cacheTag(tag)` | invalidation 用タグ |
| `revalidateTag(tag, profile)` | stale-while-revalidate（即更新ではない） |
| `updateTag(tag)` | 即時 invalidate + refresh（Server Action でのみ使用、read-your-writes） |
| `refresh()` | Client router を更新（Server Action 内） |

詳細: `backend/caching.md`

### PPR の挙動

- 静的レンダリング可能な部分はビルド時にプリレンダ
- 動的な部分（`cookies()` `headers()` `<Suspense>` 内）はリクエスト時にレンダ
- ユーザーは静的部分を即座に受け取り、動的部分はストリームで届く

---

## use() フックでデータをストリームする

React 19 の `use()` で promise を Server Component 内で「待つ」ことができる:

```tsx
import { use } from "react"

export default function Page() {
  const dataPromise = fetchData()   // promise を作るだけ（await しない）
  return (
    <div>
      <h1>タイトル</h1>
      <Suspense fallback={<Skeleton />}>
        <DataView promise={dataPromise} />
      </Suspense>
    </div>
  )
}

const DataView = ({ promise }: { promise: Promise<Data> }) => {
  const data = use(promise)   // ここで初めて待つ → ストリーミング
  return <pre>{JSON.stringify(data)}</pre>
}
```

`use()` は Suspense と組み合わせると並列ストリームに最適。

---

## React 19.2: View Transitions

Next.js 16 + React 19.2 で View Transitions API が利用可能:

```tsx
'use client'

import { ViewTransition } from "react"

<ViewTransition>
  <div className="card">...</div>
</ViewTransition>
```

ナビゲーション間で要素にアニメーション付き transition を付ける。

---

## useEffectEvent（React 19.2）

非リアクティブなロジックを Effect から抜き出す:

```tsx
import { useEffect, useEffectEvent } from "react"

const onAnalytics = useEffectEvent((event: string) => {
  // 最新のクロージャを参照しつつ、依存配列に入れなくて済む
  analytics.track(event, { userId: currentUser.id })
})

useEffect(() => {
  onAnalytics("page_view")
}, [])   // currentUser を依存に入れなくて OK
```

---

## ストリーミングのベストプラクティス

1. **page.tsx を async + 軽量に保つ** — 重い fetch は Suspense 境界内の子コンポーネントに分離
2. **並列 fetch** — `Promise.all([...])` または `<Suspense>` を並列に並べる
3. **fallback はリアルな骨格** — 画面サイズが変わると CLS が悪化するので、`<Skeleton>` で同じ高さに
4. **静的部分は `cacheLife` で長く** — 動的部分は無キャッシュ or 短く
5. **HTML 生成を妨げる要素を避ける** — early return（条件付き notFound 等）は早めに
6. **Cache Components 採用時は `"use cache"` を関数に付ける** — 戻り値が同じならキャッシュヒット

---

## Anti-patterns

- 1 つの `await` で全部の fetch をブロック → ストリームできない
- `<Suspense>` の fallback が CLS を起こす → 高さを揃える
- `cookies()` `headers()` を不必要に呼ぶ → ページ全体が動的化、PPR が効かない
- Client Component を Suspense 境界に置く → Suspense の効果が薄い（fetch は Server Component で）
- 巨大な単一 `<Suspense>` → 細かく分けて段階的にストリーム

---

## Constraints

- 重いデータ取得は **Server Component + `<Suspense>`** で並列ストリーム
- 各 Suspense 境界には CLS を起こさない `<Skeleton>` を fallback に
- 静的部分は `"use cache"` + `cacheLife`、動的部分は無キャッシュ or 短寿命
- `loading.tsx` はページ全体の fallback、`<Suspense>` は内部部分の fallback
- `use()` で promise を待つパターンを並列化に活用
- Cache Components（`cacheComponents: true`）採用は段階的に
- View Transitions は意味のあるアニメだけに使う（過度な装飾を避ける）
