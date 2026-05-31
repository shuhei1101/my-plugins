# Drizzle — 楽観的ロック

`updatedAt` 比較で「他のユーザーによる先行更新」を検知する標準パターン。

---

## 必須テンプレ

### db.ts（更新側）

```ts
import { and, eq } from "drizzle-orm"
import { VersionConflictError, DatabaseError } from "@/app/(shared)/errors/appError"

export const updateResource = async ({ db, id, updatedAt, record }: {
  db: Db
  id: string
  updatedAt: string      // クライアントから受け取った「最後に見た」timestamp
  record: ResourceUpdate
}) => {
  try {
    const [row] = await db.update(resources)
      .set({ ...record, updatedAt: new Date().toISOString() })
      .where(and(eq(resources.id, id), eq(resources.updatedAt, updatedAt)))
      .returning()

    if (!row) throw new VersionConflictError("他のユーザーによって更新されています。")
    return row
  } catch (e) {
    if (e instanceof VersionConflictError) throw e
    throw new DatabaseError("リソースの更新に失敗しました。")
  }
}
```

### service.ts（呼び出し側）

```ts
export const editResource = async ({ db, userId, id, form, updatedAt }) => {
  return await db.transaction(async (tx) => {
    await updateResource({ db: tx, id, updatedAt, record: { ... } })
  })
}
```

### actions.ts（クライアントから `updatedAt` を受け取る）

```ts
export async function updateResourceAction(
  id: string,
  input: ResourceFormType,
  updatedAt: string,
): Promise<ActionResult<void>> {
  try {
    const { db, userId } = await getAuthContext()
    await editResource({ db, userId, id, form: input, updatedAt })
    return { ok: true, data: undefined }
  } catch (e) {
    return handleActionError(e)
  }
}
```

### クライアント側

```tsx
const result = await updateResourceAction(resource.id, data, resource.updatedAt)
if (!result.ok) {
  // VersionConflictError は "CONFLICT" code で返ってくる
  if (result.error.code === "CONFLICT") {
    toast.error("他のユーザーによって更新されています。最新の内容を確認してください。")
    router.refresh()
    return
  }
  toast.error(result.error.message)
}
```

---

## ルール

- **全 update に `updatedAt` 比較必須**（楽観ロックなしの update 禁止）
- `WHERE id = ? AND updatedAt = ?` の **両方一致** が条件
- 一致しない（`returning()` が空）→ **`VersionConflictError`** を投げる
- 更新時に `updatedAt` を **新しい時刻に書き換える**（次の更新の基準に）
- `mode: "string"` で持っているので ISO 文字列比較になる（`DBタイムスタンプ.md`）

---

## バージョン列パターン（並列更新が頻繁な場合）

`updatedAt` ナノ秒精度の問題が懸念される場合、`version: integer` 列を併用:

```ts
export const resources = pgTable("resources", {
  // ...
  /** バージョン — 楽観的ロック用 */
  version: integer("version").notNull().default(1),
  ...timestamps,
})
```

```ts
import { sql } from "drizzle-orm"

const [row] = await db.update(resources)
  .set({
    ...record,
    version: sql`${resources.version} + 1`,
    updatedAt: new Date().toISOString(),
  })
  .where(and(eq(resources.id, id), eq(resources.version, expectedVersion)))
  .returning()
```

両方持つこともできるが、通常は `updatedAt` で十分。

---

## ETag パターン（HTTP API 公開時）

外部公開 API では `ETag` ヘッダ + `If-Match` で:

```ts
// GET response
res.headers.set("ETag", `"${row.updatedAt}"`)

// PATCH 時にクライアントが If-Match: "..." を送る
const ifMatch = request.headers.get("if-match")
// ifMatch を updatedAt として update に渡す
```

internal API では `updatedAt` を JSON body に含めて送る方が簡単。

---

## 関連 references

- `DB-ts.md` — update 関数の書き方
- `サービス-ts.md` — トランザクション境界
- `DBタイムスタンプ.md` — `updatedAt` カラム定義
- `エラークラス.md` — `VersionConflictError`

## 禁止

- `updatedAt` 比較なしの update（**絶対**）
- 楽観ロック衝突を generic `Error` で投げる（`VersionConflictError` 必須）
- 更新時に `updatedAt` を書き換えない（次回ロックが効かない）
- クライアントから `updatedAt` を受け取らずに更新（衝突検知不可）
