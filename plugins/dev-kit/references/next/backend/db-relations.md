# drizzle/schema.ts — Relations と Index

外部キー定義、relations、index の付け方。

---

## 外部キーの基本

```ts
import { pgTable, uuid, text, integer, index } from "drizzle-orm/pg-core"
import { relations, sql } from "drizzle-orm"
import { categories } from "./categories"

export const resources = pgTable("resources", {
  id: uuid("id").primaryKey().default(sql`gen_random_uuid()`),
  /** カテゴリ ID（NULL = 未分類） */
  categoryId: integer("category_id").references(() => categories.id, { onDelete: "set null" }),
  /** 親リソース（自己参照） */
  parentId: uuid("parent_id").references(() => resources.id, { onDelete: "cascade" }),
  ...timestamps,
}, (table) => ({
  categoryIdIdx: index("resources_category_id_idx").on(table.categoryId),
  parentIdIdx: index("resources_parent_id_idx").on(table.parentId),
}))
```

---

## onDelete の選び方

| Behavior | 用途 |
|---|---|
| `cascade` | 親消滅で子も消す（タグ・コメント・履歴） |
| `restrict` | 子が存在する間は親消せない（マスター ↔ データ） |
| `set null` | 親消滅で外部キーを null（任意関連、カテゴリ削除等） |
| `no action` | 制約だけ宣言、削除時に処理しない（基本使わない） |

```ts
// 親消滅で子も消す
userId: text("user_id").references(() => users.id, { onDelete: "cascade" }),

// 親を消すと外部キーを null に
categoryId: integer("category_id").references(() => categories.id, { onDelete: "set null" }),

// 関連商品が残ってると消せない
productId: uuid("product_id").references(() => products.id, { onDelete: "restrict" }),
```

---

## relations()

`relations()` で **双方向** に定義（Drizzle の relational query API で必要）:

```ts
import { relations } from "drizzle-orm"

export const resourceRelations = relations(resources, ({ one, many }) => ({
  category: one(categories, { fields: [resources.categoryId], references: [categories.id] }),
  parent: one(resources, { fields: [resources.parentId], references: [resources.id] }),
  tags: many(resourceTags),
  comments: many(comments),
}))

export const categoryRelations = relations(categories, ({ many }) => ({
  resources: many(resources),
}))
```

詳細: `drizzle-style.md`（relational query を使う場合）

---

## Index

```ts
import { index, uniqueIndex } from "drizzle-orm/pg-core"

export const childQuests = pgTable("child_quests", {
  id: uuid("id").primaryKey().default(sql`gen_random_uuid()`),
  childId: uuid("child_id").notNull().references(() => children.id),
  status: childQuestStatus("status").notNull(),
  ...timestamps,
}, (table) => ({
  // 外部キーに index 必須
  childIdIdx: index("child_quests_child_id_idx").on(table.childId),
  // 頻繁にフィルタするカラム
  statusIdx: index("child_quests_status_idx").on(table.status),
  // ユニーク制約
  uniqueChildStatus: uniqueIndex("child_quests_child_status_unique").on(table.childId, table.status),
  // 複合 index（よくある WHERE / ORDER BY 組み合わせ）
  childCreatedAtIdx: index("child_quests_child_created_at_idx").on(table.childId, table.createdAt),
}))
```

---

## Index 設計の原則

- **全外部キーに index 必須**（JOIN 高速化、DELETE 連鎖の高速化）
- 頻繁な **WHERE / ORDER BY 対象** カラムに index
- **複合 index** はクエリパターンに合わせる（カラム順は selectivity 高い順）
- 過剰な index は INSERT/UPDATE を遅くする → 必要なものだけ
- index 名は `{table}_{column}_idx` / `{table}_{cols}_unique`

---

## ルール

- 外部キーは **必ず `references()`** で宣言（手動 JOIN なし）
- **`onDelete` を明示**（デフォルトに任せない）
- 全外部キーに `relations()` を定義
- 全外部キーに `index()` を付ける
- ユニーク制約は `uniqueIndex` で複合キー対応

## 関連 references

- `db-id.md` — 主キー設計
- `drizzle-style.md` — relational query vs SQL Builder
- `db-migration.md` — relation 変更時のマイグレーション

## 禁止

- `references()` なしで外部キーをカラム定義
- `onDelete` を省略（PostgreSQL のデフォルトは `no action` で安全だが意図不明確）
- 外部キーに index なし
- `relations()` を片側だけ定義
