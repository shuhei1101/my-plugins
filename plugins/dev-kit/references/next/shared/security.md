# Next.js App Router — Security

> **対象**: セキュリティヘッダ・CSRF・XSS・SQL Injection・Open Redirect・Dependency vulnerabilities の防御。

---

## セキュリティヘッダ

`next.config.ts` の `headers()` で全レスポンスに付与:

```ts
// next.config.ts
import type { NextConfig } from "next"

const securityHeaders = [
  // クリックジャッキング防止
  { key: "X-Frame-Options", value: "SAMEORIGIN" },

  // MIME sniff 防止
  { key: "X-Content-Type-Options", value: "nosniff" },

  // 公開 referrer 抑制
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },

  // HSTS（HTTPS 強制 1 年、サブドメイン含む）
  { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" },

  // 古いブラウザ向け XSS 保護（モダンでは CSP 推奨）
  { key: "X-XSS-Protection", value: "1; mode=block" },

  // Permissions Policy（不要権限のオフ）
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=(self)" },

  // CSP — 要件に応じて
  // { key: "Content-Security-Policy", value: cspValue },
]

const nextConfig: NextConfig = {
  async headers() {
    return [{ source: "/(.*)", headers: securityHeaders }]
  },
}

export default nextConfig
```

---

## Content Security Policy (CSP)

```ts
const cspValue = [
  "default-src 'self'",
  "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://vercel.live",
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' blob: data: https:",
  "font-src 'self' data:",
  "connect-src 'self' https://*.supabase.co https://api.stripe.com wss:",
  "frame-src 'self' https://js.stripe.com",
  "frame-ancestors 'none'",
  "form-action 'self'",
  "base-uri 'self'",
].join("; ")
```

nonce 利用で `'unsafe-inline'` を外す（推奨）:

```ts
// proxy.ts
import { NextResponse } from "next/server"
import crypto from "crypto"

export function proxy(request: NextRequest) {
  const nonce = crypto.randomBytes(16).toString("base64")
  const csp = `script-src 'self' 'nonce-${nonce}' 'strict-dynamic'; ...`
  const response = NextResponse.next({ request: { headers: new Headers(request.headers).set("x-nonce", nonce) } })
  response.headers.set("Content-Security-Policy", csp)
  return response
}
```

Server Component で nonce を script tag に付与:

```tsx
import { headers } from "next/headers"

const nonce = (await headers()).get("x-nonce")
<script nonce={nonce}>...</script>
```

---

## CSRF

### Server Actions

Next.js Server Actions は **同一 origin チェックを自動**で行う。POST に Form Action として送信されるリクエストには Next.js が自動的に Origin と Host を照合。クロスオリジン攻撃は拒否される。

明示的に追加設定なしで CSRF 対策完了。

### route.ts での mutation

GET 以外は `Origin` ヘッダを検証:

```ts
const isAllowedOrigin = (origin: string | null) => {
  if (!origin) return false
  const allowed = [process.env.NEXT_PUBLIC_APP_URL!]
  return allowed.includes(origin)
}

export async function POST(request: NextRequest) {
  if (!isAllowedOrigin(request.headers.get("origin"))) {
    return NextResponse.json({ error: { code: "CSRF" } }, { status: 403 })
  }
  // ...
}
```

または SameSite Cookie + 認証 cookie で間接的に防御:

```ts
// auth コールバックで
cookies().set("session_token", token, {
  httpOnly: true,
  secure: true,
  sameSite: "strict",
  maxAge: 60 * 60 * 24 * 30,
})
```

---

## XSS

### React + JSX

React は文字列補間時に自動エスケープするため XSS は基本的に防げる:

```tsx
<p>{userInput}</p>      // 安全（自動エスケープ）
```

危険なのは `dangerouslySetInnerHTML`:

```tsx
<div dangerouslySetInnerHTML={{ __html: userInput }} />  // ❌ 危険
```

→ Markdown 等を表示するなら `marked` + `DOMPurify`:

```tsx
import { marked } from "marked"
import DOMPurify from "isomorphic-dompurify"

const safe = DOMPurify.sanitize(marked.parse(userInput))
<div dangerouslySetInnerHTML={{ __html: safe }} />
```

### URL の `javascript:`

ユーザー入力の URL を `<a href>` に流すなら検証:

```ts
const sanitizeUrl = (raw: string) => {
  try {
    const url = new URL(raw, "https://example.com")
    if (!["http:", "https:"].includes(url.protocol)) return "#"
    return url.toString()
  } catch {
    return "#"
  }
}
```

---

## SQL Injection

Drizzle ORM の SQL Builder / Relational Queries は **parametrized query** を発行するため、通常の使い方では SQL Injection は起きない:

```ts
// ✅ 安全
await db.select().from(resources).where(eq(resources.id, userInput))

// ✅ 安全（パラメータ）
await db.execute(sql`SELECT * FROM resources WHERE id = ${userInput}`)
```

危険なのは生 SQL の文字列結合:

```ts
// ❌ 危険
await db.execute(sql.raw(`SELECT * FROM resources WHERE id = '${userInput}'`))
```

`sql.raw` は使わない。

---

## Open Redirect

`redirect()` に外部 URL を直接渡さない:

```ts
// ❌ 危険
redirect(searchParams.get("from") ?? "/home")

// ✅ 安全
const from = searchParams.get("from") ?? "/home"
const safe = from.startsWith("/") && !from.startsWith("//") ? from : "/home"
redirect(safe)
```

---

## Mass Assignment

クライアントから来た任意のフィールドを DB に直接 INSERT しない:

```ts
// ❌ 危険（クライアントが isAdmin: true を送れる）
await db.insert(users).values(body)

// ✅ 安全（Zod で許可フィールドだけ抽出）
const data = PostUserSchema.parse(body)
await db.insert(users).values(data)
```

Zod スキーマで許可フィールドを制限する。

---

## 認証セッション

- httpOnly + Secure + SameSite=strict cookie
- セッショントークンは長いランダム文字列（64 文字 base64）
- セッション有効期限（30 日 + sliding renewal）
- ログアウト時にサーバー側 token も無効化
- 異常な session を検知してログアウト（IP / UA 変化）

詳細: `backend/auth.md`

---

## 入力バリデーション

すべての外部入力を Zod で `.parse`:

```ts
// route.ts
const body = await request.json()
const data = SchemaA.parse(body)

// Server Action
const data = SchemaB.parse(input)

// URL クエリ
const sp = SchemaC.parse(Object.fromEntries(searchParams))
```

検証なしで DB に渡さない。

---

## Dependency vulnerabilities

定期的に脆弱性チェック:

```bash
pnpm audit
pnpm update --interactive
```

CI で `pnpm audit --prod` を回す。

---

## Secret rotation

- DB password, OAuth secret は定期的にローテーション（半年〜1 年）
- リーク疑いがあれば即時ローテ
- Vercel ダッシュボードで秘密を変更してリデプロイ

---

## エラーレスポンス

内部詳細（stack trace, DB query）をクライアントに見せない:

```ts
// ❌
return NextResponse.json({ error: e.stack }, { status: 500 })

// ✅
log.error("internal", { stack: e.stack })
return NextResponse.json({ error: { code: "INTERNAL", message: "予期せぬエラー" } }, { status: 500 })
```

---

## Rate limiting & Bot 対策

詳細: `backend/rate-limit.md`

- 認証 / ログイン API には厳しい rate limit
- フォーム POST には Cloudflare Turnstile 等の CAPTCHA
- 異常検知（短時間に多くの 401 / 429）でアカウントロック

---

## File upload セキュリティ

- ファイルサイズ制限
- MIME タイプホワイトリスト
- 拡張子チェック（クライアントの偽装に注意）
- 別ドメイン / バケットに保存（XSS で生成された html を実行させない）
- アンチウイルススキャン（重要なら）

---

## Constraints

- セキュリティヘッダを `next.config.ts` で全レスポンス付与
- CSP を nonce ベースで設定（`'unsafe-inline'` 排除）
- Server Actions の CSRF 自動チェックを信頼、外部 mutation API は Origin 検証
- すべての外部入力を Zod で validate
- 生 SQL（`sql.raw`）禁止
- `dangerouslySetInnerHTML` を使うなら DOMPurify で sanitize
- `redirect()` の外部 URL チェック
- Mass Assignment 防止（Zod で許可フィールド抽出）
- secret は env / Vercel ダッシュボード、`NEXT_PUBLIC_` 禁止
- エラーレスポンスに stack trace 出さない
- `pnpm audit` を定期 / CI で実行
