<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Drizzle — ハードデリート + 履歴テーブル

ソフトデリート（`deletedAt`）は使わず、**削除前にスナップショットを履歴テーブルへ退避してハードデリート**。

---

## なぜハードデリート

- 本番テーブルが軽い（パフォーマンス・index 効率）
- `WHERE deletedAt IS NULL` 忘れによる事故ゼロ
- 履歴は別テーブルに完全保存

---

## 履歴テーブル定義

```ts
// drizzle/schema.ts
import { pgTable, uuid, text, jsonb, timestamp, index } from "drizzle-orm/pg-core"
import { sql } from "drizzle-orm"
import { timestamps } from "./_helpers"

export const histories = pgTable("histories", {
  id: uuid("id").primaryKey().default(sql`gen_random_uuid()`),
  /** 対象テーブル名 */
  tableName: text("table_name").notNull(),
  /** 対象レコード ID */
  recordId: text("record_id").notNull(),
  /** 削除前のスナップショット */
  snapshot: jsonb("snapshot").notNull(),
  /** 削除実行者 user ID */
  deletedBy: text("deleted_by"),
  ...timestamps,
}, (t) => ({
  tableRecordIdx: index("histories_table_record_idx").on(t.tableName, t.recordId),
  deletedByIdx: index("histories_deleted_by_idx").on(t.deletedBy),
}))
```

---

## db.ts（履歴記録用）

```ts
// app/api/v1/histories/db.ts
import type { Db } from "@/drizzle/db"
import { histories } from "@/drizzle/schema"

export const recordHistory = async ({ db, tableName, recordId, snapshot, deletedBy }: {
  db: Db
  tableName: string
  recordId: string
  snapshot: unknown
  deletedBy: string
}) => {
  await db.insert(histories).values({
    tableName,
    recordId,
    snapshot: snapshot as any,
    deletedBy,
  })
}
```

---

## service.ts での使い方

```ts
export const removeResource = async ({ db, userId, id }) => {
  return await db.transaction(async (tx) => {
    // 1. 現在のスナップショットを取得
    const current = await fetchResource({ db: tx, userId, id })
    if (!current) throw new AppError("リソースが見つかりません", 404, "NOT_FOUND")

    // 2. 履歴テーブルに退避
    await recordHistory({
      db: tx,
      tableName: "resources",
      recordId: id,
      snapshot: current,
      deletedBy: userId,
    })

    // 3. ハードデリート
    await deleteResource({ db: tx, id })
  })
}
```

---

## 復元

履歴から再 INSERT で復元:

```ts
export const restoreResource = async ({ db, userId, historyId }) => {
  return await db.transaction(async (tx) => {
    const [hist] = await tx.select().from(histories).where(eq(histories.id, historyId))
    if (!hist) throw new AppError("履歴が見つかりません", 404, "NOT_FOUND")

    const snap = hist.snapshot as ResourceSelect
    await tx.insert(resources).values(snap)
    // 復元したことを履歴に記録（任意）
  })
}
```

---

## 関連テーブルの履歴化

カスケード削除で連鎖したテーブルも履歴化する場合、再帰的に snapshot:

```ts
const removeResourceFully = async ({ db, userId, id }) => {
  return await db.transaction(async (tx) => {
    const resource = await fetchResource({ db: tx, userId, id })
    const tags = await fetchResourceTags({ db: tx, resourceId: id })
    const comments = await fetchResourceComments({ db: tx, resourceId: id })

    await recordHistory({ db: tx, tableName: "resources", recordId: id, snapshot: { resource, tags, comments }, deletedBy: userId })
    await deleteResource({ db: tx, id })   // cascade で tags, comments も消える
  })
}
```

---

## 履歴テーブルのクリーンアップ

長期保存だけ要件ならそのまま、容量問題が出てきたら:

- N 年以上経過した履歴を Cron で削除
- 別 DB / コールドストレージ（S3）に export

詳細: `jobs.md`

---

## ルール

- **削除系の全 service** で履歴記録 → ハードデリート の順
- 履歴記録はトランザクション内（履歴 INSERT 成功 + DELETE 成功で同期）
- `snapshot` は jsonb（柔軟）
- `tableName` + `recordId` で復元時の照合
- `deletedBy` で誰が削除したかを追跡

## 関連 references

- `service-ts.md` — トランザクション境界
- `db-ts.md` — delete 関数
- `db-transaction.md` — トランザクション
- `jobs.md` — 履歴クリーンアップ Cron

## 禁止

- ソフトデリート（`deletedAt IS NULL` WHERE 必須）と混在
- 履歴記録なしのハードデリート（**絶対**）
- 履歴 INSERT を トランザクション外（同期保証なし）
- snapshot を text で持つ（JSON パースの手間、jsonb 必須）
