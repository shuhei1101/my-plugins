# Next.js App Router — Logger

## Setup

The logger is a singleton instance using `loglevel`.
Import it from `app/(core)/logger.ts`.

```ts
import { logger } from "@/app/(core)/logger"
```

---

## Log levels

| Level | Method | Use for |
|---|---|---|
| debug | `logger.debug(msg, data?)` | Development-only details (params, intermediate values) |
| info | `logger.info(msg, data?)` | Normal operation events (start / complete of key operations) |
| warn | `logger.warn(msg, data?)` | Unexpected but recoverable situations |
| error | `logger.error(msg, error?)` | Errors that require attention |

Priority: `debug < info < warn < error`

---

## Usage patterns

```ts
// Basic message
logger.info("家族登録処理を開始")

// With structured data (second argument)
logger.info("家族登録処理完了", { userId, familyId })
logger.debug("リクエスト受信", { path: request.nextUrl.pathname, method: request.method })

// Warning
logger.warn("リトライします", { attempt, maxRetries })

// Error — pass the error object as second argument
logger.error("家族登録中にエラー", error)
logger.error("DBクエリ失敗", { error: error.message, table: "families" })
```

---

## Log level configuration

```bash
# .env.local
NEXT_PUBLIC_LOG_LEVEL=debug    # local development — all logs visible

# Production (Vercel / hosting)
NEXT_PUBLIC_LOG_LEVEL=warn     # production — warn and error only
```

The logger reads `process.env.NEXT_PUBLIC_LOG_LEVEL` at initialization.

---

## Where to log

| Layer | Log what |
|---|---|
| `route.ts` | Request start (`info`), validation complete (`debug`), response sent (`info`) |
| `service.ts` | Key business operations start/complete (`info`), intermediate steps (`debug`) |
| `db.ts` | Not typically logged (service.ts covers it) |
| `client.ts` | Fetch start (`debug`), response received (`debug`), error (`error`) |
| Screen / hooks | User actions and state transitions (`debug`) |

---

## Constraints

- Never use `console.log`, `console.error`, or `console.warn` — use `logger` only
- Never log passwords, tokens, session IDs, or personally identifiable information
- Always pass error objects as the second argument: `logger.error("msg", error)` — not as a string
- Use structured data (object as second argument) rather than string interpolation: prefer `logger.info("msg", { userId })` over `logger.info(\`msg ${userId}\`)`
