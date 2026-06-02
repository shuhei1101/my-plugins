<!-- This file is a Japanese mirror of ローカルYAML開発DB.md. When updating the English original, update this file too. -->
# ローカル開発用 YAML データストア

> 関数ごとに `type` で型を定義し、`query.ts` / `db.ts` の実装を本番（Drizzle）と
> ローカル（YAML ファイル）で差し替える。クラス・`interface`・Repository は使わない。
> データアクセスは `fetch{Feature}` / `insert{Feature}` などの素の関数で、`db` を引数で受け渡す（quest-pay 準拠）。
> トランザクション境界は `service.ts` が持つ。

---

## コンセプト

```
service.ts（transaction() でトランザクション境界）
   ↓ fetchResource({ db, id }) / insertResource({ db, record })
query.ts / db.ts  ← env で実装を切り替え
   ├─ *.drizzle.ts  → 本番（Supabase / Drizzle）。渡された db(tx) を使う
   └─ *.yaml.ts     → ローカル（data/dev/*.yaml）。db は無視
```

- 関数の型（`FetchResource` 等）を `types.ts` に定義し、両実装が同じ型を満たす
- `USE_YAML_DB=true` を `.env.local` に設定するだけで切り替わる
- **トランザクション維持**：本番は Drizzle の `db.transaction`、ローカルは YAML スナップショット/ロールバック + ロック
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
├── query.drizzle.ts  / query.yaml.ts
├── db.ts             # 書き込みの切り替え（re-export）
├── db.drizzle.ts     / db.yaml.ts
└── service.ts        # トランザクション境界
app/(shared)/lib/
├── yamlStore.ts      # readTable / writeTable / runYamlTransaction（ロック+ロールバック）
└── transaction.ts    # transaction() / baseDb の env 切り替え
data/dev/resources.yaml   # ローカル開発データ（gitignore）
```

---

## 関数ごとの型定義

関数 1 つにつき型を 1 つ定義する。型名と関数名を対応させる（`FetchResource` ↔ `fetchResource`）。
quest-pay 同様に `db` を引数に含める。

```ts
// app/api/v1/resources/types.ts
import type { Db } from "@/drizzle/db"
import type { Resource, ResourceInsert, ResourceUpdate } from "@/drizzle/schema"

// ----- 読み取り（query.ts） -----
export type FetchResource = (args: { db: Db; id: string }) => Promise<Resource | null>
export type FetchResources = (args: { db: Db; isPublic?: boolean }) => Promise<Resource[]>

// ----- 書き込み（db.ts） -----
export type InsertResource = (args: { db: Db; record: ResourceInsert }) => Promise<{ id: string }>
export type UpdateResource = (args: { db: Db; id: string; updatedAt: string; record: ResourceUpdate }) => Promise<void>
export type DeleteResource = (args: { db: Db; id: string }) => Promise<void>
```

`db` は本番では Drizzle のトランザクションハンドル（`tx`）。YAML 実装は `db` を使わない（ロールバックは
`runYamlTransaction` が担う）が、型を合わせるためシグネチャには含める。

---

## 本番実装（Drizzle）

渡された `db`（= `service.ts` の `transaction` が渡す `tx`）を使う。

```ts
// app/api/v1/resources/query.drizzle.ts
import { eq } from "drizzle-orm"
import { resources } from "@/drizzle/schema"
import { QueryError } from "@/app/(shared)/errors/appError"
import type { FetchResource, FetchResources } from "./types"

export const fetchResource: FetchResource = async ({ db, id }) => {
  try {
    const [row] = await db.select().from(resources).where(eq(resources.id, id))
    return row ?? null
  } catch {
    throw new QueryError("リソースの取得に失敗しました。")
  }
}

export const fetchResources: FetchResources = async ({ db, isPublic }) => {
  try {
    return isPublic !== undefined
      ? db.select().from(resources).where(eq(resources.isPublic, isPublic))
      : db.select().from(resources)
  } catch {
    throw new QueryError("リソース一覧の取得に失敗しました。")
  }
}
```

```ts
// app/api/v1/resources/db.drizzle.ts
import { and, eq } from "drizzle-orm"
import { resources } from "@/drizzle/schema"
import { DatabaseError, VersionConflictError } from "@/app/(shared)/errors/appError"
import type { InsertResource, UpdateResource, DeleteResource } from "./types"

export const insertResource: InsertResource = async ({ db, record }) => {
  try {
    const [row] = await db.insert(resources).values(record).returning({ id: resources.id })
    return { id: row.id }
  } catch {
    throw new DatabaseError("リソースの登録に失敗しました。")
  }
}

export const updateResource: UpdateResource = async ({ db, id, updatedAt, record }) => {
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

export const deleteResource: DeleteResource = async ({ db, id }) => {
  try {
    await db.delete(resources).where(eq(resources.id, id))
  } catch {
    throw new DatabaseError("リソースの削除に失敗しました。")
  }
}
```

---

## ローカル実装（YAML）

`yamlStore.ts` が読み書きとトランザクション（ロック + スナップショット/ロールバック）を提供する。

```ts
// app/(shared)/lib/yamlStore.ts
import { parse, stringify } from "yaml"
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, rmSync } from "fs"
import { join } from "path"

const DIR = join(process.cwd(), "data", "dev")
const tablePath = (table: string) => join(DIR, `${table}.yaml`)

export const readTable = <T>(table: string): T[] => {
  const path = tablePath(table)
  if (!existsSync(path)) return []
  return (parse(readFileSync(path, "utf8")) as T[]) ?? []
}

export const writeTable = <T>(table: string, rows: T[]) => {
  mkdirSync(DIR, { recursive: true })
  writeFileSync(tablePath(table), stringify(rows))
}

// ----- 簡易トランザクション（ロック + スナップショット/ロールバック） -----

let lock: Promise<unknown> = Promise.resolve()   // in-process ロック（同時に 1 件だけ実行）

const snapshot = (): Record<string, string> => {
  if (!existsSync(DIR)) return {}
  return Object.fromEntries(readdirSync(DIR).map((f) => [f, readFileSync(join(DIR, f), "utf8")]))
}

const restore = (snap: Record<string, string>) => {
  mkdirSync(DIR, { recursive: true })
  for (const f of readdirSync(DIR)) if (!(f in snap)) rmSync(join(DIR, f))   // 新規作成分を削除
  for (const [f, body] of Object.entries(snap)) writeFileSync(join(DIR, f), body)   // 中身を巻き戻す
}

export const runYamlTransaction = async <T>(fn: () => Promise<T>): Promise<T> => {
  const run = async () => {
    const snap = snapshot()
    try {
      return await fn()
    } catch (e) {
      restore(snap)   // どこかで失敗したら全テーブルを巻き戻す
      throw e
    }
  }
  const result = lock.then(run, run)   // 直前のトランザクション完了後に直列実行
  lock = result.catch(() => {})
  return result
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

export const fetchResources: FetchResources = async ({ isPublic }) => {
  const rows = readTable<Resource>(TABLE)
  return isPublic !== undefined ? rows.filter((r) => r.isPublic === isPublic) : rows
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

YAML 実装は `db` を destructure しない（型には含まれるが未使用）。トランザクション内の書き込みは即座に
ファイルへ反映されるため、同一トランザクション内の後続 read は自分の書き込みを見られる。失敗時は
`runYamlTransaction` がスナップショットへ巻き戻す。

---

## トランザクションと実装の切り替え

```ts
// app/(shared)/lib/transaction.ts
import { db } from "@/drizzle/db"
import type { Db } from "@/drizzle/db"
import { runYamlTransaction } from "./yamlStore"

const useYaml = process.env.USE_YAML_DB === "true"
const YAML_DB = {} as Db   // YAML モードで leaf に渡すダミー（leaf 側は使わない）

/** トランザクション境界。本番=Drizzle tx、ローカル=YAML スナップショット/ロールバック */
export const transaction = <T>(fn: (db: Db) => Promise<T>): Promise<T> =>
  useYaml ? runYamlTransaction(() => fn(YAML_DB)) : db.transaction(fn)

/** トランザクション外の単発呼び出し用 db */
export const baseDb: Db = useYaml ? YAML_DB : db
```

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

`service.ts` がトランザクション境界を持つ（quest-pay と同じ）。`transaction()` が渡す `db` を
各関数にスレッドする。失敗すれば本番は Drizzle がロールバック、ローカルは YAML がスナップショット復元。

```ts
// app/api/v1/resources/service.ts
import { transaction, baseDb } from "@/app/(shared)/lib/transaction"
import { fetchResource } from "./query"
import { insertResource } from "./db"
import { insertResourceTags } from "../tags/db"
import type { ResourceInsert } from "@/drizzle/schema"
import { NotFoundError } from "@/app/(shared)/errors/appError"

/** 単発取得（トランザクション不要） */
export const getResource = async ({ id }: { id: string }) => {
  const resource = await fetchResource({ db: baseDb, id })
  if (!resource) throw new NotFoundError("リソースが見つかりません。")
  return resource
}

/** 登録（リソース + タグを 1 トランザクションで。途中失敗は全て巻き戻る） */
export const registerResource = ({ record, tags }: { record: ResourceInsert; tags: string[] }) =>
  transaction(async (db) => {
    const { id } = await insertResource({ db, record })
    if (tags.length > 0) await insertResourceTags({ db, resourceId: id, tags })
    return { id }
  })
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
- 引数はオブジェクトで受け、`db` を含める（quest-pay 準拠）。本番は渡された `db`(tx) を使い、YAML は無視する
- 読み取りは `query.ts`、書き込みは `db.ts` に分離（既存の `クエリ-ts.md` / `DB-ts.md` 準拠）
- 切り替えは `query.ts` / `db.ts` の re-export と `transaction.ts` のみ。実装ファイル（`*.drizzle.ts` / `*.yaml.ts`）は env を見ない
- トランザクション境界は `service.ts` が `transaction()` で持つ。複数テーブルの更新は必ず `transaction()` 内で行う
- YAML のロールバックは `data/dev/` 全体のスナップショット復元、同時実行は in-process ロックで直列化（単一プロセス・ローカル開発専用。分散ロックは想定しない）
- `data/dev/` は必ず `.gitignore` に追加する（機密データ流出防止）
- 本番ビルドに YAML 実装を混入させない（`USE_YAML_DB` のガードを守る）
