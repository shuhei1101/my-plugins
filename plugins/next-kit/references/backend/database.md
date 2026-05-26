# Next.js App Router — Database Design (Drizzle ORM)

## Overview

Use Drizzle ORM for all database access. All schema definitions live in a single file.

```
drizzle/
├── schema.ts       # All table definitions, Enum types, and relations
├── db.ts           # DB client instance
└── migrations/     # Migration files (managed by drizzle-kit)
```

---

## Schema definition pattern

```ts
// drizzle/schema.ts
import { pgTable, pgEnum, text, uuid, timestamp } from "drizzle-orm/pg-core"
import { relations } from "drizzle-orm"

// Enum types
export const userTypeEnum = pgEnum("user_type", ["parent", "child"])

// Table definition
export const profiles = pgTable("profiles", {
  id: uuid("id").primaryKey().defaultRandom(),
  userId: uuid("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  name: text("name").notNull(),
  userType: userTypeEnum("user_type").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
})

// Relations
export const profileRelations = relations(profiles, ({ one }) => ({
  user: one(users, { fields: [profiles.userId], references: [users.id] }),
}))
```

---

## Relation design principles

| Delete behavior | Use when |
|---|---|
| `onDelete: "cascade"` | Child records should be deleted with the parent |
| `onDelete: "restrict"` | Parent cannot be deleted while child records exist |
| `onDelete: "set null"` | Foreign key becomes NULL when parent is deleted |

Always add an index on foreign key columns and frequently filtered columns:

```ts
import { index } from "drizzle-orm/pg-core"

export const childQuests = pgTable("child_quests", {
  id: uuid("id").primaryKey().defaultRandom(),
  childId: uuid("child_id").notNull().references(() => children.id),
  status: childQuestStatusEnum("status").notNull(),
}, (table) => ({
  childIdIdx: index("child_quests_child_id_idx").on(table.childId),
  statusIdx: index("child_quests_status_idx").on(table.status),
}))
```

---

## DB query patterns in db.ts

```ts
import { eq, and, desc, count } from "drizzle-orm"
import { families } from "@/drizzle/schema"

// Select one
export const selectFamilyById = async ({ db, id }) => {
  return db.select().from(families).where(eq(families.id, id)).then(r => r[0] ?? null)
}

// Select many with filter
export const selectFamilies = async ({ db, userId }) => {
  return db.select().from(families).where(eq(families.ownerId, userId)).orderBy(desc(families.createdAt))
}

// Insert
export const insertFamily = async ({ db, data }) => {
  const [row] = await db.insert(families).values(data).returning()
  return row
}

// Update
export const updateFamily = async ({ db, id, data }) => {
  await db.update(families).set(data).where(eq(families.id, id))
}

// Delete
export const deleteFamily = async ({ db, id }) => {
  await db.delete(families).where(eq(families.id, id))
}
```

---

## Migration workflow

```bash
# Generate migration after schema changes
npx drizzle-kit generate

# Apply migrations
npx drizzle-kit migrate
```

---

## Constraints

- All schema definitions go in `drizzle/schema.ts` — never define inline table schemas elsewhere
- Always use `drizzle-kit` for migrations — never write raw SQL migration files manually
- Always define `relations()` for every foreign key — required for Drizzle's relational query API
- Use Enum types (`pgEnum`) for columns with a fixed set of values
- Never use `db.execute(sql\`...\`)` for regular queries — use the Drizzle query builder
