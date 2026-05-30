<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# not-found.tsx — 404 ページ

`notFound()` が呼ばれた時に表示される Server Component。

---

## 実装

```tsx
// app/(authenticated)/resources/[id]/not-found.tsx
import Link from "next/link"
import { Button } from "@/app/(shared)/components/ui/button"
import { RESOURCE_URL } from "@/app/(shared)/endpoints"

export default function NotFound() {
  return (
    <div className="p-6 text-center space-y-4">
      <h2 className="text-xl font-semibold">リソースが見つかりません</h2>
      <p className="text-muted-foreground">削除されたか、URL が間違っている可能性があります。</p>
      <Button asChild>
        <Link href={RESOURCE_URL.list}>一覧に戻る</Link>
      </Button>
    </div>
  )
}
```

---

## ルートレベル `not-found.tsx`

```tsx
// app/not-found.tsx
import Link from "next/link"
import { Button } from "@/app/(shared)/components/ui/button"
import { HOME_URL } from "@/app/(shared)/endpoints"

export default function NotFound() {
  return (
    <div className="p-6 text-center space-y-4">
      <h2 className="text-2xl font-bold">404 — ページが見つかりません</h2>
      <Button asChild><Link href={HOME_URL}>ホームに戻る</Link></Button>
    </div>
  )
}
```

---

## トリガー: notFound()

`page.tsx` で `notFound()` を呼ぶと自動的に最寄りの `not-found.tsx` が表示される:

```tsx
import { notFound } from "next/navigation"

export default async function Page({ params }: PageProps<'/resources/[id]'>) {
  const { id } = await params
  const resource = await fetchResource({ db, id })
  if (!resource) notFound()    // ← ここで not-found.tsx に飛ぶ
  return <ResourceViewScreen resource={resource} />
}
```

---

## ルール

- 配置は `app/not-found.tsx`（ルート）と各サブツリー `not-found.tsx`
- **Server Component**（`'use client'` 不要）
- 戻る先のリンクを必ず用意（`<Link href={...}>`）
- 文言は短く、原因（削除 / URL 違い）を簡潔に説明
- URL は `RESOURCE_URL.*` 経由（hard-code 禁止）

## 関連 references

- `frontend/error-tsx.md` — エラーバウンダリ
- `frontend/conventions/route-files.md`
- `backend/query-ts.md` — fetchXxx の null 返却パターン

## 禁止

- `'use client'` を付ける
- リンクなしの dead-end ページ
- センシティブ情報を露出
