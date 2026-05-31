# Next.js App Router — Test Fixtures (Data Factory)

> **対象**: テストで使うデータ生成を集約して保守性を高める。

---

## 原則

- 1 リソース = 1 fixture ファイル
- Factory 関数で「デフォルト値 + overrides」を返す
- DB シード関数とセットで提供
- 既存 fixtures を参照して関連データを連鎖生成

---

## ファイル構成

```
tests/fixtures/
├── index.ts                  # まとめて export
├── user.ts
├── resource.ts
├── tag.ts
├── category.ts
└── helpers.ts                # nanoid 等の ID 生成
```

---

## 基本 Factory パターン

```ts
// tests/fixtures/resource.ts
import { db } from "@/drizzle/db"
import { resources, type ResourceInsert } from "@/drizzle/schema"
import { nanoid } from "@/tests/fixtures/helpers"

/** デフォルト値 + overrides を持つ Resource を返す（DB には保存しない） */
export const buildResource = (overrides?: Partial<ResourceInsert>): ResourceInsert => ({
  name: `テストリソース_${nanoid(6)}`,
  isPublic: false,
  categoryId: null,
  iconId: 1,
  iconColor: "#3B82F6",
  ...overrides,
})

/** 1 件 INSERT して row を返す */
export const seedResource = async (overrides?: Partial<ResourceInsert>) => {
  const [row] = await db.insert(resources).values(buildResource(overrides)).returning()
  return row
}

/** n 件 INSERT */
export const seedResources = async (count: number, baseOverrides?: Partial<ResourceInsert>) => {
  const records = Array.from({ length: count }).map((_, i) =>
    buildResource({ ...baseOverrides, name: `${baseOverrides?.name ?? "リソース"}_${i + 1}` })
  )
  return await db.insert(resources).values(records).returning()
}

/** 全削除（テスト前のクリーンアップ用） */
export const cleanResources = async () => {
  await db.delete(resources)
}
```

---

## 関連データを連鎖生成

```ts
// tests/fixtures/resource-with-tags.ts
import { seedResource } from "./resource"
import { seedTags } from "./tag"
import { db } from "@/drizzle/db"
import { resourceTags } from "@/drizzle/schema"

export const seedResourceWithTags = async (tagNames: string[], resourceOverrides?: Parameters<typeof seedResource>[0]) => {
  const resource = await seedResource(resourceOverrides)
  const tags = await seedTags(tagNames)
  await db.insert(resourceTags).values(
    tags.map((t) => ({ resourceId: resource.id, tagId: t.id }))
  )
  return { resource, tags }
}
```

---

## User fixture

```ts
// tests/fixtures/user.ts
import { db } from "@/drizzle/db"
import { users, profiles } from "@/drizzle/schema"

export const TEST_USER_ID = "00000000-0000-0000-0000-000000000001"
export const TEST_USER_2_ID = "00000000-0000-0000-0000-000000000002"

export const seedTestUser = async (id = TEST_USER_ID) => {
  const [user] = await db.insert(users).values({
    id,
    email: `${id}@example.com`,
    name: "テストユーザー",
  }).onConflictDoNothing().returning()

  await db.insert(profiles).values({
    userId: id,
    displayName: "テスト",
    userType: "parent",
  }).onConflictDoNothing()

  return user
}
```

---

## Helpers

```ts
// tests/fixtures/helpers.ts
import { customAlphabet } from "nanoid"

const alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
export const nanoid = (n = 6) => customAlphabet(alphabet, n)()

export const isoNow = () => new Date().toISOString()

export const fixedDate = (ms = 0) => new Date(2026, 0, 1, 0, 0, 0, ms).toISOString()
```

---

## まとめて export

```ts
// tests/fixtures/index.ts
export * from "./user"
export * from "./resource"
export * from "./tag"
export * from "./category"
export * from "./resource-with-tags"
export * from "./helpers"
```

```ts
// テスト側
import { seedResource, seedTestUser, cleanResources } from "@/tests/fixtures"
```

---

## DB の cleanup 戦略

| 戦略 | Pros | Cons |
|---|---|---|
| **各 test 前に truncate** | 単純、確実 | やや遅い |
| **transaction で rollback** | 高速、DB 状態に影響なし | Vitest concurrent と相性悪い場合あり |
| **DB を完全 reset（毎回）** | 確実 | 最も遅い |
| **testcontainers で別 DB** | 完全分離 | セットアップが重い |

最も簡単な truncate:

```ts
// tests/helpers/db.ts
import { db } from "@/drizzle/db"
import { resources, tags, profiles } from "@/drizzle/schema"

export const truncateAll = async () => {
  await db.delete(resourceTags)   // 外部キーがあるものから順に
  await db.delete(resources)
  await db.delete(tags)
  await db.delete(profiles)
  // ...
}
```

```ts
beforeEach(async () => {
  await truncateAll()
  await seedTestUser()
})
```

---

## E2E の専用 API

E2E から DB を直接いじるのが難しい場合（別プロセス等）、テスト専用 API ルートを用意:

```ts
// app/api/v1/test/seed/route.ts
import { NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  if (process.env.NODE_ENV !== "test") {
    return new NextResponse("Forbidden", { status: 403 })
  }
  const body = await request.json()
  // body に従って seed
  return NextResponse.json({ ok: true })
}
```

**`NODE_ENV === "test"` 以外は 403** で防御。production にデプロイされても無効。

---

## Test data 命名の慣習

- 一意な名前を作るには suffix に `nanoid(6)` を付ける（並列実行で衝突防止）
- 固定値が必要なら `fixedDate` `TEST_USER_ID` のような const
- enum / boolean の各値を網羅するヘルパー

```ts
export const ALL_RESOURCE_STATUSES = ["draft", "published", "archived"] as const
```

---

## Constraints

- 1 リソース 1 ファイル
- Factory 関数 = `build*`（保存しない）、`seed*` = INSERT して返す
- 関連データの連鎖生成は `seedXxxWithYyy` でセット
- DB cleanup は `beforeEach` で truncate
- テスト専用 API は `NODE_ENV === "test"` で防御
- 一意な名前生成に `nanoid` 等を使う（並列実行に強くする）
- ヘルパー（`isoNow`, `fixedDate`, `TEST_USER_ID`）を共通化
- fixtures を全 test 共通の API（`@/tests/fixtures`）で公開
