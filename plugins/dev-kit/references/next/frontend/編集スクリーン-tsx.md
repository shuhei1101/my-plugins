# {Feature}EditScreen.tsx / {Feature}NewScreen.tsx — Edit Client Component

編集・新規作成画面。shadcn `<Form>` + react-hook-form + Zod + Server Action。

---

## 必須テンプレ（Edit）

```tsx
'use client'

import { useTransition } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Form } from "@/app/(shared)/components/ui/form"
import { Button } from "@/app/(shared)/components/ui/button"
import { ScreenWrapper } from "@/app/(shared)/components/ScreenWrapper"
import { PageHeader } from "@/app/(shared)/components/PageHeader"
import { toast } from "sonner"
import { useRouter } from "next/navigation"

import { ResourceFormSchema, type ResourceFormType } from "../../form"
import { updateResourceAction, deleteResourceAction } from "../../actions"
import { ResourceEditLayout } from "./components/ResourceEditLayout"
import { BasicSettings } from "./components/BasicSettings"
import { DetailSettings } from "./components/DetailSettings"
import { useConfirmDialog } from "@/app/(shared)/hooks/useConfirmDialog"

import type { fetchResource } from "@/app/api/v1/resources/[id]/query"

type Props = {
  resource: NonNullable<Awaited<ReturnType<typeof fetchResource>>>
}

/** リソース編集画面 */
export const ResourceEditScreen = ({ resource }: Props) => {
  const router = useRouter()
  const [isPending, startTransition] = useTransition()
  const confirm = useConfirmDialog()

  // フォーム state（サーバー値を default に）
  const form = useForm<ResourceFormType>({
    resolver: zodResolver(ResourceFormSchema),
    defaultValues: {
      name: resource.resource.name,
      tags: resource.tags.map((t) => t.name),
      categoryId: resource.resource.categoryId,
      isPublic: resource.resource.isPublic,
    },
  })

  // 送信処理
  const onSubmit = (data: ResourceFormType) => {
    startTransition(async () => {
      const result = await updateResourceAction(resource.resource.id, data, resource.resource.updatedAt)
      if (!result.ok) {
        if (result.error.field) form.setError(result.error.field as any, { message: result.error.message })
        else toast.error(result.error.message)
        return
      }
      toast.success("更新しました")
      form.reset(data)
    })
  }

  // 削除（確認ダイアログ必須）
  const onDelete = async () => {
    const ok = await confirm({
      title: "削除確認",
      description: `「${resource.resource.name}」を削除します。この操作は取り消せません。`,
      confirmText: "削除",
      variant: "destructive",
    })
    if (!ok) return
    startTransition(async () => {
      const result = await deleteResourceAction(resource.resource.id)
      if (result && !result.ok) toast.error(result.error.message)
      // 成功時は Server Action 内で redirect
    })
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <ResourceEditLayout
          title="リソース編集"
          isLoading={isPending}
          tabs={[
            { value: "basic",   label: "基本",   content: <BasicSettings form={form} /> },
            { value: "details", label: "詳細",   content: <DetailSettings form={form} /> },
          ]}
          actions={
            <>
              <Button type="button" variant="destructive" onClick={onDelete} disabled={isPending}>削除</Button>
              <Button type="submit" disabled={!form.formState.isDirty || isPending}>保存</Button>
            </>
          }
        />
      </form>
    </Form>
  )
}
```

---

## New（新規作成）テンプレ

```tsx
'use client'

import { useTransition } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { useRouter } from "next/navigation"
import { Form } from "@/app/(shared)/components/ui/form"
import { Button } from "@/app/(shared)/components/ui/button"
import { toast } from "sonner"

import { ResourceFormSchema, defaultResourceForm, type ResourceFormType } from "../form"
import { registerResourceAction } from "../actions"
import { RESOURCE_URL } from "@/app/(shared)/endpoints"

export const ResourceNewScreen = () => {
  const router = useRouter()
  const [isPending, startTransition] = useTransition()

  const form = useForm<ResourceFormType>({
    resolver: zodResolver(ResourceFormSchema),
    defaultValues: defaultResourceForm,
  })

  const onSubmit = (data: ResourceFormType) => {
    startTransition(async () => {
      const result = await registerResourceAction(data)
      if (!result.ok) {
        if (result.error.field) form.setError(result.error.field as any, { message: result.error.message })
        else toast.error(result.error.message)
        return
      }
      toast.success("作成しました")
      router.push(RESOURCE_URL.view(result.data.id))
    })
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        {/* ... ResourceEditLayout と同じ */}
      </form>
    </Form>
  )
}
```

---

## ルール

- **`'use client'`** 必須
- Server から `resource`（編集時） or なし（新規）を props で受け取る
- `useForm` + `zodResolver(ResourceFormSchema)` で初期化
- 編集時の `defaultValues` は **サーバーから受け取った値**
- mutation は **Server Action**（`useMutation` ではない）
- **`useTransition`** で `isPending` 管理
- 確認ダイアログは **削除のみ**（登録・更新は不要、PR135、QA-027）
- 削除確認は `useConfirmDialog()` 経由（`window.confirm` 禁止）
- Dirty 判定は **`formState.isDirty`**（PR135、`JSON.stringify` 比較廃止）
- 送信成功後は `form.reset(data)` で dirty を落とす
- 楽観的ロック: `resource.resource.updatedAt` を Server Action に渡す
- 失敗時:
  - `error.field` があればフィールドにエラー表示
  - なければ toast.error
- 成功時:
  - 編集 → toast.success
  - 新規 → toast.success + 詳細画面に router.push

## 関連 references

- `frontend/編集ページ-tsx.md` — Server Component 側
- `frontend/フォーム-ts.md` — Zod schema
- `frontend/フォームコンポーネント.md` — shadcn Form の書き方
- `backend/アクション-ts.md` — Server Action 実装
- `backend/DB楽観的ロック.md` — 楽観的ロック
- `frontend/確認ダイアログ.md` — useConfirmDialog
- `frontend/useActionState.md` — useTransition の使い分け

## 禁止

- `'use client'` 省略
- mutation を `useMutation` + `fetch` 経由（Server Action を優先）
- 確認ダイアログを登録・更新でも出す（削除のみ）
- `window.confirm` を使う
- `JSON.stringify` で dirty 判定
- `updatedAt` を Server Action に渡さない（楽観ロックが効かない）
- 成功 / 失敗 toast を省略
