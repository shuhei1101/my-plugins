---
paths:
  - "**/app/(authenticated)/**/*ViewScreen.tsx"
---

# {Feature}ViewScreen.tsx — View Client Component

レコード詳細の表示。`'use client'` 必須。読み取り専用、`useMutation` を持たない。

---

## 必須テンプレ

```tsx
'use client'

import Link from "next/link"
import { Button } from "@/app/(shared)/components/ui/button"
import { ScreenWrapper } from "@/app/(shared)/components/ScreenWrapper"
import { PageHeader } from "@/app/(shared)/components/PageHeader"
import { RESOURCE_URL } from "@/app/(shared)/endpoints"
import { ResourceHeader } from "./components/ResourceHeader"

import type { fetchResource } from "@/app/api/v{N}/resources/[id]/query"

type Props = {
  resource: NonNullable<Awaited<ReturnType<typeof fetchResource>>>
}

/** リソース詳細画面（読み取り） */
export const ResourceViewScreen = ({ resource }: Props) => {
  return (
    <ScreenWrapper>
      <PageHeader
        title={resource.resource.name}
        actions={
          resource.canEdit && (
            <Button asChild>
              <Link href={RESOURCE_URL.edit(resource.resource.id)}>編集</Link>
            </Button>
          )
        }
      />

      <ResourceHeader resource={resource} />

      <div className="space-y-4 mt-4">
        {resource.resource.description && (
          <p className="text-muted-foreground">{resource.resource.description}</p>
        )}
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div className="text-muted-foreground">登録日</div>
          <div>{new Date(resource.resource.createdAt).toLocaleDateString("ja-JP")}</div>
        </div>
      </div>
    </ScreenWrapper>
  )
}
```

---

## ルール

- **`'use client'`** 必須
- Server Component から `resource` props を受け取る（fetch しない）
- 読み取り専用 — `useMutation` / `<form>` を持たない
- 編集ボタンは **`resource.canEdit`** で出し分け（権限はサーバーで判定済み）
- 編集遷移は `<Link href={RESOURCE_URL.edit(id)}>` で URL 定数経由
- ID は `resource.resource.id` のように `query.ts` の戻り値構造に従う

## なぜ Client Component

- リンク・タブ・コラプス等のインタラクションを持つことが多い
- 編集ボタンクリック → 編集画面遷移 → 戻ってきたとき TanStack Query キャッシュを利用可能
- 完全に静的な View なら Server Component にしても良い

## 共通 hook の併用

view/edit 共通の hook（`useResource`）を呼ぶ場合:

```tsx
import { useResource } from "../hooks/useResource"

const { data } = useResource({ resourceId: resource.resource.id, initialData: resource })
```

`initialData` に Server から渡された props を入れて、TanStack Query キャッシュを hydrate。

詳細: `frontend/useQueryパターン.md`

## 関連 references

- `frontend/詳細ページ-tsx.md` — Server Component 側
- `frontend/IDルーティング.md` — `[id]/` 構成
- `frontend/スクリーンラッパー.md`, `frontend/ページヘッダー.md`
- `frontend/useQueryパターン.md`
