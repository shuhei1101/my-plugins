<!-- This file is a Japanese mirror of ローカルYAMLリポジトリ.md. When updating the English original, update this file too. -->
# ローカル開発用 YAML リポジトリパターン

> TypeScript の `type` でデータアクセス層を抽象化し、
> 本番は Drizzle/Supabase、ローカル開発は YAML ファイルをストアとして差し替える。
> クラスは使わず、ファクトリ関数が型を満たすオブジェクトを返す関数型スタイル。

---

## コンセプト

```
サービス層 (service.ts)
    ↓ type (ResourceRepository)
本番: createDrizzleResourceRepository  ←→  ローカル: createYamlResourceRepository
    ↓                                              ↓
Supabase (Drizzle)                          dev-data/resources.yaml
```

- サービス層は `ResourceRepository` 型にしか依存しない
- `USE_YAML_DB=true` を `.env.local` に設定するだけで切り替わる
- YAML ファイルはスキーマと同じ構造を持つ → 移行コストなし

---

## セットアップ

```bash
pnpm add yaml
```

```
# .env.local（ローカル開発用）
USE_YAML_DB=true
```

```
# .gitignore に追加
dev-data/
```

---

## フォルダ構成

```
lib/
└── repositories/
    ├── types.ts     # ResourceRepository 型定義
    ├── index.ts     # getResourceRepository（ファクトリ）
    ├── drizzle.ts   # createDrizzleResourceRepository
    └── yaml.ts      # createYamlResourceRepository
dev-data/
└── resources.yaml   # ローカル開発データ（gitignore）
```

---

## 型定義

```ts
// lib/repositories/types.ts
import type { Resource, ResourceInsert, ResourceUpdate } from "@/drizzle/schema"

export type ResourceRepository = {
  findById: (id: string) => Promise<Resource | null>
  findAll: (params?: { isPublic?: boolean }) => Promise<Resource[]>
  insert: (record: ResourceInsert) => Promise<Resource>
  update: (id: string, record: ResourceUpdate) => Promise<Resource>
  delete: (id: string) => Promise<void>
}
```

スキーマ型は Drizzle schema から import する。YAML 実装でも同じ型を使うため型の乖離が起きない。

---

## Drizzle 実装（本番）

```ts
// lib/repositories/drizzle.ts
import { eq, and } from "drizzle-orm"
import type { Db } from "@/drizzle/db"
import { resources } from "@/drizzle/schema"
import type { ResourceInsert, ResourceUpdate } from "@/drizzle/schema"
import { DatabaseError } from "@/app/(shared)/errors/appError"
import type { ResourceRepository } from "./types"

export const createDrizzleResourceRepository = (db: Db): ResourceRepository => ({
  findById: async (id) => {
    const [row] = await db.select().from(resources).where(eq(resources.id, id))
    return row ?? null
  },

  findAll: async (params) => {
    const conditions = []
    if (params?.isPublic !== undefined) {
      conditions.push(eq(resources.isPublic, params.isPublic))
    }
    return conditions.length
      ? db.select().from(resources).where(and(...conditions))
      : db.select().from(resources)
  },

  insert: async (record: ResourceInsert) => {
    try {
      const [row] = await db.insert(resources).values(record).returning()
      return row
    } catch {
      throw new DatabaseError("リソースの登録に失敗しました。")
    }
  },

  update: async (id, record: ResourceUpdate) => {
    try {
      const [row] = await db
        .update(resources)
        .set({ ...record, updatedAt: new Date().toISOString() })
        .where(eq(resources.id, id))
        .returning()
      if (!row) throw new DatabaseError("リソースが見つかりませんでした。")
      return row
    } catch (e) {
      if (e instanceof DatabaseError) throw e
      throw new DatabaseError("リソースの更新に失敗しました。")
    }
  },

  delete: async (id) => {
    try {
      await db.delete(resources).where(eq(resources.id, id))
    } catch {
      throw new DatabaseError("リソースの削除に失敗しました。")
    }
  },
})
```

---

## YAML 実装（ローカル開発）

```ts
// lib/repositories/yaml.ts
import { parse, stringify } from "yaml"
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs"
import { join } from "path"
import type { Resource, ResourceInsert, ResourceUpdate } from "@/drizzle/schema"
import type { ResourceRepository } from "./types"

export const createYamlResourceRepository = (): ResourceRepository => {
  const filePath = join(process.cwd(), "dev-data", "resources.yaml")

  const load = (): Resource[] => {
    if (!existsSync(filePath)) return []
    return (parse(readFileSync(filePath, "utf8")) as Resource[]) ?? []
  }

  const save = (records: Resource[]) => {
    mkdirSync(join(process.cwd(), "dev-data"), { recursive: true })
    writeFileSync(filePath, stringify(records))
  }

  return {
    findById: async (id) => load().find((r) => r.id === id) ?? null,

    findAll: async (params) => {
      const records = load()
      return params?.isPublic !== undefined
        ? records.filter((r) => r.isPublic === params.isPublic)
        : records
    },

    insert: async (record: ResourceInsert) => {
      const records = load()
      const now = new Date().toISOString()
      const newRecord: Resource = { ...record, id: crypto.randomUUID(), createdAt: now, updatedAt: now }
      records.push(newRecord)
      save(records)
      return newRecord
    },

    update: async (id, record: ResourceUpdate) => {
      const records = load()
      const index = records.findIndex((r) => r.id === id)
      if (index === -1) throw new Error(`Resource not found: ${id}`)
      records[index] = { ...records[index], ...record, updatedAt: new Date().toISOString() }
      save(records)
      return records[index]
    },

    delete: async (id) => save(load().filter((r) => r.id !== id)),
  }
}
```

---

## ファクトリ（切り替えポイント）

```ts
// lib/repositories/index.ts
import { db } from "@/drizzle/db"
import { createDrizzleResourceRepository } from "./drizzle"
import { createYamlResourceRepository } from "./yaml"
import type { ResourceRepository } from "./types"

export const getResourceRepository = (): ResourceRepository =>
  process.env.USE_YAML_DB === "true"
    ? createYamlResourceRepository()
    : createDrizzleResourceRepository(db)
```

---

## service.ts での使い方

```ts
// app/api/v1/resources/service.ts
import { getResourceRepository } from "@/lib/repositories"

export const getResource = async (id: string) => {
  const repo = getResourceRepository()
  const resource = await repo.findById(id)
  if (!resource) throw new NotFoundError("リソースが見つかりません。")
  return resource
}

export const createResource = async (record: ResourceInsert) => {
  const repo = getResourceRepository()
  return repo.insert(record)
}
```

`db` を直接 import しない → YAML 実装と Drizzle 実装を透過的に切り替え可能。

---

## YAML データファイルの例

```yaml
# dev-data/resources.yaml
- id: "01935abc-1234-7000-a000-000000000001"
  name: テストリソース A
  isPublic: false
  createdAt: "2026-06-01T00:00:00.000Z"
  updatedAt: "2026-06-01T00:00:00.000Z"
- id: "01935abc-1234-7000-a000-000000000002"
  name: テストリソース B
  isPublic: true
  createdAt: "2026-06-01T01:00:00.000Z"
  updatedAt: "2026-06-01T01:00:00.000Z"
```

スキーマと同じフィールドを持つ → 本番 DB へのデータ移行もそのまま使える。

---

## 既存の `db.ts` / `query.ts` との関係

| ファイル | 役割 | YAML 実装での対応 |
|---|---|---|
| `db.ts` | INSERT / UPDATE / DELETE | `createYamlResourceRepository` に統合 |
| `query.ts` | SELECT / JOIN | 〃 |
| `service.ts` | ビジネスロジック | **変更なし**（`ResourceRepository` 型経由） |

既存の `db.ts` / `query.ts` パターンを維持しつつ段階移行することもできる。

---

## Constraints

- `ResourceRepository` は `type` で定義する（`interface` / クラスは使わない）
- ファクトリ関数名は `create{Store}{Resource}Repository` 形式
- `createYamlResourceRepository` は `USE_YAML_DB === "true"` のときのみ呼ばれる
- `dev-data/` は必ず `.gitignore` に追加する（機密データ流出防止）
- `getResourceRepository` は Server Component / Route Handler からのみ呼ぶ
- YAML の I/O は同期（`readFileSync` / `writeFileSync`）で可。ローカル開発専用のため
- 本番ビルドに YAML 依存を混入させない（`USE_YAML_DB` のガードを守る）
