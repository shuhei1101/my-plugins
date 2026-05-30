# Drizzle — SQL Builder vs Relational Queries

Drizzle は **SQL Builder（低レベル）** と **Relational Queries（高レベル）** の 2 つの API を持つ。本プロジェクトは **SQL Builder を標準**。

---

## SQL Builder（標準）

```ts
const rows = await db.select()
  .from(resources)
  .innerJoin(categories, eq(resources.categoryId, categories.id))
  .leftJoin(resourceTags, eq(resourceTags.resourceId, resources.id))
  .where(eq(resources.isPublic, true))
  .orderBy(desc(resources.createdAt))
  .limit(20)
```

| Pros | Cons |
|---|---|
| 複雑な JOIN・サブクエリを表現できる | 結果が flat な配列（自前で集約） |
| エイリアス・複数 JOIN・並列 SELECT が自然 | コード行数が増える |
| 発行 SQL が想像しやすい | — |
| `Promise.all` でクエリチューニング | — |

---

## Relational Queries（オプション）

```ts
const resource = await db.query.resources.findFirst({
  where: eq(resources.id, id),
  with: {
    category: true,
    tags: true,
  },
})
```

| Pros | Cons |
|---|---|
| 結果が構造化された object | 複雑な JOIN・複数階層が表現しづらい |
| 短く書ける | エイリアス・条件付き JOIN が困難 |
| TypeScript の型が完全 | 内部で複数 SQL を発行することがある |

---

## 使い分け

| ケース | 推奨 |
|---|---|
| 単純な「ID で 1 件取得 + 1 階層 with」 | Relational Query |
| 一覧取得（フィルタ・ソート・ページング） | SQL Builder |
| 複数 JOIN（3+ テーブル） | SQL Builder |
| エイリアス必要（同じテーブルを 2 回 JOIN） | SQL Builder |
| 重複排除（`groupBy`） | SQL Builder |
| 件数 + 行を並列で取る | SQL Builder + `Promise.all` |
| `relations()` を使った自然な書き味が欲しい | Relational Query |

---

## エイリアス（SQL Builder）

```ts
import { alias } from "drizzle-orm/pg-core"

const familyIcons = alias(icons, "family_icons")

const rows = await db.select()
  .from(quests)
  .leftJoin(icons, eq(quests.iconId, icons.id))
  .leftJoin(familyIcons, eq(quests.familyIconId, familyIcons.id))
```

---

## 重複排除パターン（SQL Builder）

`leftJoin` で n:m の関連を join すると親が複製される。`groupBy` + 件数取得で対応:

```ts
// 親 ID 一覧を先に取る（重複なし）
const ids = await db.select({ id: resources.id })
  .from(resources)
  .leftJoin(resourceTags, eq(resourceTags.resourceId, resources.id))
  .where(inArray(resourceTags.name, tags))
  .groupBy(resources.id)
  .limit(20)
  .offset(offset)

// 続いて詳細を取得（join 付き）
const details = await db.select()
  .from(resources)
  .leftJoin(...)
  .where(inArray(resources.id, ids.map((r) => r.id)))
```

複雑だが正確。1 クエリで取りに行くと重複が大量に発生する。

---

## 並列取得

```ts
const [rows, totalRecords] = await Promise.all([
  db.select().from(resources).where(...).limit(20),
  db.select({ value: count() }).from(resources).where(...).then((r) => r[0].value),
])
```

トランザクション内では `Promise.all` 禁止（`db-transaction.md`）。

---

## 結果を構造化する private helper

`query.ts` 内で SQL Builder の flat 結果を構造化 object に変換:

```ts
const buildResourceDetail = (rows: any[]) => {
  const head = rows[0]
  const tags = rows
    .filter((r) => r.resource_tags)
    .reduce((acc, r) => {
      if (!acc.some((t) => t.id === r.resource_tags.id)) acc.push(r.resource_tags)
      return acc
    }, [] as ResourceTagSelect[])
  return {
    resource: head.resources,
    category: head.categories,
    tags,
  }
}
```

`query.ts` 内に置く（`buildXxx` 命名）。

---

## ルール

- 標準は **SQL Builder**
- Relational Query は「単体取得 + 1 階層 with」のみ採用
- 複雑な JOIN は **alias + groupBy + Promise.all** を駆使
- `db.execute(sql.raw(...))` は使わない（SQL Injection の温床）
- 動的 SQL が必要なら `sql\`...\`` テンプレートタグ（パラメータ化される）

## 関連 references

- `query-ts.md`, `db-ts.md` — 具体的な書き方
- `db-relations.md` — relations 定義
- `db-transaction.md` — トランザクション

## 禁止

- `sql.raw()` — SQL Injection の温床
- 高レベル Relational Query を複雑なケースで使う（SQL Builder に切り替える）
- 文字列結合の SQL（`` `SELECT * FROM ${table}` ``）
