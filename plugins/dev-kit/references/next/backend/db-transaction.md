# Drizzle — トランザクション規約

トランザクションは **`service.ts` がトランザクション境界** を持つ。

---

## 必須テンプレ

```ts
// service.ts
import { db } from "@/drizzle/db"

export const registerResource = async ({ db, userId, form }) => {
  return await db.transaction(async (tx) => {
    const { id } = await insertResource({ db: tx, record: ... })
    await insertResourceTags({ db: tx, resourceId: id, tags: form.tags })
    await recordTimeline({ db: tx, type: "created", resourceId: id })
    return { id }
  })
}
```

---

## ルール

- **`service.ts` が境界**（route.ts / actions.ts はトランザクションを開かない）
- `db.transaction(async (tx) => { ... })` で囲む
- 中の関数（`insertXxx`, `fetchXxx`）に **`tx` を引数で渡す**（`db.ts` / `query.ts` は `db` 引数で受ける）
- **例外を投げればロールバック**（自動）
- `try` の **外** で `await db.transaction(...)` を書く → catch で `AppError` 判定

```ts
try {
  return await db.transaction(async (tx) => { ... })
} catch (e) {
  if (e instanceof AppError) throw e
  throw new DatabaseError("...")
}
```

---

## ネストしたトランザクション（savepoint）

PostgreSQL は savepoint で nested transaction をサポート。Drizzle の `tx.transaction(...)` で書ける:

```ts
await db.transaction(async (tx) => {
  await op1(tx)
  await tx.transaction(async (innerTx) => {
    await op2(innerTx)    // ここだけロールバックも可能
  })
})
```

使用機会は稀。基本は 1 階層で済む設計に。

---

## トランザクション中で何を呼ぶか

| 呼んでいい | 呼ばない |
|---|---|
| `db.ts` の関数（INSERT/UPDATE/DELETE） | 外部 API（fetch、決済等） |
| `query.ts` の関数（SELECT、Lock 取得用） | メール送信 / プッシュ通知 |
| 同一 transaction の他関数 | 他の `service.ts` 関数（呼ぶなら `tx` を渡す） |

外部 API 呼び出しはトランザクション外で。失敗時のロールバックが効かないため。

---

## 並列処理

トランザクション内では **`Promise.all` 禁止**（serial に書く）:

```ts
// ❌ 危険（並列実行で deadlock の可能性）
await db.transaction(async (tx) => {
  await Promise.all([insertA(tx), insertB(tx)])
})

// ✅ シリアル
await db.transaction(async (tx) => {
  await insertA(tx)
  await insertB(tx)
})
```

並列実行が必要なら、トランザクション外で `Promise.all` する（独立した処理に限る）。

---

## ロックの取得（SELECT FOR UPDATE）

```ts
import { sql } from "drizzle-orm"

await db.transaction(async (tx) => {
  // 行ロック取得
  const [row] = await tx.select().from(resources).where(eq(resources.id, id)).for("update")
  if (!row) throw new AppError("not found", 404)

  // ロック中に他人は SELECT FOR UPDATE / UPDATE できない
  await tx.update(resources).set({ count: row.count + 1 }).where(eq(resources.id, id))
})
```

楽観ロック（`updatedAt` 比較）で済むなら不要。在庫減算等で厳密性が必要なときに使う。

---

## 関連 references

- `service-ts.md` — トランザクション境界の置き方
- `db-optimistic-lock.md` — 楽観ロック
- `db-ts.md` — `tx` を受け取る関数の書き方

## 禁止

- `route.ts` / `actions.ts` で `db.transaction` を開く（→ service.ts に移動）
- トランザクション内で外部 API
- トランザクション内で `Promise.all`
- ロールバック後に redirect（→ try の外で）
- トランザクション中の長時間処理（30 秒以上は危険）
