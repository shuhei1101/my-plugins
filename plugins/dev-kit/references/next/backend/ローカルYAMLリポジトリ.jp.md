<!-- This file is a Japanese mirror of ローカルYAMLリポジトリ.md. When updating the English original, update this file too. -->
# ローカル開発用 YAML リポジトリパターン

> TypeScript インターフェースでデータアクセス層を抽象化し、
> 本番は Drizzle/Supabase、ローカル開発は YAML ファイルをストアとして差し替える。

---

## コンセプト

```
サービス層 (service.ts)
    ↓ interface (IResourceRepository)
本番: DrizzleResourceRepository  ←→  ローカル: YamlResourceRepository
    ↓                                      ↓
Supabase (Drizzle)                  dev-data/resources.yaml
```

- サービス層はインターフェースにしか依存しない
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
    ├── types.ts                    # インターフェース定義
    ├── index.ts                    # ファクトリ関数
    ├── drizzle/
    │   └── ResourceRepository.ts  # 本番実装（Drizzle）
    └── yaml/
        └── ResourceRepository.ts  # ローカル実装（YAML）
dev-data/
└── resources.yaml                 # ローカル開発データ（gitignore）
```

---

## インターフェース定義

```ts
// lib/repositories/types.ts
export interface IResourceRepository {
  findById(id: string): Promise<Resource | null>
  findAll(params?: { isPublic?: boolean }): Promise<Resource[]>
  insert(record: ResourceInsert): Promise<Resource>
  update(id: string, record: ResourceUpdate): Promise<Resource>
  delete(id: string): Promise<void>
}
```

スキーマ型（`Resource` / `ResourceInsert` / `ResourceUpdate`）は Drizzle schema から import する。
YAML 実装でも同じ型を使うため、型の乖離が起きない。

---

## Drizzle 実装（本番）

```ts
// lib/repositories/drizzle/ResourceRepository.ts
import { eq, and } from "drizzle-orm"
import type { Db } from "@/drizzle/db"
import { resources } from "@/drizzle/schema"
import type { ResourceInsert, ResourceUpdate, Resource } from "@/drizzle/schema"
import { DatabaseError } from "@/app/(shared)/errors/appError"
import type { IResourceRepository } from "../types"

export class DrizzleResourceRepository implements IResourceRepository {
  constructor(private db: Db) {}

  async findById(id: string) {
    const [row] = await this.db.select().from(resources).where(eq(resources.id, id))
    return row ?? null
  }

  async findAll(params?: { isPublic?: boolean }) {
    const conditions = []
    if (params?.isPublic !== undefined) {
      conditions.push(eq(resources.isPublic, params.isPublic))
    }
    return conditions.length
      ? this.db.select().from(resources).where(and(...conditions))
      : this.db.select().from(resources)
  }

  async insert(record: ResourceInsert) {
    try {
      const [row] = await this.db.insert(resources).values(record).returning()
      return row
    } catch {
      throw new DatabaseError("リソースの登録に失敗しました。")
    }
  }

  async update(id: string, record: ResourceUpdate) {
    try {
      const [row] = await this.db
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
  }

  async delete(id: string) {
    try {
      await this.db.delete(resources).where(eq(resources.id, id))
    } catch {
      throw new DatabaseError("リソースの削除に失敗しました。")
    }
  }
}
```

---

## YAML 実装（ローカル開発）

```ts
// lib/repositories/yaml/ResourceRepository.ts
import { parse, stringify } from "yaml"
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs"
import { join } from "path"
import type { ResourceInsert, ResourceUpdate, Resource } from "@/drizzle/schema"
import type { IResourceRepository } from "../types"

export class YamlResourceRepository implements IResourceRepository {
  private readonly filePath = join(process.cwd(), "dev-data", "resources.yaml")

  private load(): Resource[] {
    if (!existsSync(this.filePath)) return []
    return (parse(readFileSync(this.filePath, "utf8")) as Resource[]) ?? []
  }

  private save(records: Resource[]) {
    mkdirSync(join(process.cwd(), "dev-data"), { recursive: true })
    writeFileSync(this.filePath, stringify(records))
  }

  async findById(id: string) {
    return this.load().find((r) => r.id === id) ?? null
  }

  async findAll(params?: { isPublic?: boolean }) {
    const records = this.load()
    if (params?.isPublic !== undefined) {
      return records.filter((r) => r.isPublic === params.isPublic)
    }
    return records
  }

  async insert(record: ResourceInsert) {
    const records = this.load()
    const now = new Date().toISOString()
    const newRecord: Resource = {
      ...record,
      id: crypto.randomUUID(),
      createdAt: now,
      updatedAt: now,
    }
    records.push(newRecord)
    this.save(records)
    return newRecord
  }

  async update(id: string, record: ResourceUpdate) {
    const records = this.load()
    const index = records.findIndex((r) => r.id === id)
    if (index === -1) throw new Error(`Resource not found: ${id}`)
    records[index] = { ...records[index], ...record, updatedAt: new Date().toISOString() }
    this.save(records)
    return records[index]
  }

  async delete(id: string) {
    this.save(this.load().filter((r) => r.id !== id))
  }
}
```

---

## ファクトリ関数

```ts
// lib/repositories/index.ts
import { db } from "@/drizzle/db"
import { DrizzleResourceRepository } from "./drizzle/ResourceRepository"
import { YamlResourceRepository } from "./yaml/ResourceRepository"
import type { IResourceRepository } from "./types"

export const getResourceRepository = (): IResourceRepository => {
  if (process.env.USE_YAML_DB === "true") {
    return new YamlResourceRepository()
  }
  return new DrizzleResourceRepository(db)
}
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
| `db.ts` | INSERT / UPDATE / DELETE | `YamlResourceRepository` に統合 |
| `query.ts` | SELECT / JOIN | 〃 |
| `service.ts` | ビジネスロジック | **変更なし**（インターフェース経由） |

既存の `db.ts` / `query.ts` パターンを維持しつつ、
リポジトリパターンに段階移行することもできる（`service.ts` → repo → `db.ts` の呼び出しをまとめる）。

---

## Constraints

- `IResourceRepository` インターフェースはスキーマ型（Drizzle の `$inferSelect`）に依存してよい
- `YamlResourceRepository` は `process.env.USE_YAML_DB === "true"` のときのみ使用
- `dev-data/` は必ず `.gitignore` に追加する（機密データ流出防止）
- ファクトリ関数（`getResourceRepository`）は Server Component / Route Handler からのみ呼ぶ
- YAML ファイルへのアクセスは同期 I/O（`readFileSync` / `writeFileSync`）で可。並列リクエストが少ないローカル開発専用のため
- 本番コードに `YamlResourceRepository` の依存を混入させない（`USE_YAML_DB` のガードを守る）
