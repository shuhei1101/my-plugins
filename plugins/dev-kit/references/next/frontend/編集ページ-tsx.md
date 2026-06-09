---
paths:
  - "**/app/(authenticated)/*/new/page.tsx"
  - "**/app/(authenticated)/*/[id]/edit/page.tsx"
---
<!-- This file is a Japanese mirror of 編集ページ-tsx.md. When updating the English original, update this file too. -->

# app/(authenticated)/{feature}/[id]/edit/page.tsx — Edit Server Component

編集画面のエントリポイント。データ取得 + 権限ガード + Client Screen render。

---

## 必須テンプレ

```tsx
// app/(authenticated)/resources/[id]/edit/page.tsx
import { notFound, redirect } from "next/navigation"
import { ResourceEditScreen } from "./ResourceEditScreen"
import { fetchResource } from "@/app/api/v1/resources/[id]/query"
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

- **async function**（Server Component）
- `params` は **`await`** 必須
- `getAuthContext()` で認証
- 該当なし → `notFound()`
- **編集権限なし → `redirect(VIEW_URL)`**（必ず実装）
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

## 禁止

- `'use client'` を付ける
- 権限チェックを省略（必ず `if (!resource.canEdit) redirect(...)`）
- データ取得を fetch(/api/v1/...) 経由
- redirect 先を URL クエリから取る（オープンリダイレクト脆弱性、`セキュリティ.md`）
- `params` を await しない
