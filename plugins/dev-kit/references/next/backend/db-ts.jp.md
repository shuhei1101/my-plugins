<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# app/api/v1/{resource}/db.ts

書き込み（INSERT / UPDATE / DELETE）専用ファイル。`service.ts` から呼ばれる。

---

## 必須テンプレ

```ts
import { eq, and } from "drizzle-orm"
import type { Db } from "@/drizzle/db"
import { resources, type ResourceInsert, type ResourceUpdate } from "@/drizzle/schema"
import { DatabaseError, VersionConflictError } from "@/app/(shared)/errors/appError"

/** リソースを挿入 */
export const insertResource = async ({ db, record }: { db: Db; record: ResourceInsert }) => {
  try {
    const [row] = await db.insert(resources).values(record).returning()
    return row
  } catch (e) {
    throw new DatabaseError("リソースの登録に失敗しました。")
  }
}

/** リソースを更新（楽観的ロック付き） */
export const updateResource = async ({ db, id, updatedAt, record }: {
  db: Db
  id: string
  updatedAt: string                    // 楽観ロック用
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

/** リソースを削除（ハードデリート） */
export const deleteResource = async ({ db, id }: { db: Db; id: string }) => {
  try {
    await db.delete(resources).where(eq(resources.id, id))
  } catch (e) {
    throw new DatabaseError("リソースの削除に失敗しました。")
  }
}
```

---

## ルール

- 1 関数 = 1 SQL 文（複数文の組み合わせは `service.ts` で）
- 引数は **オブジェクト** で受ける（`{ db, id, record }`）
- `db` 引数は `Db` 型（`tx` も同じ型なのでトランザクション内でも使える）
- 失敗は **必ず `DatabaseError`** で包む（生の Drizzle error を投げない）
- 楽観的ロック衝突は **`VersionConflictError`** を投げる
- 戻り値:
  - `insertXxx` → `returning()` で row を返す
  - `updateXxx` → `returning()` で row を返す（呼び出し側が利用）
  - `deleteXxx` → void
- DB アクセスは **SQL Builder**（`db.select() / .insert() / .update() / .delete()`）を使う（`drizzle-style.md`）

## 命名

- `insert{Feature}` — INSERT
- `update{Feature}` — UPDATE
- `delete{Feature}` — DELETE
- `upsert{Feature}` — INSERT ON CONFLICT
- `insert{Feature}Tags` — 関連テーブル操作

## バルク操作

```ts
export const insertResourceTags = async ({ db, resourceId, tags }: {
  db: Db
  resourceId: string
  tags: { name: string }[]
}) => {
  try {
    const records = tags.map((t) => ({ resourceId, name: t.name }))
    await db.insert(resourceTags).values(records)
  } catch (e) {
    throw new DatabaseError("タグの登録に失敗しました。")
  }
}

export const deleteResourceTags = async ({ db, resourceId }: { db: Db; resourceId: string }) => {
  try {
    await db.delete(resourceTags).where(eq(resourceTags.resourceId, resourceId))
  } catch (e) {
    throw new DatabaseError("タグの削除に失敗しました。")
  }
}
```

## 関連 references

- 楽観的ロック詳細: `db-optimistic-lock.md`
- ハードデリート + 履歴パターン: `db-history.md`
- Drizzle の API 選択: `drizzle-style.md`
- スキーマ定義: `db-id.md`, `db-timestamps.md`, `db-enum.md`, `db-relations.md`

## 禁止

- 1 関数で複数 SQL（service.ts でトランザクション組む）
- `query.ts` の関数を呼ぶ（読み取りは service.ts から query.ts を呼ぶ）
- 生の Drizzle エラーをそのまま外に投げる
- 楽観ロックなしで update（`updatedAt` チェックを省略しない）
- `db.execute(sql.raw(...))` — SQL Injection の温床、Builder で書く
