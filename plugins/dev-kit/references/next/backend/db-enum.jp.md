<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# drizzle/schema.ts — Enum

固定セットの値を取るカラムは `pgEnum` で型安全に定義。

---

## 必須テンプレ

```ts
import { pgEnum, pgTable, uuid, text } from "drizzle-orm/pg-core"

/** リソースステータス */
export const resourceStatus = pgEnum("resource_status", [
  "draft",       // 下書き
  "published",   // 公開中
  "archived",    // アーカイブ
])
export type ResourceStatus = (typeof resourceStatus.enumValues)[number]

/** ユーザータイプ */
export const userType = pgEnum("user_type", [
  "parent",
  "child",
])
export type UserType = (typeof userType.enumValues)[number]
```

---

## カラム定義での利用

```ts
export const resources = pgTable("resources", {
  id: uuid("id").primaryKey().default(sql`gen_random_uuid()`),
  name: text("name").notNull(),
  /** ステータス */
  status: resourceStatus("status").notNull().default("draft"),
  ...timestamps,
})
```

---

## Zod スキーマと併用

```ts
import { z } from "zod"

export const ResourceFormSchema = z.object({
  status: z.enum(resourceStatus.enumValues),
})
```

`z.enum` の引数に `enumValues` を渡すと、enum 定義の変更が自動的に反映される。

---

## 命名

| 対象 | 命名 |
|---|---|
| Enum 定義（camelCase 単数） | `resourceStatus`, `userType`, `notificationType` |
| Postgres での名前（snake_case 単数） | `resource_status`, `user_type` |
| TypeScript の型（PascalCase 単数） | `ResourceStatus`, `UserType` |

`*Enum` 接尾辞は **付けない**（quest-pay 流儀に合わせる）。

---

## Enum 値追加

```bash
# 値を配列に追加 → マイグレーション生成
pnpm drizzle-kit generate
pnpm drizzle-kit migrate
```

Postgres 側で `ALTER TYPE ... ADD VALUE` が走る。値の **削除・並び替えは難しい**（既存データへの影響大）ので慎重に。

詳細: `db-migration.md`

---

## ルール

- 固定セットの値は **`pgEnum`** を必ず使う（`text` で持つと型安全性なし）
- 値が動的に変わる（ユーザー追加可能等）なら別テーブルで管理
- 命名は camelCase 単数（`*Enum` 接尾辞なし）
- カラム JSDoc に値の説明を付ける（`comments.md` の重要カラム規約）

```ts
/** リソースステータス — draft=下書き / published=公開 / archived=非表示 */
status: resourceStatus("status").notNull().default("draft"),
```

## 関連 references

- `db-migration.md` — Enum 値追加時のマイグレーション
- `conventions/comments.md` — カラム JSDoc

## 禁止

- `text` 型で enum 的なものを持つ（型安全性なし）
- Enum 値の途中削除（マイグレーションで事故る）
- `*Enum` 接尾辞（命名統一違反）
