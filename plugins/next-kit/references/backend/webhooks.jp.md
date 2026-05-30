<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Next.js App Router — Webhook Receiver

> **対象**: Stripe / GitHub / Slack 等の Webhook を受信するパターン。

---

## 配置

```
app/api/v1/webhooks/{provider}/route.ts
```

例: `app/api/v1/webhooks/stripe/route.ts`

---

## 基本パターン

```ts
// app/api/v1/webhooks/stripe/route.ts
import { NextRequest, NextResponse } from "next/server"
import { logger } from "@/app/(shared)/logger"
import { stripe } from "@/app/(shared)/lib/stripe"
import { handleStripeEvent } from "./service"

const log = logger.create("webhook:stripe")

export async function POST(request: NextRequest) {
  const signature = request.headers.get("stripe-signature")
  if (!signature) return new NextResponse("Missing signature", { status: 400 })

  const body = await request.text()    // 署名検証のため raw body が必要

  let event
  try {
    event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET!)
  } catch (e) {
    log.error("signature verification failed", { error: (e as Error).message })
    return new NextResponse("Invalid signature", { status: 400 })
  }

  // idempotency: 同じ event.id を 2 回処理しない
  const alreadyProcessed = await checkProcessedEvent(event.id)
  if (alreadyProcessed) {
    log.info("event already processed", { id: event.id, type: event.type })
    return new NextResponse(null, { status: 200 })
  }

  try {
    await handleStripeEvent(event)
    await markEventProcessed(event.id)
  } catch (e) {
    log.error("webhook processing failed", { id: event.id, type: event.type, error: (e as Error).message })
    return new NextResponse("Processing failed", { status: 500 })
    // Stripe は 5xx を受け取ると自動リトライする
  }

  return new NextResponse(null, { status: 200 })
}
```

---

## 重要ポイント

### 1. 署名検証（必須）

Webhook の URL は公開されるため、署名検証なしだと誰でも叩ける。Stripe / GitHub / Slack それぞれの公式ライブラリで検証。

| プロバイダ | 関数 |
|---|---|
| Stripe | `stripe.webhooks.constructEvent(body, signature, secret)` |
| GitHub | HMAC-SHA256 + secret で `X-Hub-Signature-256` 検証 |
| Slack | HMAC-SHA256 + signing secret で `X-Slack-Signature` 検証 |

### 2. raw body

署名検証には **raw body** が必要。`await request.text()` で生文字列を取得（`request.json()` だと検証に失敗）。

### 3. Idempotency

同じイベントが複数回届く可能性がある（Webhook 仕様）。DB の `processed_events` テーブル（または Redis）で `event.id` を保存し、二重処理を防ぐ:

```ts
// drizzle/schema.ts
export const processedEvents = pgTable("processed_events", {
  id: text("id").primaryKey(),
  provider: text("provider").notNull(),
  eventType: text("event_type").notNull(),
  processedAt: timestamp("processed_at").notNull().defaultNow(),
})
```

```ts
const checkProcessedEvent = async (eventId: string) =>
  Boolean(await db.query.processedEvents.findFirst({ where: eq(processedEvents.id, eventId) }))

const markEventProcessed = async (eventId: string) =>
  await db.insert(processedEvents).values({ id: eventId, provider: "stripe", eventType: "..." })
```

### 4. レスポンス時間

Webhook は素早く 2xx を返すべき。重い処理は **バックグラウンドジョブに enqueue**（`backend/jobs.md`）して即時 200 を返す:

```ts
await enqueueJob({ type: "process-stripe-event", payload: event })
return new NextResponse(null, { status: 200 })
```

### 5. リトライポリシー

5xx を返すと多くのプロバイダが自動リトライする（exponential backoff）。失敗を投げるかどうかは「リトライしてほしいか」で判断。

---

## Stripe 設定例

```ts
// app/(shared)/lib/stripe.ts
import Stripe from "stripe"

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2024-11-20.acacia",
})
```

```ts
// app/api/v1/webhooks/stripe/service.ts
import type Stripe from "stripe"

export const handleStripeEvent = async (event: Stripe.Event) => {
  switch (event.type) {
    case "checkout.session.completed":
      await handleCheckoutCompleted(event.data.object)
      break
    case "customer.subscription.deleted":
      await handleSubscriptionDeleted(event.data.object)
      break
    default:
      // 未対応イベントは無視（ログだけ）
      break
  }
}
```

---

## GitHub Webhook 例

```ts
import { createHmac, timingSafeEqual } from "crypto"

const verifyGithubSignature = (body: string, signature: string) => {
  const hmac = createHmac("sha256", process.env.GITHUB_WEBHOOK_SECRET!)
  hmac.update(body)
  const expected = `sha256=${hmac.digest("hex")}`
  return timingSafeEqual(Buffer.from(expected), Buffer.from(signature))
}

export async function POST(request: NextRequest) {
  const signature = request.headers.get("x-hub-signature-256")
  if (!signature) return new NextResponse("Missing signature", { status: 400 })

  const body = await request.text()
  if (!verifyGithubSignature(body, signature)) {
    return new NextResponse("Invalid signature", { status: 400 })
  }

  const event = JSON.parse(body)
  const eventType = request.headers.get("x-github-event")
  // ... 処理
  return new NextResponse(null, { status: 200 })
}
```

---

## ローカル開発

Webhook を localhost で受けるには:
- **Stripe**: `stripe listen --forward-to localhost:3000/api/v1/webhooks/stripe`
- **GitHub / Slack**: `ngrok http 3000`、`smee.io`

---

## Constraints

- 配置は `app/api/v1/webhooks/{provider}/route.ts`
- **署名検証必須**（公式ライブラリ or HMAC 自前）
- raw body 取得（`await request.text()`）
- イベント ID で idempotency 担保（DB or Redis）
- 重い処理は jobs に enqueue → 即 200 を返す
- 失敗時に 5xx を返すとリトライされる（意図したケースだけ）
- WEBHOOK_SECRET 等は env で管理（PUBLIC prefix なし）
- ロガーにはイベント ID・type・処理結果を必ず記録
