# Next.js App Router — State Management

## State type overview

| State type | Tool | Where |
|---|---|---|
| Server data (fetched from API) | TanStack Query (`useQuery`, `useMutation`) | `_hooks/` |
| Global UI state (cross-component) | React Context | `app/(core)/_components/` |
| Local UI state (single component) | `useState` | Inside the component or hook |
| Form state | `useState` + Zod validation | `_hooks/` |

---

## Server data — TanStack Query

TanStack Query (`@tanstack/react-query`) manages all server-side data.

### Provider setup

The `QueryClientProvider` is set up in `app/(core)/_components/providers.tsx`.
Do not create a new provider instance for individual features.

### Cache invalidation

After a mutation succeeds, invalidate the affected query keys:

```ts
const queryClient = useQueryClient()

onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: ["families"] })
}
```

### staleTime and refetch

- Default: `staleTime: 0, refetchOnMount: "always"` — always re-fetch on mount
- For data that rarely changes, increase `staleTime` (e.g. `1000 * 60 * 5` for 5 minutes)

---

## Global UI state — React Context

Use React Context for UI state that needs to be shared across components at different levels.

### Existing contexts (do not duplicate)

| Context | File | Purpose |
|---|---|---|
| `FABContext` | `app/(core)/_components/FABContext.tsx` | Per-screen FAB customization |
| `LoadingContext` | `app/(core)/_components/LoadingContext.tsx` | Global loading indicator |
| `ThemeContext` | `app/(core)/_theme/themeContext.tsx` | Dark/light theme toggle |

### Creating a new context

Only create a new Context if the state cannot be passed via props or handled by TanStack Query.

```ts
// 1. Create context with default value
const MyContext = createContext<MyContextType | null>(null)

// 2. Provider component
export const MyProvider = ({ children }) => {
  const [state, setState] = useState(initialState)
  return <MyContext.Provider value={{ state, setState }}>{children}</MyContext.Provider>
}

// 3. Custom hook to consume it
export const useMyContext = () => {
  const ctx = useContext(MyContext)
  if (!ctx) throw new Error("useMyContext must be used within MyProvider")
  return ctx
}
```

---

## Local UI state — useState

For state that only affects a single component or a small component subtree,
use `useState` directly inside the component or a local hook.

```ts
const [isOpen, setIsOpen] = useState(false)
const [activeTab, setActiveTab] = useState<"list" | "done">("list")
```

---

## Constraints

- Do not use Zustand, Redux, or other state management libraries — use TanStack Query + Context
- Never store server data in `useState` — use TanStack Query
- Never call `queryClient.setQueryData()` to write optimistic updates unless explicitly discussed
- Avoid prop drilling more than 2 levels — use Context or lift to a hook instead
