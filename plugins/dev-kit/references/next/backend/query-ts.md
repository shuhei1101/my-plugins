# app/api/v1/{resource}/query.ts

読み取り（SELECT）専用ファイル。**SELECT 関数群 + フィルタ Zod スキーマ + 戻り値型** を全てここに集約する。

---

## 必須テンプレ

```ts
import { z } from "zod"
import { and, asc, count, desc, eq, inArray, isNull, like } from "drizzle-orm"
import type { Db } from "@/drizzle/db"
import {
  resources, type ResourceSelect,
  categories, type CategorySelect,
  resourceTags, type ResourceTagSelect,
} from "@/drizzle/schema"
import { QueryError } from "@/app/(shared)/errors/appError"
import { calculatePagination } from "./dbHelper"

// ----- フィルタ / ソート / 検索パラメータ -----

/** リソースフィルタ */
export const ResourceFilterSchema = z.object({
  name: z.string().optional(),
  tags: z.array(z.string()).default([]),
  categoryId: z.string().optional(),
})
export type ResourceFilter = z.infer<typeof ResourceFilterSchema>

/** ソート */
export const ResourceSortSchema = z.object({
  column: z.enum(["name", "createdAt", "updatedAt"]).default("createdAt"),
  order: z.enum(["asc", "desc"]).default("desc"),
})
export type ResourceSort = z.infer<typeof ResourceSortSchema>

/** 検索パラメータ全体（pagination 込み） */
export const ResourceSearchParamsSchema = ResourceFilterSchema.merge(ResourceSortSchema).extend({
  page: z.coerce.number().int().min(1).default(1),
  pageSize: z.coerce.number().int().min(1).max(100).default(20),
})
export type ResourceSearchParams = z.infer<typeof ResourceSearchParamsSchema>

// ----- 戻り値型 -----

/** 単体取得の結果 */
export type ResourceDetail = {
  resource: ResourceSelect
  category: CategorySelect | null
  tags: ResourceTagSelect[]
  canEdit: boolean
}

// ----- SELECT 関数 -----

/** 一覧取得 */
export const fetchResources = async ({ db, userId, params }: {
  db: Db
  userId: string
  params: ResourceSearchParams
}) => {
  try {
    const { offset, limit } = calculatePagination({ page: params.page, pageSize: params.pageSize })

    const conditions = []
    if (params.name) conditions.push(like(resources.name, `%${params.name}%`))
    if (params.tags.length > 0) conditions.push(inArray(resourceTags.name, params.tags))
    if (params.categoryId) {
      conditions.push(
        params.categoryId === "null"
          ? isNull(resources.categoryId)
          : eq(resources.categoryId, Number(params.categoryId)),
      )
    }

    const [rows, totalRecords] = await Promise.all([
      db.select()
        .from(resources)
        .leftJoin(categories, eq(resources.categoryId, categories.id))
        .leftJoin(resourceTags, eq(resourceTags.resourceId, resources.id))
        .where(and(...conditions))
        .orderBy(params.order === "asc" ? asc(resources[params.column]) : desc(resources[params.column]))
        .limit(limit)
        .offset(offset),
      db.select({ value: count() })
        .from(resources)
        .where(and(...conditions))
        .then((r) => r[0].value),
    ])

    return { rows: buildResourceList(rows), totalRecords }
  } catch (e) {
    throw new QueryError("リソース一覧の取得に失敗しました。")
  }
}

/** 単体取得 */
export const fetchResource = async ({ db, userId, id }: {
  db: Db
  userId: string
  id: string
}): Promise<ResourceDetail | null> => {
  try {
    const rows = await db.select()
      .from(resources)
      .leftJoin(categories, eq(resources.categoryId, categories.id))
      .leftJoin(resourceTags, eq(resourceTags.resourceId, resources.id))
      .where(eq(resources.id, id))

    if (rows.length === 0) return null

    const result = buildResourceDetail(rows)
    const canEdit = await checkEditPermission({ db, userId, resourceId: id })
    return { ...result, canEdit }
  } catch (e) {
    throw new QueryError("リソースの取得に失敗しました。")
  }
}

// ----- private helpers（SQL 行 → 構造化 object） -----

const buildResourceList = (rows: any[]) => { /* ... */ return [] }
const buildResourceDetail = (rows: any[]) => { /* ... */ return { resource: rows[0].resources, category: rows[0].categories, tags: [] } }
```

---

## ルール

- **SELECT 関数だけ**を置く（INSERT / UPDATE / DELETE は `db.ts`）
- **フィルタ Zod スキーマ + 型** もここで定義（route.ts / client.ts から共有）
- **戻り値型** もここで定義（`ResourceDetail` 等）
- 失敗は **`QueryError`** で包む（`DatabaseError` ではない）
- 引数は **オブジェクト**（`{ db, userId, params }`）
- 関数名は **`fetch{Feature}`** プレフィックス
- 複雑な JOIN・並列取得 (`Promise.all`) を積極利用
- 重複排除のため `groupBy` を使う（必要なら）
- 結果を構造化する private helper（`buildXxx`）は同ファイル内
- `canEdit` 等の権限フラグもサーバーで計算してレスポンスに含める

## 命名

- `fetch{Feature}` — 単体取得
- `fetch{Feature}s` / `fetch{Feature}List` — 一覧
- `fetch{Feature}By{Key}` — 特定キーでの取得
- `count{Feature}` — 件数だけ
- `exists{Feature}` — boolean
- Schema: `{Feature}FilterSchema`, `{Feature}SortSchema`, `{Feature}SearchParamsSchema`
- 戻り値型: `{Feature}Detail`, `{Feature}WithChildren` 等

## なぜ query.ts に集約

CQRS パターン: 読み取りと書き込みを別ファイルにすると、複雑な JOIN 系のロジックが db.ts と混ざらず読みやすい。フックトリガーで「query.ts 編集中」を検出して reference を inject しやすい。

## 関連 references

- Drizzle の API 選択: `drizzle-style.md`
- DB スキーマ: `db-id.md`, `db-relations.md`, `db-enum.md`
- 認証コンテキスト: `auth-context.md`

## 禁止

- INSERT / UPDATE / DELETE を書く（`db.ts` に書く）
- `db.execute(sql.raw(...))` — Builder で書く
- 認証コンテキストを内部で取得（呼び出し元から渡す）
- 生 Drizzle エラーをそのまま外に投げる
- 戻り値型を別ファイルに定義（query.ts 内に集約）
