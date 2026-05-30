<!-- This file is a Japanese mirror of db-migration.md. When updating the English original, update this file too. -->
# Drizzle — マイグレーション運用

`drizzle-kit` を使った schema → SQL migration → DB 適用の流れ。

---

## 設定

```ts
// drizzle.config.ts
import { defineConfig } from "drizzle-kit"

export default defineConfig({
  schema: "./drizzle/schema.ts",
  out: "./drizzle/migrations",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
})
```

---

## 手順

```bash
# 1) schema.ts を編集後、SQL migration を生成
pnpm drizzle-kit generate

# 2) 確認（dry-run）
pnpm drizzle-kit migrate --dry-run

# 3) 適用
pnpm drizzle-kit migrate

# 4) ローカル DB 確認
pnpm drizzle-kit studio    # GUI で DB を確認
```

---

## 環境別の運用

| 環境 | 適用方法 |
|---|---|
| ローカル | `pnpm drizzle-kit migrate` を手動実行 |
| Preview（Vercel） | デプロイ前に手動 or CI で `DATABASE_URL` を切り替えて実行 |
| Production | **明示的に** 手動 / 専用 job で実行（自動適用 NG） |

production 自動適用は事故の元（誤ったマイグレーション → DB 破壊）。Production migration は別 job / 手動承認制が推奨。

---

## マイグレーションファイルの命名

`drizzle-kit generate` が `0000_quiet_madame_masque.sql` のような名前で生成。

| 命名規則を整えたいとき |
|---|
| `pnpm drizzle-kit generate --name add-user-type` で名前付け |
| `0001_add_user_type.sql` のような形になる |

---

## 破壊的変更（カラム削除・型変更）

drizzle-kit は基本的に **追加系（ALTER TABLE ADD COLUMN）は自動**、削除・型変更は **対話的確認** で生成。

破壊的変更の手順:

1. アプリケーション側で旧カラム参照を全て削除（or 二重書き対応）
2. デプロイ → 旧コードが本番に残らないように
3. `pnpm drizzle-kit generate` で削除 migration 生成
4. 適用

「コード変更 → schema 変更」の順を厳守。

---

## Enum の値追加

```ts
// 値を配列に追加
export const resourceStatus = pgEnum("resource_status", [
  "draft",
  "published",
  "archived",
  "scheduled",   // 追加
])
```

```bash
pnpm drizzle-kit generate
# → ALTER TYPE "resource_status" ADD VALUE 'scheduled';
```

**Enum 値の削除は基本不可**（既存データへの影響）。値を非推奨にする場合はコメントで示し、DB から消すのは別 PR で段階的に。

詳細: `db-enum.md`

---

## マイグレーションファイルの編集

drizzle-kit が生成した SQL が意図と違う場合、**マイグレーションファイルを手動編集** してから適用:

```sql
-- drizzle/migrations/0005_xxx.sql
-- 自動生成: ALTER TABLE users ADD COLUMN role text;
-- 手動編集: NOT NULL with default
ALTER TABLE users ADD COLUMN role text NOT NULL DEFAULT 'user';
```

ただし schema.ts も合わせる:

```ts
role: text("role").notNull().default("user"),
```

---

## マイグレーションのロールバック

drizzle-kit には **down migration はない**。ロールバックが必要な場合:

1. 「逆向き」の schema 変更を新しい migration として書く
2. または DB から手動で `ALTER TABLE ... DROP COLUMN ...`

production では **デプロイ前に必ずバックアップ**。Vercel + Neon なら branch でテスト → 本番反映の流れ。

---

## ルール

- schema 変更後は必ず `generate` → 確認 → `migrate`
- 破壊的変更は **コード側の参照削除を先**
- production 自動適用 NG（手動 / 専用 job）
- マイグレーションファイルは git にコミット
- 生成された SQL は **手で編集 OK**（だが schema.ts と矛盾しないこと）
- Enum 値削除は段階的に

## 関連 references

- `db-id.md`, `db-timestamps.md`, `db-enum.md`, `db-relations.md` — schema 定義
- `devops/deploy.md` — デプロイ時のマイグレーション運用

## 禁止

- production 自動マイグレーション
- マイグレーションファイルを git 管理外に
- schema.ts と migration の SQL が乖離した状態でコミット
- カラム削除を「コードがまだ参照中」の状態でデプロイ
