# drizzle/schema.ts — 認証関連テーブル

Better Auth が要求する 4 テーブル（user / session / account / verification）+ アプリ固有の profile。

---

## 必須テンプレ

```ts
// drizzle/schema.ts
import { pgTable, text, timestamp, boolean, uuid, integer } from "drizzle-orm/pg-core"
import { relations, sql } from "drizzle-orm"
import { timestamps } from "./_helpers"

// ----- Better Auth required tables -----

/** ユーザー */
export const users = pgTable("user", {
  id: text("id").primaryKey(),
  name: text("name"),
  email: text("email").notNull().unique(),
  emailVerified: boolean("email_verified").notNull().default(false),
  image: text("image"),
  ...timestamps,
})
export type UserSelect = typeof users.$inferSelect

/** セッション */
export const sessions = pgTable("session", {
  id: text("id").primaryKey(),
  userId: text("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  token: text("token").notNull().unique(),
  expiresAt: timestamp("expires_at", { withTimezone: true }).notNull(),
  ipAddress: text("ip_address"),
  userAgent: text("user_agent"),
  ...timestamps,
})

/** OAuth アカウント */
export const accounts = pgTable("account", {
  id: text("id").primaryKey(),
  userId: text("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  accountId: text("account_id").notNull(),
  providerId: text("provider_id").notNull(),
  accessToken: text("access_token"),
  refreshToken: text("refresh_token"),
  idToken: text("id_token"),
  accessTokenExpiresAt: timestamp("access_token_expires_at", { withTimezone: true }),
  refreshTokenExpiresAt: timestamp("refresh_token_expires_at", { withTimezone: true }),
  scope: text("scope"),
  password: text("password"),
  ...timestamps,
})

/** メール確認・パスワードリセット用トークン */
export const verifications = pgTable("verification", {
  id: text("id").primaryKey(),
  identifier: text("identifier").notNull(),
  value: text("value").notNull(),
  expiresAt: timestamp("expires_at", { withTimezone: true }).notNull(),
  ...timestamps,
})

// ----- App-specific profile -----

/** ユーザープロフィール */
export const profiles = pgTable("profiles", {
  userId: text("user_id")
    .primaryKey()
    .references(() => users.id, { onDelete: "cascade" }),
  /** 表示名 */
  displayName: text("display_name").notNull(),
  /** 家族 ID（ない場合は null） */
  familyId: uuid("family_id").references(() => families.id, { onDelete: "set null" }),
  /** ユーザータイプ */
  userType: userType("user_type").notNull(),
  ...timestamps,
})
export type ProfileSelect = typeof profiles.$inferSelect

// ----- Relations -----

export const usersRelations = relations(users, ({ one, many }) => ({
  profile: one(profiles, { fields: [users.id], references: [profiles.userId] }),
  sessions: many(sessions),
  accounts: many(accounts),
}))

export const profilesRelations = relations(profiles, ({ one }) => ({
  user: one(users, { fields: [profiles.userId], references: [users.id] }),
  family: one(families, { fields: [profiles.familyId], references: [families.id] }),
}))
```

---

## ルール

- **Better Auth 公式 schema 名を厳守**（`user`, `session`, `account`, `verification`）
- **`onDelete: "cascade"`**: user 削除で session / account も削除
- アプリ固有データは **`profiles`** テーブルに分離（user テーブルを汚さない）
- `relations()` で双方向リレーション定義
- ID は `text` 型（Better Auth デフォルト、変更しない）
- timestamps は共通ヘルパー（`db-timestamps.md`）

## マイグレーション

スキーマ変更後:

```bash
pnpm drizzle-kit generate
pnpm drizzle-kit migrate
```

詳細: `db-migration.md`

## 関連 references

- `auth-context.md` — getAuthContext 実装
- `auth-setup.md` — Better Auth 設定
- `db-id.md` — ID 設計
- `db-timestamps.md` — timestamps ヘルパー
- `db-relations.md` — relations 設計
- `db-migration.md` — マイグレーション運用

## 禁止

- Better Auth のテーブル名・カラム名を変更
- profile を user テーブルに統合
- session / account の onDelete を変更（cascade 必須）
