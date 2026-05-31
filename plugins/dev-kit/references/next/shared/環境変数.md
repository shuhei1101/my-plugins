# Next.js App Router — Environment & Configuration

> **方針**: 環境変数は **秘密情報のみ**、構造化された設定は **YAML** に置く。
> **なぜ YAML**: Python（AITuber 等）と Next.js 両方から読める設定ファイルを共有できるため、バックエンドが Python の場合に設定を 1 箇所に集約できる。Next.js 単独でも構造・コメント・git 履歴のメリットがある。

---

## 2 層構成

| 層 | File | 内容 | git 管理 |
|---|---|---|---|
| 秘密情報 | `.env.local`（dev）/ Vercel ダッシュボード（prod） | API key, DB password, OAuth secret | ❌ |
| 構造化設定 | `config/settings.yaml` | アプリパラメータ・機能フラグ・モデル選択 | ✅ |
| サンプル | `.env.sample`, `config/settings.sample.yaml` | テンプレ + コメント | ✅ |

---

## どこに何を置くか

| 値 | 置き場所 |
|---|---|
| DB password, OAuth secret, Stripe secret | `.env.local`（秘密） |
| Supabase URL / Anon Key | 環境差があれば `.env`、なければ `settings.yaml` |
| LLM モデル名、retry 回数、timeout | `settings.yaml` |
| 機能フラグ | `settings.yaml` の `features:` |
| UI 文字列・コピー | `settings.yaml` または専用ファイル |
| Log level, debug flag | `settings.yaml`（env で上書き可） |
| ハードコードでよい定数（最大長等） | `app/(shared)/constants.ts` |

---

## 決定フロー

```
環境間（dev/staging/prod）で値が違う?
  → No → app/(shared)/constants.ts（TS const）
  → Yes → 次へ

秘密?
  → Yes → 環境変数（.env.local / Vercel）
  → No → 次へ

構造を持つ?（ネストオブジェクト、配列）
  → Yes → settings.yaml
  → No → settings.yaml（git 可視化のため推奨）or env（フラット 1 行のみ）
```

デフォルト: **YAML config**。env は本物の秘密と `NODE_ENV` 程度に限定。

---

## TypeScript 定数

環境で変わらない値:

```ts
// app/(shared)/constants.ts

/** ページング既定 */
export const DEFAULT_PAGE_SIZE = 20

/** 名前最大文字数 */
export const RESOURCE_NAME_MAX = 20

/** API タイムアウト（ms） */
export const API_TIMEOUT_MS = 30_000
```

UPPER_SNAKE_CASE。`// セクション` でグルーピング。

---

## 環境変数

### ファイル配置

```
packages/web/
├── .env.local        # dev（git 除外）
├── .env.sample       # テンプレ（git 管理、コメント付き）
└── （prod は Vercel ダッシュボード）
```

`.env.sample` を **必要変数の正式リスト** にする。

### NEXT_PUBLIC_ プレフィックス

| 変数の用途 | プレフィックス | 露出 |
|---|---|---|
| クライアント（ブラウザ）で読む | `NEXT_PUBLIC_` | ブラウザ JS にバンドル（公開） |
| サーバーのみ | なし | サーバー専用（クライアントに送られない） |

```bash
# ✅ クライアント可
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

# ✅ サーバー専用
SUPABASE_SERVICE_ROLE_KEY=eyJ...
STRIPE_SECRET_KEY=sk_...
DATABASE_URL=postgresql://...
```

**シークレットには絶対 `NEXT_PUBLIC_` を付けない**。ビルド時にクライアント JS に埋め込まれる。

### Next.js 16 のランタイム env

`serverRuntimeConfig` / `publicRuntimeConfig` は **Next.js 16 で廃止**。`process.env.*` を直接使う。

ランタイムで読みたい（ビルド時に固定したくない）場合は `connection()` を使う:

```tsx
import { connection } from "next/server"

export default async function Page() {
  await connection()                            // ここでバウンダリ
  const config = process.env.RUNTIME_CONFIG     // ランタイムで評価
  return <p>{config}</p>
}
```

### t3-env 推奨

型安全な env 管理に `@t3-oss/env-nextjs`:

```bash
pnpm add @t3-oss/env-nextjs zod
```

```ts
// env.ts
import { createEnv } from "@t3-oss/env-nextjs"
import { z } from "zod"

export const env = createEnv({
  server: {
    DATABASE_URL: z.string().url(),
    STRIPE_SECRET_KEY: z.string().min(1),
  },
  client: {
    NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
    NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(1),
  },
  experimental__runtimeEnv: {
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  },
})
```

```ts
import { env } from "@/env"
const url = env.NEXT_PUBLIC_SUPABASE_URL    // 型安全
```

ビルド時に env がそろわないと失敗 → デプロイ時の設定漏れを防ぐ。

---

## YAML config

```yaml
# config/settings.yaml

app:
  name: "Quest Pay"
  defaultTheme: "light"       # "light" | "dark"
  defaultPageSize: 20

features:
  publicQuest: true
  socialLogin: false
  payment: true

api:
  timeoutMs: 30000
  retryCount: 0

logger:
  level: "info"              # NEXT_PUBLIC_LOG_LEVEL で上書き可
  format: "jsonl"

stripe:
  publishableKey: "pk_test_..."   # 公開キーは OK
  # secretKey は .env の STRIPE_SECRET_KEY を参照
```

### ロード

```ts
// app/(shared)/config.ts
import { readFileSync } from "fs"
import { resolve } from "path"
import { parse } from "yaml"
import { z } from "zod"

const ConfigSchema = z.object({
  app: z.object({
    name: z.string(),
    defaultTheme: z.enum(["light", "dark"]),
    defaultPageSize: z.number().int().positive(),
  }),
  features: z.record(z.string(), z.boolean()),
  api: z.object({
    timeoutMs: z.number(),
    retryCount: z.number(),
  }),
  logger: z.object({
    level: z.enum(["debug", "info", "warn", "error"]),
    format: z.enum(["jsonl", "text"]),
  }),
})

export type Config = z.infer<typeof ConfigSchema>

let cached: Config | null = null

export const loadConfig = (): Config => {
  if (cached) return cached
  const raw = readFileSync(resolve(process.cwd(), "config/settings.yaml"), "utf-8")
  cached = ConfigSchema.parse(parse(raw))
  return cached
}
```

### env override（log level 等）

```ts
export const loadConfig = (): Config => {
  if (cached) return cached
  const raw = readFileSync(resolve(process.cwd(), "config/settings.yaml"), "utf-8")
  let cfg = ConfigSchema.parse(parse(raw))

  // log level を env で上書き
  if (process.env.NEXT_PUBLIC_LOG_LEVEL) {
    cfg = { ...cfg, logger: { ...cfg.logger, level: process.env.NEXT_PUBLIC_LOG_LEVEL as any } }
  }

  cached = cfg
  return cfg
}
```

---

## クライアントへの config 公開

YAML はサーバー側でしか読めない。クライアントに渡すには:

### A. ビルド時インライン（推奨、PR135）

```ts
// next.config.ts
import { loadConfig } from "./app/(shared)/config"

const config = loadConfig()

export default {
  env: {
    APP_CONFIG: JSON.stringify({
      app: config.app,
      features: config.features,
      logger: { level: config.logger.level, format: config.logger.format },
    }),
  },
}
```

クライアント:

```ts
const APP_CONFIG = JSON.parse(process.env.APP_CONFIG!) as { app, features, logger }
```

ビルド時に固定 → ランタイムコスト 0。

### B. API ルート経由（変更頻度が高い値）

```ts
// app/api/v1/config/public/route.ts
import { NextResponse } from "next/server"
import { loadConfig } from "@/app/(shared)/config"

export async function GET() {
  const cfg = loadConfig()
  return NextResponse.json({
    data: { app: cfg.app, features: cfg.features },
  })
}
```

`useQuery({ queryKey: ["publicConfig"], staleTime: Infinity })` でフェッチ。設定変更を再デプロイなしで反映できる。

ハイブリッド: 変更頻度の低いものはビルド時、高いものは API。

---

## 機能フラグの拡張（QA-068）

シンプル：`settings.yaml` の `features:` で boolean フラグ。

将来：ユーザー別 / 段階リリースが必要なら `GrowthBook` / `Statsig` / `LaunchDarkly` 等に拡張する。`feature-flags` SDK のラッパーを `app/(shared)/feature-flags.ts` に置けば置き換え容易。

```ts
// app/(shared)/feature-flags.ts
import { loadConfig } from "./config"

export const isFeatureEnabled = (name: string): boolean => {
  const cfg = loadConfig()
  return Boolean(cfg.features[name])
}
```

将来:

```ts
import { GrowthBook } from "@growthbook/growthbook"

const gb = new GrowthBook({ apiHost: "...", clientKey: "..." })

export const isFeatureEnabled = (name: string, userId?: string): boolean => {
  return gb.isOn(name)
}
```

---

## やってはいけない

- 秘密を `settings.yaml` に書く（git に乗る）
- ネスト構造を `.env` に詰め込む（フラットで型なし）
- `process.env` を散在的に読む（型なし）→ `env.ts` で一元化
- `NEXT_PUBLIC_` をシークレットに付ける
- config loader を複数 fork して維持する

---

## Constraints

- 秘密 → env vars
- 構造化設定 → YAML（バックエンドが Python のプロジェクトで共有可能、QA-058）
- 単純定数 → TS const
- すべての env 変数を `env.ts`（t3-env）または `env.d.ts` で型定義
- すべての env 変数を `.env.sample` に記載
- YAML は Zod でバリデーション（fail fast）
- `NEXT_PUBLIC_` をシークレットに付けない
- 機能フラグは段階的に拡張可能な抽象を維持
- クライアント config はビルド時インラインを推奨、頻繁変更だけ API
