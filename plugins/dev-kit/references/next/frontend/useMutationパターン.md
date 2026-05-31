# hooks/use{Verb}{Feature}.ts — useMutation パターン

mutation 用 hook。**通常は Server Action 直接呼び**で済むが、**楽観更新・複雑な並列・キャンセル** が必要なときに使う。

---

## いつ useMutation を使うか

```
mutation を書きたい
  ├─ シンプル（フォーム送信、削除等）→ Server Action 直接呼び（actions.ts + useTransition）
  └─ 以下のいずれかが必要 → useMutation
      - 楽観更新（useOptimistic でも可だが、複雑なら useMutation）
      - mutation のキャンセル
      - 並列 mutation の管理
      - 細かいリトライ / バックオフ
```

Server Action 直接呼びの詳細: `frontend/useActionState.md`

---

## 必須テンプレ — 楽観更新

```ts
// app/(authenticated)/resources/[id]/hooks/useToggleResourceFavorite.ts
'use client'

import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toggleResourceFavoriteAction } from "../../actions"

/** お気に入りトグル — 楽観 UI 付き */
export const useToggleResourceFavorite = (resourceId: string) => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (next: boolean) => {
      const result = await toggleResourceFavoriteAction(resourceId, next)
      if (!result.ok) throw new Error(result.error.message)
    },
    onMutate: async (next) => {
      // 競合する fetch をキャンセル
      await queryClient.cancelQueries({ queryKey: ["resource", resourceId] })
      // 元の値を退避
      const previous = queryClient.getQueryData(["resource", resourceId])
      // 楽観的に更新
      queryClient.setQueryData(["resource", resourceId], (old: any) => ({ ...old, isFavorite: next }))
      return { previous }
    },
    onError: (_err, _next, context) => {
      // 失敗 → ロールバック
      if (context) queryClient.setQueryData(["resource", resourceId], context.previous)
    },
    onSettled: () => {
      // 成功 / 失敗どちらでも最終的に同期
      queryClient.invalidateQueries({ queryKey: ["resource", resourceId] })
    },
  })
}
```

---

## 通常 mutation テンプレ

楽観更新が不要なら useMutation でもシンプルに:

```ts
'use client'
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { archiveResourceAction } from "../../actions"

export const useArchiveResource = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (resourceId: string) => {
      const result = await archiveResourceAction(resourceId)
      if (!result.ok) throw new Error(result.error.message)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resources"] })
      toast.success("アーカイブしました")
    },
    onError: (e) => toast.error(e.message),
  })
}
```

---

## 「楽観更新」を使っていい用途リスト

PR135 で許可（QA-054）:

✅ いいね / お気に入り
✅ ブックマーク / フォロー
✅ リアクション
✅ トグル状態（is_public 等）

❌ 課金 / 決済
❌ フォーム保存
❌ 重要なデータ作成・削除

---

## ルール

- **第一選択は Server Action 直接呼び**（`useTransition`、`actions.ts`）
- 楽観更新が必要なときだけ useMutation
- mutation エラーは `onError` で toast.error（または `handleAppError`）
- 成功時は `invalidateQueries` でキャッシュ無効化 + toast.success
- 楽観更新は **`onMutate` で snapshot 退避 → `onError` でロールバック → `onSettled` で invalidate**
- Server Action と組み合わせる場合、戻り値が `ActionResult<T>` なので `result.ok` 判定が必要

## 命名

- `use{Verb}{Feature}` — `useToggleResourceFavorite`, `useArchiveResource`
- 動詞は `register` / `update` / `delete` / `archive` / `restore` / `toggle` / `publish` 等

## 関連 references

- `frontend/useActionState.md` — Server Action 直接呼び（標準）
- `frontend/useQueryパターン.md` — 読み取り側
- `backend/アクション-ts.md` — Server Action 定義
- `frontend/クエリクライアントセットアップ.md`

## 禁止

- シンプルな mutation で useMutation を使う（Server Action 直接が簡潔）
- 楽観更新を「許可リスト外」で使う（QA-054）
- `useMutation` で `fetch` を直書きする（Server Action 経由）
- ロールバックを `onMutate` の snapshot なしで実装
