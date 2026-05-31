# ローカル開発 YAML リポジトリパターン — TypeScript インターフェースによる DB 切り替え

dev-kit の Next.js バックエンドリファレンスで採用するローカル開発用 DB 切り替えパターン。

---

## 概要

TypeScript インターフェース（`IResourceRepository`）でデータアクセス層を抽象化し、
本番は Drizzle/Supabase、ローカル開発時は YAML ファイルを DB 代替として使う。

環境変数 `USE_YAML_DB=true`（`.env.local`）を設定するだけで切り替わる。

---

## フォルダ構成

```
lib/
└── repositories/
    ├── types.ts                    # インターフェース
    ├── index.ts                    # ファクトリ関数
    ├── drizzle/ResourceRepository.ts  # 本番
    └── yaml/ResourceRepository.ts    # ローカル
dev-data/                           # YAML データ（gitignore）
```

## 切り替えポイント

```ts
// lib/repositories/index.ts
export const getResourceRepository = (): IResourceRepository =>
  process.env.USE_YAML_DB === "true"
    ? new YamlResourceRepository()
    : new DrizzleResourceRepository(db)
```

## 注意事項

- `dev-data/` は必ず `.gitignore` に追加する
- YAML 実装は同期 I/O（ローカル専用のため許容）
- `service.ts` は `getResourceRepository()` 経由で使い、`db` を直接 import しない

---

## 変更履歴

| # | 日付 | 概要 |
|---|---|---|
| 1 | 2026-06-01 | 初版作成 |
