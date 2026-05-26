# Next.js App Router — Custom Hook Patterns

## Hook placement rules

| Scope | Location |
|---|---|
| Scoped to one route | `app/(app)/{feature}/_hooks/use{Feature}.ts` |
| Scoped to a sub-route | `app/(app)/{feature}/[id]/{sub}/_hooks/use{Sub}.ts` |
| Shared across multiple features | `app/(core)/_hooks/use{Name}.ts` |

Hooks go in `_hooks/` (plural). Some legacy code uses `_hook/` (singular) — use `_hooks/` for new code.

---

## Data-fetching hook pattern (TanStack Query)

Use `useQuery` for read operations. Always include error handling via `handleAppError`.

```ts
// app/(app)/quests/family/_hooks/useFamilyQuests.ts
"use client"

import { useQuery } from "@tanstack/react-query"
import { useRouter } from "next/navigation"
import { getFamilyQuests } from "@/app/api/quests/family/client"
import { handleAppError } from "@/app/(core)/error/handler/client"

export const useFamilyQuests = ({ filter, sortColumn, sortOrder, page, pageSize }) => {
  const router = useRouter()

  const { error, data, isLoading, refetch } = useQuery({
    queryKey: ["familyQuests", filter, sortColumn, sortOrder, page, pageSize],
    retry: false,
    queryFn: () => getFamilyQuests({ ...filter, sortColumn, sortOrder, page, pageSize }),
    staleTime: 0,
    refetchOnMount: "always",
  })

  if (error) handleAppError(error, router)

  return {
    quests: data?.rows ?? [],
    totalRecords: data?.totalRecords ?? 0,
    isLoading,
    refetch,
  }
}
```

### queryKey conventions

- Array form: `["resourceName", ...filterParams]`
- Include all parameters that affect the result in the key
- Use consistent resource name strings (e.g. `"familyQuests"`, `"children"`)

---

## Mutation hook pattern (TanStack Query)

Use `useMutation` for write operations (POST, PATCH, DELETE).

```ts
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useRouter } from "next/navigation"
import { postFamily } from "@/app/api/families/client"
import { handleAppError } from "@/app/(core)/error/handler/client"

export const useFamilyNew = () => {
  const router = useRouter()
  const queryClient = useQueryClient()

  const { mutate, isPending } = useMutation({
    mutationFn: postFamily,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["families"] })
      router.push(HOME_URL)
    },
    onError: (error) => handleAppError(error, router),
  })

  return { onSubmit: mutate, isLoading: isPending }
}
```

---

## Form state hook pattern

For form state, combine `useState` with a submit handler. Use Zod for validation.

```ts
import { useState } from "react"
import { z } from "zod"
import { useMutation } from "@tanstack/react-query"

const FormSchema = z.object({
  name: z.string().min(1),
  description: z.string().optional(),
})

export const useFeatureForm = () => {
  const [form, setForm] = useState({ name: "", description: "" })
  const [errors, setErrors] = useState<Record<string, string>>({})

  const { mutate, isPending } = useMutation({ mutationFn: postResource })

  const onSubmit = () => {
    const result = FormSchema.safeParse(form)
    if (!result.success) {
      setErrors(result.error.flatten().fieldErrors)
      return
    }
    mutate(result.data)
  }

  return { form, setForm, errors, onSubmit, isLoading: isPending }
}
```

---

## Error handling in hooks

Always pass errors to `handleAppError` with the router instance.
This function redirects to the appropriate error page based on error type.

```ts
import { handleAppError } from "@/app/(core)/error/handler/client"

// In useQuery:
if (error) handleAppError(error, router)

// In useMutation onError:
onError: (error) => handleAppError(error, router)
```

---

## Constraints

- All hooks must have `"use client"` at the top of the file (or the component that uses them must)
- Never fetch data directly in a Screen component — always use a hook
- Use `useRouter()` for navigation inside hooks
- Do not use `console.log` — use `logger` from `@/app/(core)/logger`
