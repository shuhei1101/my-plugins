# ローカル開発用 YAML データストア

> 関数ごとに `type` で型を定義し、`query.ts` / `db.ts` の実装を本番（Drizzle）と
> ローカル（YAML ファイル）で差し替える。クラス・`interface`・Repository は使わない。
> データアクセスは `fetch{Feature}` / `insert{Feature}` などの素の関数。

---

## コンセプト

```
service.ts
   ↓ import { fetchResource } from "./query"
   ↓ import { insertResource } from "./db"
query.ts / db.ts  ← env で実装を切り替え
   ├─ *.drizzle.ts  → 本番（Supabase / Drizzle）
   └─ *.yaml.ts     → ローカル（data/dev/*.yaml）
```

- 関数の型（`FetchResource` 等）を 1 か所（`types.ts`）に定義し、両実装が同じ型を満たす
- `USE_YAML_DB=true` を `.env.local` に設定するだけで切り替わる
- YAML ファイルはスキーマと同じフィールドを持つ → 移行コストなし

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
data/dev/
```

---

## フォルダ構成

```
app/api/v1/resources/
├── types.ts          # 関数ごとの型定義
├── query.ts          # 読み取りの切り替え（re-export）
├── query.drizzle.ts  # 本番（Drizzle）
├── query.yaml.ts     # ローカル（YAML）
├── db.ts             # 書き込みの切り替え（re-export）
├── db.drizzle.ts     # 本番（Drizzle）
└── db.yaml.ts        # ローカル（YAML）
app/(shared)/lib/yamlStore.ts   # 汎用 YAML 読み書きヘルパー
data/dev/resources.yaml         # ローカル開発データ（gitignore）
```

---

## 関数ごとの型定義

関数 1 つにつき型を 1 つ定義する。型名と関数名を対応させる（`FetchResource` ↔ `fetchResource`）。

```ts
// app/api/v1/resources/types.ts
import type { Resource, ResourceInsert, ResourceUpdate } from "@/drizzle/schema"

// ----- 読み取り（query.ts） -----
export type FetchResource = (args: { id: string }) => Promise<Resource | null>
export type FetchResources = (args?: { isPublic?: boolean }) => Promise<Resource[]>

// ----- 書き込み（db.ts） -----
export type InsertResource = (args: { record: ResourceInsert }) => Promise<{ id: string }>
export type UpdateResource = (args: { id: string; updatedAt: string; record: ResourceUpdate }) => Promise<void>
export type DeleteResource = (args: { id: string }) => Promise<void>
```

スキーマ型（`Resource` / `ResourceInsert` / `ResourceUpdate`）は Drizzle schema から import する。
両実装が同じ型を import するため、シグネチャの乖離が起きない。

---

## 本番実装（Drizzle）

```ts
// app/api/v1/resources/query.drizzle.ts
import { eq } from "drizzle-orm"
import { db } from "@/drizzle/db"
import { resources } from "@/drizzle/schema"
import { QueryError } from "@/app/(shared)/errors/appError"
import type { FetchResource, FetchResources } from "./types"

export const fetchResource: FetchResource = async ({ id }) => {
  try {
    const [row] = await db.select().from(resources).where(eq(resources.id, id))
    return row ?? null
  } catch {
    throw new QueryError("リソースの取得に失敗しました。")
  }
}

export const fetchResources: FetchResources = async (args) => {
  try {
    return args?.isPublic !== undefined
      ? db.select().from(resources).where(eq(resources.isPublic, args.isPublic))
      : db.select().from(resources)
  } catch {
    throw new QueryError("リソース一覧の取得に失敗しました。")
  }
}
```

```ts
// app/api/v1/resources/db.drizzle.ts
import { and, eq } from "drizzle-orm"
import { db } from "@/drizzle/db"
import { resources } from "@/drizzle/schema"
import { DatabaseError, VersionConflictError } from "@/app/(shared)/errors/appError"
import type { InsertResource, UpdateResource, DeleteResource } from "./types"

export const insertResource: InsertResource = async ({ record }) => {
  try {
    const [row] = await db.insert(resources).values(record).returning({ id: resources.id })
    return { id: row.id }
  } catch {
    throw new DatabaseError("リソースの登録に失敗しました。")
  }
}

export const updateResource: UpdateResource = async ({ id, updatedAt, record }) => {
  try {
    const [row] = await db.update(resources)
      .set({ ...record, updatedAt: new Date().toISOString() })
      .where(and(eq(resources.id, id), eq(resources.updatedAt, updatedAt)))
      .returning({ id: resources.id })
    if (!row) throw new VersionConflictError("他のユーザーによって更新されています。")
  } catch (e) {
    if (e instanceof VersionConflictError) throw e
    throw new DatabaseError("リソースの更新に失敗しました。")
  }
}

export const deleteResource: DeleteResource = async ({ id }) => {
  try {
    await db.delete(resources).where(eq(resources.id, id))
  } catch {
    throw new DatabaseError("リソースの削除に失敗しました。")
  }
}
```

---

## ローカル実装（YAML）

汎用の読み書きヘルパーを 1 つ用意し、各関数はそれを使う。

```ts
// app/(shared)/lib/yamlStore.ts
import { parse, stringify } from "yaml"
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs"
import { join, dirname } from "path"

const tablePath = (table: string) => join(process.cwd(), "data", "dev", `${table}.yaml`)

export const readTable = <T>(table: string): T[] => {
  const path = tablePath(table)
  if (!existsSync(path)) return []
  return (parse(readFileSync(path, "utf8")) as T[]) ?? []
}

export const writeTable = <T>(table: string, rows: T[]) => {
  const path = tablePath(table)
  mkdirSync(dirname(path), { recursive: true })
  writeFileSync(path, stringify(rows))
}
```

```ts
// app/api/v1/resources/query.yaml.ts
import { readTable } from "@/app/(shared)/lib/yamlStore"
import type { Resource } from "@/drizzle/schema"
import type { FetchResource, FetchResources } from "./types"

const TABLE = "resources"

export const fetchResource: FetchResource = async ({ id }) =>
  readTable<Resource>(TABLE).find((r) => r.id === id) ?? null

export const fetchResources: FetchResources = async (args) => {
  const rows = readTable<Resource>(TABLE)
  return args?.isPublic !== undefined ? rows.filter((r) => r.isPublic === args.isPublic) : rows
}
```

```ts
// app/api/v1/resources/db.yaml.ts
import { readTable, writeTable } from "@/app/(shared)/lib/yamlStore"
import type { Resource } from "@/drizzle/schema"
import type { InsertResource, UpdateResource, DeleteResource } from "./types"

const TABLE = "resources"

export const insertResource: InsertResource = async ({ record }) => {
  const rows = readTable<Resource>(TABLE)
  const now = new Date().toISOString()
  const row: Resource = { ...record, id: crypto.randomUUID(), createdAt: now, updatedAt: now }
  writeTable(TABLE, [...rows, row])
  return { id: row.id }
}

export const updateResource: UpdateResource = async ({ id, record }) => {
  const rows = readTable<Resource>(TABLE)
  writeTable(TABLE, rows.map((r) => (r.id === id ? { ...r, ...record, updatedAt: new Date().toISOString() } : r)))
}

export const deleteResource: DeleteResource = async ({ id }) => {
  writeTable(TABLE, readTable<Resource>(TABLE).filter((r) => r.id !== id))
}
```

`types.ts` の型を付けているため、YAML 実装が Drizzle 実装とシグネチャ不一致なら型エラーになる。

---

## 切り替え（re-export）

```ts
// app/api/v1/resources/query.ts
import * as drizzle from "./query.drizzle"
import * as yaml from "./query.yaml"

const impl = process.env.USE_YAML_DB === "true" ? yaml : drizzle

export const fetchResource = impl.fetchResource
export const fetchResources = impl.fetchResources
```

```ts
// app/api/v1/resources/db.ts
import * as drizzle from "./db.drizzle"
import * as yaml from "./db.yaml"

const impl = process.env.USE_YAML_DB === "true" ? yaml : drizzle

export const insertResource = impl.insertResource
export const updateResource = impl.updateResource
export const deleteResource = impl.deleteResource
```

---

## service.ts での使い方

`service.ts` は `./query` / `./db` から import するだけ。実装の差し替えを意識しない。

```ts
// app/api/v1/resources/service.ts
import { fetchResource } from "./query"
import { insertResource } from "./db"
import { NotFoundError } from "@/app/(shared)/errors/appError"

export const getResource = async ({ id }: { id: string }) => {
  const resource = await fetchResource({ id })
  if (!resource) throw new NotFoundError("リソースが見つかりません。")
  return resource
}

export const registerResource = async ({ record }: { record: ResourceInsert }) =>
  insertResource({ record })
```

---

## YAML データファイルの例

```yaml
# data/dev/resources.yaml
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

## Constraints

- 関数 1 つにつき `type` を 1 つ定義する（`FetchResource` ↔ `fetchResource`）。`interface`・クラスは使わない
- データアクセスは素の関数。命名は `fetch{Feature}`（読み取り）/ `insert`・`update`・`delete{Feature}`（書き込み）
- 引数はオブジェクトで受ける（`{ id }` / `{ record }`）
- 読み取りは `query.ts`、書き込みは `db.ts` に分離（既存の `クエリ-ts.md` / `DB-ts.md` 準拠）
- 切り替えは `query.ts` / `db.ts` の re-export 層のみ。実装ファイル（`*.drizzle.ts` / `*.yaml.ts`）は env を見ない
- `data/dev/` は必ず `.gitignore` に追加する（機密データ流出防止）
- YAML の I/O は同期（`readFileSync` / `writeFileSync`）で可。ローカル開発専用のため
- YAML モードはトランザクション非対応（各書き込みが即時永続）。複数テーブルにまたがる整合性が要る処理は本番 Drizzle 側で `service.ts` のトランザクションに閉じる
- 本番ビルドに YAML 実装を混入させない（`USE_YAML_DB` のガードを守る）
