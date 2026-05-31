# ローカル開発 YAML リポジトリパターン — type + ファクトリ関数による DB 切り替え

dev-kit の Next.js バックエンドリファレンスで採用するローカル開発用 DB 切り替えパターン。

---

## 概要

TypeScript の `type`（`ResourceRepository`）でデータアクセス層を抽象化し、
本番は Drizzle/Supabase、ローカル開発時は YAML ファイルを DB 代替として使う。
クラス・`interface`・`I` プレフィックスは使わず、ファクトリ関数が型を満たすオブジェクトを返す関数型スタイル。

環境変数 `USE_YAML_DB=true`（`.env.local`）を設定するだけで切り替わる。

---

## フォルダ構成

```
lib/
└── repositories/
    ├── types.ts     # ResourceRepository 型定義
    ├── index.ts     # getResourceRepository（切り替えポイント）
    ├── drizzle.ts   # createDrizzleResourceRepository
    └── yaml.ts      # createYamlResourceRepository
dev-data/            # YAML データ（gitignore）
```

## 切り替えポイント

```ts
// lib/repositories/index.ts
export const getResourceRepository = (): ResourceRepository =>
  process.env.USE_YAML_DB === "true"
    ? createYamlResourceRepository()
    : createDrizzleResourceRepository(db)
```

## スタイル方針

- `type` で契約を定義（`interface` は使わない）
- ファクトリ関数名: `create{Store}{Resource}Repository`
- クラス不使用

## 注意事項

- `dev-data/` は必ず `.gitignore` に追加する
- YAML 実装は同期 I/O（ローカル専用のため許容）
- `service.ts` は `getResourceRepository()` 経由で使い、`db` を直接 import しない

---

## 変更履歴

| # | 日付 | 概要 |
|---|---|---|
| 1 | 2026-06-01 | 初版作成 |
| 2 | 〃 | クラス/interface 廃止・type + ファクトリ関数スタイルに変更 |
