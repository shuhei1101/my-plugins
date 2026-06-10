---
paths:
  - "**/hooks/use*Form.ts"
---

# hooks/use{Feature}Form.ts — フォーム state hook

react-hook-form を内包し、Server から取得した値を初期値に流す hook。Edit Screen から使う。

---

## 必須テンプレ

```ts
// app/(authenticated)/resources/[id]/edit/hooks/useResourceForm.ts
'use client'

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { ResourceFormSchema, type ResourceFormType } from "../../../form"
import type { fetchResource } from "@/app/api/v{N}/resources/[id]/query"

type Args = {
  resource: NonNullable<Awaited<ReturnType<typeof fetchResource>>>
}

/** リソース編集フォーム state */
export const useResourceForm = ({ resource }: Args) => {
  return useForm<ResourceFormType>({
    resolver: zodResolver(ResourceFormSchema),
    defaultValues: {
      name: resource.resource.name,
      tags: resource.tags.map((t) => t.name),
      categoryId: resource.resource.categoryId,
      isPublic: resource.resource.isPublic,
    },
  })
}
```

---

## いつ hook 化するか

- フォームの **初期値変換ロジック** が重い、または複数箇所で再利用する
- フォームと一緒に「状態 + helper」をまとめたい

それ以外は **Screen 内で `useForm` を直接呼べば OK**。hook 化は強制ではない。

---

## 非同期に値を流すパターン

Server から取得済みの値を Client で受け取る場合は `defaultValues` で OK。
非同期 fetch する場合は **`useForm({ values })`** を使う:

```ts
const { data } = useQuery({ queryKey: ["resourceForm", id], queryFn: () => getResource({ resourceId: id }) })

const form = useForm<ResourceFormType>({
  resolver: zodResolver(ResourceFormSchema),
  values: data ? {
    name: data.resource.name,
    // ...
  } : undefined,
})
```

`values` が変わると自動的に `reset` される。`formState.isDirty` も正しく動く。

---

## ルール

- 配置は **`{feature}/[id]/edit/hooks/use{Feature}Form.ts`**
- Zod schema は **フィーチャ直下の `form.ts`** から import（`frontend/フォーム-ts.md`）
- `defaultValues` には **サーバー値** を流す
- 非同期に流すなら **`values`** プロパティ
- Dirty 判定は **`form.formState.isDirty`**（`JSON.stringify` 比較は使わない）
- 送信成功後は **`form.reset(data)`** で dirty を落とす

## 関連 references

- `frontend/フォーム-ts.md` — Zod schema 定義
- `frontend/フォームコンポーネント.md` — shadcn `<Form>` で UI 組み立て
- `frontend/編集スクリーン-tsx.md` — 完全な利用例

## 禁止

- 型を手書き（Zod から推論）
- `defaultValues` と `values` を両方使う
