# Next.js App Router — Environment Variable Management

## Environment files

| File | Purpose | Git tracked |
|---|---|---|
| `.env` | Shared defaults across all environments | No (`.gitignore`) |
| `.env.local` | Local development overrides | No |
| `.env.sample` | Template showing required variable names (no values) | Yes |
| `.env.test` | Test environment variables | Conditionally |
| `.env.production` | Production environment (Vercel / hosting dashboard) | No |

Files are loaded from the package's root (e.g. `packages/web/`).

---

## NEXT_PUBLIC_ prefix rule

| Variable used in | Prefix | Example |
|---|---|---|
| Client-side code (browser) | `NEXT_PUBLIC_` | `NEXT_PUBLIC_SUPABASE_URL` |
| Server-side only (route.ts, service.ts) | (none) | `SUPABASE_SERVICE_ROLE_KEY` |

**Never add `NEXT_PUBLIC_` to secret keys.** Values with this prefix are embedded in the browser bundle.

```bash
# ✅ Client-safe — readable in browser
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
NEXT_PUBLIC_LOG_LEVEL=debug

# ✅ Server-only — never exposed to browser
SUPABASE_SERVICE_ROLE_KEY=eyJ...
STRIPE_SECRET_KEY=sk_...
```

---

## Accessing env vars in code

```ts
// Client-side (component, hook — both work)
const url = process.env.NEXT_PUBLIC_SUPABASE_URL

// Server-side only (route.ts, service.ts, db.ts)
const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY
```

TypeScript: add variable declarations to `env.d.ts` (or `next-env.d.ts`) so IDE gives autocomplete:

```ts
declare namespace NodeJS {
  interface ProcessEnv {
    NEXT_PUBLIC_SUPABASE_URL: string
    SUPABASE_SERVICE_ROLE_KEY: string
  }
}
```

---

## Adding a new variable

1. Add to `.env.sample` with an empty value and a comment
2. Add to `.env.local` (your actual value — never commit)
3. Add the TypeScript declaration to `env.d.ts`
4. Set the value in the hosting dashboard (Vercel / Supabase) for production

---

## Log level variable

```bash
NEXT_PUBLIC_LOG_LEVEL=debug    # local: show all logs
NEXT_PUBLIC_LOG_LEVEL=warn     # production: warn and error only
```

---

## Constraints

- Never commit `.env`, `.env.local`, or any file with real secret values
- Never add `NEXT_PUBLIC_` prefix to secrets (service role keys, payment keys, etc.)
- Always update `.env.sample` when adding a new variable
