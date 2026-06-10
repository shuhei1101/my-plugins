---
paths:
  - "**/app/(authenticated)/*/[id]/edit/page.tsx"
  - "**/app/(authenticated)/*/new/page.tsx"
---


# app/(authenticated)/{feature}/[id]/edit/page.tsx — Edit Server Component

編集画面のエントリポイント。データ取得 + 権限ガード + Client Screen render。

---

## 必須テンプレ

```tsx
// app/(authenticated)/resources/[id]/edit/page.tsx
import { notFound, redirect } from "next/navigation"
import { ResourceEditScreen } from "./ResourceEditScreen"
import { fetchResource } from "@/app/api/v{N}/resources/[id]/query"
import { getAuthContext } from "@/app/(shared)/auth"
import { RESOURCE_URL } from "@/app/(shared)/endpoints"

export default async function Page(props: PageProps<'/resources/[id]/edit'>) {
  const { id } = await props.params
  const { db, userId } = await getAuthContext()
  const resource = await fetchResource({ db, userId, id })

  if (!resource) notFound()
  if (!resource.canEdit) redirect(RESOURCE_URL.view(id))   // 権限なし → View に戻す

  return <ResourceEditScreen resource={resource} />
}
```

---

## new 用の page.tsx

新規作成画面は `app/(authenticated)/{feature}/new/page.tsx`:

```tsx
// app/(authenticated)/resources/new/page.tsx
import { ResourceNewScreen } from "./ResourceNewScreen"

export default async function Page() {
  return <ResourceNewScreen />
}
```

データ取得なし（空のフォームから始まる）。

---

## ルール

- **async function**（Server Component。`'use client'` を付けない）
- `params` は **`await`** 必須
- `getAuthContext()` で認証。データ取得は `fetch(/api/v{N}/...)` 経由しない
- 該当なし → `notFound()`
- **編集権限なし → `redirect(VIEW_URL)`**（必ず実装）。redirect 先を URL クエリから取らない（オープンリダイレクト脆弱性、`セキュリティ.md`）
- Server で取得した `resource` を Client Screen に渡す

## 権限判定

`canEdit` はサーバーで判定済み（`fetchResource` のレスポンスに含まれる）。クライアントは `redirect` するだけ。

詳細: `backend/クエリ-ts.md`（`canEdit` の計算方法）

## ローディング

同階層に `loading.tsx`:

```tsx
// app/(authenticated)/resources/[id]/edit/loading.tsx
import { Skeleton } from "@/app/(shared)/components/ui/skeleton"

export default function Loading() {
  return (
    <div className="space-y-4 p-6">
      <Skeleton className="h-8 w-48" />
      <Skeleton className="h-64" />
      <Skeleton className="h-12 w-32" />
    </div>
  )
}
```

## 関連 references

- `frontend/編集スクリーン-tsx.md` — Client Screen 側
- `frontend/IDルーティング.md` — `[id]/` 構成
- `backend/クエリ-ts.md` — fetchResource + canEdit
- `backend/認証コンテキスト.md` — getAuthContext
