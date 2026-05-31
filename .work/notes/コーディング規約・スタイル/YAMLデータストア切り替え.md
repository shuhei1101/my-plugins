# ローカル開発 YAML データストア — 関数ごとの type 定義による実装切り替え

dev-kit の Next.js バックエンドリファレンスで採用するローカル開発用 DB 切り替えパターン。

リファレンス: `plugins/dev-kit/references/next/backend/ローカルYAML開発DB.md`

---

## 概要

`query.ts`（読み取り）/ `db.ts`（書き込み）のデータアクセス関数を、本番（Drizzle/Supabase）と
ローカル（YAML ファイル）で差し替える。環境変数 `USE_YAML_DB=true`（`.env.local`）で切り替わる。

quest-pay の実コードスタイルに準拠：

- **素の関数**（`fetchResource` / `insertResource` / `updateResource` / `deleteResource`）
- 引数は**オブジェクト**（`{ id }` / `{ record }`）
- **クラス・`interface`・Repository は使わない**
- 関数 1 つにつき `type` を 1 つ定義（`FetchResource` ↔ `fetchResource`）

---

## フォルダ構成

```
app/api/v1/resources/
├── types.ts          # 関数ごとの型定義
├── query.ts          # 読み取り切り替え（re-export）
├── query.drizzle.ts  / query.yaml.ts
├── db.ts             # 書き込み切り替え（re-export）
└── db.drizzle.ts     / db.yaml.ts
app/(shared)/lib/yamlStore.ts   # 汎用 YAML 読み書き
data/dev/*.yaml                 # ローカルデータ（gitignore）
```

## 型定義スタイル

```ts
// types.ts
export type FetchResource = (args: { id: string }) => Promise<Resource | null>
export type InsertResource = (args: { record: ResourceInsert }) => Promise<{ id: string }>
```

```ts
// query.drizzle.ts / query.yaml.ts どちらも同じ型を満たす
export const fetchResource: FetchResource = async ({ id }) => { ... }
```

## 切り替え

```ts
// db.ts
import * as drizzle from "./db.drizzle"
import * as yaml from "./db.yaml"
const impl = process.env.USE_YAML_DB === "true" ? yaml : drizzle
export const insertResource = impl.insertResource
```

## 注意事項

- `data/dev/` は必ず `.gitignore` に追加する
- 実装ファイル（`*.drizzle.ts` / `*.yaml.ts`）は env を見ない。切り替えは `query.ts` / `db.ts` の re-export のみ
- YAML モードはトランザクション非対応（複数テーブル整合性が必要な処理は本番 Drizzle 側に閉じる）

---

## 変更履歴

| # | 日付 | 概要 |
|---|---|---|
| 1 | 2026-06-01 | 初版作成 |
| 2 | 〃 | クラス/interface 廃止・type + ファクトリ関数スタイルに変更 |
| 3 | 〃 | データ置き場を `dev-data/` → `data/dev/` に変更 |
| 4 | 〃 | quest-pay 準拠に全面見直し（関数ごとの type 定義・素の関数・query.ts/db.ts 分離）。ファイル名を `ローカルYAML開発DB.md` にリネーム |
