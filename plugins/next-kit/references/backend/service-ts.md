# app/api/v1/{resource}/service.ts

ビジネスロジック層。**トランザクション境界** を持ち、複数の `query.ts` / `db.ts` 関数を組み合わせて 1 つの業務ユニットを実行する。

---

## 必須テンプレ

```ts
import type { Db } from "@/drizzle/db"
import { insertResource, updateResource, deleteResource } from "./db"
import { fetchResource } from "./query"
import { insertResourceTags, deleteResourceTags } from "../tags/db"
import { recordHistory } from "../histories/db"
import type { ResourceFormType } from "@/app/(authenticated)/resources/form"
import { AppError, DatabaseError } from "@/app/(shared)/errors/appError"

/** リソースを新規登録 */
export const registerResource = async ({ db, userId, form }: {
  db: Db
  userId: string
  form: ResourceFormType
}) => {
  try {
    return await db.transaction(async (tx) => {
      const { id } = await insertResource({ db: tx, record: { ...form, createdBy: userId } })
      if (form.tags.length > 0) await insertResourceTags({ db: tx, resourceId: id, tags: form.tags })
      return { id }
    })
  } catch (e) {
    if (e instanceof AppError) throw e
    throw new DatabaseError("リソースの登録に失敗しました。")
  }
}

/** リソースを編集 */
export const editResource = async ({ db, userId, id, form, updatedAt }: {
  db: Db
  userId: string
  id: string
  form: ResourceFormType
  updatedAt: string
}) => {
  try {
    return await db.transaction(async (tx) => {
      await updateResource({
        db: tx, id, updatedAt,
        record: { name: form.name, categoryId: form.categoryId, isPublic: form.isPublic, updatedBy: userId },
      })
      await deleteResourceTags({ db: tx, resourceId: id })
      if (form.tags.length > 0) await insertResourceTags({ db: tx, resourceId: id, tags: form.tags })
    })
  } catch (e) {
    if (e instanceof AppError) throw e
    throw new DatabaseError("リソースの更新に失敗しました。")
  }
}

/** リソースを削除（ハードデリート + 履歴退避） */
export const removeResource = async ({ db, userId, id }: {
  db: Db
  userId: string
  id: string
}) => {
  try {
    return await db.transaction(async (tx) => {
      const current = await fetchResource({ db: tx, userId, id })
      if (!current) throw new AppError("リソースが見つかりません。", 404, "NOT_FOUND")
      await recordHistory({ db: tx, tableName: "resources", recordId: id, snapshot: current, deletedBy: userId })
      await deleteResource({ db: tx, id })
    })
  } catch (e) {
    if (e instanceof AppError) throw e
    throw new DatabaseError("リソースの削除に失敗しました。")
  }
}
```

---

## ルール

- **`db.transaction(async (tx) => { ... })`** でラップ（トランザクション境界）
- 中の関数（`insertXxx` 等）には **`tx` を渡す**（呼び出し元がトランザクションを決める）
- `AppError` 派生（`ClientValueError`, `ClientAuthError`, `VersionConflictError` 等）はそのまま投げる
- それ以外を `DatabaseError` でラップして再投
- 削除時は **`recordHistory` で履歴退避 → `deleteXxx` ハードデリート** の順（`db-history.md` 参照）
- 楽観的ロックの `updatedAt` は呼び出し側から受け取り `updateXxx` に渡す（`db-optimistic-lock.md`）
- 監査が必要なテーブルでは `createdBy` / `updatedBy` を record に含める

## 命名

- 動詞 + 名詞（`registerResource`, `editResource`, `removeResource`, `activatePublicQuest`）
- HTTP メソッドと 1:1 ではない（業務ユニット名で命名）

## 引数の形

オブジェクト引数で受ける（位置引数禁止）:

```ts
// ✅
export const xxx = async ({ db, userId, ... }: { db: Db; userId: string; ... }) => { ... }

// ❌
export const xxx = async (db, userId, ...) => { ... }
```

## ログ規約

```ts
import { logger } from "@/app/(shared)/logger"
const log = logger.create("service:resource")

log.info("registerResource start", { userId })
log.info("registerResource complete", { id, userId })
```

詳細: `shared/logger.md`

## 禁止

- 直接 SQL を書く（`db.ts` / `query.ts` の関数を呼ぶ）
- `route.ts` を import（責務分離違反）
- トランザクションなしで複数テーブル更新
- `try` の外で `db.transaction` を呼ぶ（catch できなくなる）
- 認証コンテキストを内部で取得（呼び出し元から渡す）
