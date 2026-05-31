# Next.js App Router — SEO / Metadata

> **Stack**: Next.js 16 Metadata API、`sitemap.ts`、`robots.ts`、`manifest.ts`、構造化データ。

---

## Metadata API

### 静的 metadata（layout / page）

```tsx
// app/(authenticated)/resources/page.tsx
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "リソース一覧",
  description: "登録されたリソースを一覧表示します。",
}
```

### 動的 metadata（generateMetadata）

```tsx
// app/(authenticated)/resources/[id]/page.tsx
import type { Metadata } from "next"
import { fetchResource } from "@/app/api/v1/resources/[id]/query"
import { getAuthContext } from "@/app/(shared)/auth"

export async function generateMetadata(props: PageProps<'/resources/[id]'>): Promise<Metadata> {
  const { id } = await props.params
  const { db, userId } = await getAuthContext()
  const resource = await fetchResource({ db, userId, id })

  if (!resource) return { title: "リソース", description: "リソースが見つかりません" }

  return {
    title: resource.name,
    description: resource.description ?? `${resource.name} のページ`,
    openGraph: {
      title: resource.name,
      description: resource.description ?? undefined,
      images: resource.iconUrl ? [{ url: resource.iconUrl, width: 1200, height: 630, alt: resource.name }] : [],
      type: "article",
    },
    twitter: {
      card: "summary_large_image",
      title: resource.name,
      description: resource.description ?? undefined,
      images: resource.iconUrl ? [resource.iconUrl] : [],
    },
  }
}
```

> `generateMetadata` は **Server Component の関数**（Client Component には書けない）

### ルートレベル metadata（共通）

```tsx
// app/layout.tsx
import type { Metadata } from "next"

export const metadata: Metadata = {
  metadataBase: new URL("https://example.com"),
  title: {
    template: "%s | Quest Pay",
    default: "Quest Pay",
  },
  description: "Quest Pay — 子供にお金の概念を学ばせる家族向けクエストアプリ",
  applicationName: "Quest Pay",
  authors: [{ name: "Quest Pay Team" }],
  robots: { index: true, follow: true },
  icons: {
    icon: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
  openGraph: {
    siteName: "Quest Pay",
    locale: "ja_JP",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    creator: "@your_account",
  },
}
```

子の `title` は `%s | Quest Pay` のテンプレートに自動的に入る。

---

## sitemap.ts

```tsx
// app/sitemap.ts
import type { MetadataRoute } from "next"
import { db } from "@/drizzle/db"
import { resources } from "@/drizzle/schema"

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const all = await db.select({ id: resources.id, updatedAt: resources.updatedAt }).from(resources)

  const staticPages: MetadataRoute.Sitemap = [
    { url: "https://example.com/", lastModified: new Date(), changeFrequency: "daily", priority: 1 },
    { url: "https://example.com/about", lastModified: new Date(), changeFrequency: "monthly", priority: 0.7 },
  ]

  const dynamicPages: MetadataRoute.Sitemap = all.map((r) => ({
    url: `https://example.com/resources/${r.id}`,
    lastModified: new Date(r.updatedAt),
    changeFrequency: "weekly",
    priority: 0.6,
  }))

  return [...staticPages, ...dynamicPages]
}
```

大量の URL がある場合は `generateSitemaps` で複数 sitemap を出力:

```tsx
// app/products/sitemap.ts
import type { MetadataRoute } from "next"

export async function generateSitemaps() {
  return [{ id: 0 }, { id: 1 }, { id: 2 }]
}

// Next.js 16: id は Promise<string>
export default async function sitemap({ id }: { id: Promise<string> }): Promise<MetadataRoute.Sitemap> {
  const resolvedId = await id
  const start = Number(resolvedId) * 50000
  // ...
}
```

---

## robots.ts

```tsx
// app/robots.ts
import type { MetadataRoute } from "next"

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: "*", allow: "/", disallow: ["/api/", "/error/"] },
    ],
    sitemap: "https://example.com/sitemap.xml",
  }
}
```

---

## manifest.ts（PWA）

PWA 対応するなら `manifest.ts` を置く。詳細: `frontend/PWA.md`

```tsx
// app/manifest.ts
import type { MetadataRoute } from "next"

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Quest Pay",
    short_name: "QuestPay",
    description: "Quest Pay app",
    start_url: "/",
    display: "standalone",
    background_color: "#ffffff",
    theme_color: "#3B82F6",
    icons: [
      { src: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { src: "/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
  }
}
```

---

## opengraph-image.tsx / twitter-image.tsx

Next.js が自動的に動的 OG 画像を生成できる:

```tsx
// app/(authenticated)/resources/[id]/opengraph-image.tsx
import { ImageResponse } from "next/og"
import { fetchResource } from "@/app/api/v1/resources/[id]/query"

export const alt = "Resource"
export const size = { width: 1200, height: 630 }
export const contentType = "image/png"

// Next.js 16: params は Promise
export default async function Image({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const resource = await fetchResource({ db, userId: null, id })

  return new ImageResponse(
    (
      <div style={{ display: "flex", width: "100%", height: "100%", background: "#3B82F6", color: "white", alignItems: "center", justifyContent: "center", fontSize: 64 }}>
        {resource?.name ?? "Resource"}
      </div>
    ),
    { width: 1200, height: 630 }
  )
}
```

`<img>` ベースの簡易レンダリングなので CSS は限定的。Tailwind 一部のみ。

---

## 構造化データ（JSON-LD）

検索エンジンに意味付けを伝える:

```tsx
// app/(authenticated)/resources/[id]/page.tsx
export default async function Page(props: PageProps<'/resources/[id]'>) {
  const { id } = await props.params
  const resource = await fetchResource({ db, id })

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: resource?.name,
    description: resource?.description,
    image: resource?.iconUrl,
    datePublished: resource?.createdAt,
    dateModified: resource?.updatedAt,
  }

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <ResourceViewScreen resource={resource} />
    </>
  )
}
```

---

## icon / apple-icon

```
app/
├── icon.png       # ファビコン（自動）
├── icon.svg       # 同上 SVG
├── apple-icon.png # Apple Touch Icon
```

ファイルを置くだけで Next.js が `<link>` タグを自動生成。

動的に生成する場合:

```tsx
// app/icon.tsx
import { ImageResponse } from "next/og"

export const size = { width: 32, height: 32 }
export const contentType = "image/png"

export default function Icon() {
  return new ImageResponse(
    (<div style={{ background: "#3B82F6", color: "white", width: "100%", height: "100%", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 24 }}>Q</div>),
    { ...size }
  )
}
```

---

## 認証画面の noindex

認証必須エリアは検索対象外:

```tsx
// app/(authenticated)/layout.tsx
import type { Metadata } from "next"

export const metadata: Metadata = {
  robots: { index: false, follow: false },
}
```

または `robots.ts` で `/api/` `/error/` 等を `disallow` リストに。

---

## ベストプラクティス

1. **title はページ固有**、`metadataBase` でルート URL 統一
2. **description は 120-160 字** で要点
3. **OG image は 1200x630 推奨**
4. **動的 OG image は `next/og` で**（外部サービス不要）
5. **構造化データは主要な詳細ページに**（Article / Product / FAQ 等）
6. **認証画面は `noindex`**（誤って公開しない）
7. **`metadataBase` を必ず設定**（相対 URL → 絶対 URL 解決）
8. **multi-locale なら `alternates.languages`**

---

## Constraints

- ルート `layout.tsx` に `metadataBase` 必須
- 動的ページは `generateMetadata` を使う
- OG image は `opengraph-image.tsx` でルートと並べる
- 認証画面は `noindex`
- `sitemap.ts` / `robots.ts` でクローラ制御
- 重要な詳細ページに JSON-LD 構造化データ
- title は短く、description は 120-160 字
- `generateMetadata` は **Server Component の関数**（Client 不可）
