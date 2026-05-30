<!-- This file is a Japanese mirror of logger-impl.md. When updating the English original, update this file too. -->
# app/(shared)/logger.ts — JSON Lines ロガー実装

サーバー / クライアント両用。**JSON Lines（1 行 = 1 JSON）** 形式で出力。

---

## 実装

```ts
// app/(shared)/logger.ts
'use client'    // クライアント / サーバー両用 OK

type LogLevel = "debug" | "info" | "warn" | "error"
const ORDER: Record<LogLevel, number> = { debug: 10, info: 20, warn: 30, error: 40 }

const currentLevel = (): LogLevel => {
  // production はクライアント側を warn 以上に強制（情報漏洩防止、PR135 QA-055）
  if (typeof window !== "undefined") {
    if (process.env.NODE_ENV === "production") {
      const stored = window.localStorage.getItem("log.level")
      if (stored && stored in ORDER) {
        const lv = stored as LogLevel
        return ORDER[lv] >= ORDER["warn"] ? lv : "warn"
      }
      return "warn"
    }
    const stored = window.localStorage.getItem("log.level")
    if (stored && stored in ORDER) return stored as LogLevel
  }
  const env = (process.env.NEXT_PUBLIC_LOG_LEVEL ??
    (process.env.NODE_ENV === "production" ? "warn" : "info")) as LogLevel
  return env in ORDER ? env : "info"
}

const safeStringify = (obj: unknown): string => {
  try { return JSON.stringify(obj) } catch { return "\"[unserializable]\"" }
}

type LogContext = Record<string, unknown>

const emit = (level: LogLevel, component: string | undefined, msg: string, ctx?: LogContext) => {
  if (ORDER[level] < ORDER[currentLevel()]) return
  const record: Record<string, unknown> = {
    ts: new Date().toISOString(),
    level,
    msg,
  }
  if (component) record.component = component
  if (ctx) record.ctx = ctx
  // eslint-disable-next-line no-console
  console[level](safeStringify(record))
}

const make = (component?: string) => ({
  debug: (msg: string, ctx?: LogContext) => emit("debug", component, msg, ctx),
  info:  (msg: string, ctx?: LogContext) => emit("info",  component, msg, ctx),
  warn:  (msg: string, ctx?: LogContext) => emit("warn",  component, msg, ctx),
  error: (msg: string, ctx?: LogContext) => emit("error", component, msg, ctx),
})

/** デフォルトロガー */
export const logger = {
  ...make(),
  /** コンポーネント tag 付きロガー */
  create: (component: string) => make(component),
}
```

---

## 使い方

### デフォルトロガー

```ts
import { logger } from "@/app/(shared)/logger"

logger.info("家族登録処理を開始", { userId })
logger.debug("リクエスト受信", { path: request.nextUrl.pathname })
logger.warn("リトライします", { attempt, maxRetries })
logger.error("家族登録中にエラー", { error: e.message, userId })
```

### コンポーネント bound

```ts
const log = logger.create("api:resources.POST")

log.info("request received", { path })
log.debug("auth resolved", { userId })
log.error("update failed", { error: e.message, userId })
```

---

## 出力例

```json
{"ts":"2026-05-28T12:34:56.789Z","level":"info","component":"api:resources.POST","msg":"request received","ctx":{"path":"/api/v1/resources"}}
```

---

## ログレベル設定

```bash
# .env.local（dev）
NEXT_PUBLIC_LOG_LEVEL=debug

# Vercel（prod）— warn 未満を入れても強制で warn 以上にクランプ
NEXT_PUBLIC_LOG_LEVEL=warn
```

dev は `localStorage.setItem("log.level", "debug")` で動的変更可。
prod は warn 未満を受け付けない（**情報漏洩防止**、PR135 QA-055）。

---

## エラーログのフォーマット

```ts
try { ... }
catch (e) {
  log.error("update failed", {
    error: e instanceof Error ? e.message : String(e),
    code: e instanceof AppError ? e.code : undefined,
    stack: e instanceof Error ? e.stack : undefined,    // 500 系のみ
    userId,
    resourceId: id,
  })
  throw e
}
```

`Error` オブジェクトを直接 `ctx` に入れない（シリアライズ崩れ）→ `e.message` を取り出す。

---

## センシティブ情報

絶対に含めない:
- パスワード、トークン、API key
- セッション ID
- フルメールアドレス（マスク or hash）
- クレジットカード番号
- PII（個人を特定できる詳細情報）

---

## ルール

- 出力は **JSON Lines**（1 行 = 1 JSON、装飾なし）
- `logger` / `logger.create("...")` を使う（`console.log` 禁止）
- エラーは `{ error: error.message }` を ctx に
- 秘密情報を絶対に出さない
- production はクライアント側 **warn 以上に強制**（PR135）
- `ctx` で構造化、文字列補間しない
- Component tag は `{layer}:{name}` 形式

## 関連 references

- `shared/logger-tags.md` — Component tag 一覧
- `shared/security.md` — センシティブ情報

## 禁止

- `console.log` / `console.error` を直接使う
- `e` を ctx にそのまま入れる（`e.message` を取り出す）
- パスワード / トークンを log に出す
- 文字列補間（`logger.info(\`登録 ${id}\`)` ではなく `logger.info("登録", { id })`）
