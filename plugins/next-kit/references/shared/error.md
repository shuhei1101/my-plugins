# Next.js App Router — Error Handling

## Error class hierarchy

```
AppError (base)
├── ClientValueError   — form validation / input error
└── ClientAuthError    — authentication / authorization error
```

All error classes are defined in `app/(core)/errors/`.

### AppError

```ts
class AppError extends Error {
  statusCode: number
  code: string

  // Create from a failed fetch response
  static fromResponse(data: unknown, statusCode: number): AppError
}
```

### ClientValueError

Use for form validation failures. Carries the field name that caused the error.

```ts
class ClientValueError extends AppError {
  field?: string  // name of the invalid field
}
```

### ClientAuthError

Use for unauthenticated or unauthorized access.

```ts
class ClientAuthError extends AppError {}
```

---

## Server-side error handling — route.ts

Wrap every API handler with `withRouteErrorHandling`.
It catches all errors and converts them to a structured JSON response automatically.

```ts
import { withRouteErrorHandling } from "@/app/(core)/error/handler/server"

export async function POST(request: NextRequest) {
  return withRouteErrorHandling(async () => {
    // All errors thrown here are caught and formatted automatically
    const data = await doSomething()
    return NextResponse.json(data)
  })
}
```

Never add a try/catch inside a `withRouteErrorHandling` block for the happy path — let errors propagate.

---

## Client-side error handling — hooks

Use `handleAppError` to process errors from fetch calls. It reads the error type and redirects to the appropriate error page.

```ts
import { handleAppError } from "@/app/(core)/error/handler/client"

// In useQuery:
const { error, data } = useQuery({ ... })
if (error) handleAppError(error, router)

// In useMutation:
useMutation({
  onError: (error) => handleAppError(error, router),
})
```

---

## Error pages

| Page | Route | Trigger |
|---|---|---|
| Global error boundary | `app/error.tsx` | Unhandled render errors |
| Unauthorized | `app/error/unauthorized/page.tsx` | `ClientAuthError` (401 / 403) |

---

## Throwing errors in service.ts

Throw `AppError` (or a subclass) for expected failure conditions:

```ts
import { AppError } from "@/app/(core)/error/appError"

if (!family) {
  throw new AppError("Family not found", 404, "FAMILY_NOT_FOUND")
}

if (!hasPermission) {
  throw new ClientAuthError("Forbidden", 403, "FORBIDDEN")
}
```

---

## Constraints

- All `route.ts` handlers must use `withRouteErrorHandling` — no bare try/catch
- All hook-level errors must go through `handleAppError(error, router)` — do not show raw error messages
- Never expose internal error details (stack traces, DB queries) in API responses
- Use `ClientValueError` for form validation — never throw a generic `Error` for user-facing validation
