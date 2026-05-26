# Next.js App Router — Folder Structure & Naming Conventions

## Top-level app/ structure

```
app/
├── (app)/          # Authenticated app screens (Route Group — not part of URL)
├── (auth)/         # Authentication screens (login, signup, password reset)
├── (core)/         # Shared components, utilities, and providers
├── api/            # API routes (server-side handlers)
├── error/          # Error pages (unauthorized, etc.)
├── layout.tsx      # Root layout
└── error.tsx       # Global error boundary
```

Route Groups (`(name)/`) organize pages without affecting the URL path.

---

## Authenticated screen folder pattern (`app/(app)/`)

Each feature gets its own subfolder. The structure inside is consistent:

```
app/(app)/{feature}/
├── page.tsx                    # Next.js page — thin wrapper only, no logic
├── {Feature}Screen.tsx         # Screen component — UI and state wiring
├── _components/                # Components scoped to this feature
│   └── {Component}.tsx
├── _hooks/                     # Custom hooks scoped to this feature
│   └── use{Feature}.ts
└── [id]/                       # Dynamic route segment
    ├── page.tsx
    ├── {Feature}Screen.tsx
    ├── _components/
    └── _hooks/
```

### page.tsx role

`page.tsx` is a thin wrapper only. It imports and renders the Screen component.
Do not put data fetching, hooks, or business logic directly in `page.tsx`.

```tsx
// app/(app)/quests/page.tsx
import { QuestListScreen } from "./QuestListScreen"
export default function Page() {
  return <QuestListScreen />
}
```

### Nested sub-routes

Sub-routes follow the same pattern recursively:

```
app/(app)/quests/family/[id]/
├── page.tsx
├── QuestViewScreen.tsx
├── _components/
├── _hooks/
└── view/           # Sub-page (URL: /quests/family/[id]/view)
    ├── page.tsx
    └── _hooks/
```

---

## Shared folder (`app/(core)/`)

Common components, utilities, and providers shared across all screens.

```
app/(core)/
├── _components/        # Shared UI components (ScreenWrapper, PageHeader, etc.)
├── _theme/             # Theme context and configuration
├── _auth/              # Auth helpers and HOCs
├── endpoints.ts        # All URL constants (centralized)
├── logger.ts           # Logger instance
└── errors/             # Error classes and handlers
```

---

## API routes folder (`app/api/`)

Each resource mirrors the URL structure:

```
app/api/{resource}/
├── route.ts        # Next.js API handler (GET, POST, PATCH, DELETE)
├── client.ts       # Client-side fetch functions (called from hooks)
├── service.ts      # Business logic
├── db.ts           # DB queries (Drizzle ORM)
└── query.ts        # Query parameter types and validation

app/api/{resource}/[id]/
├── route.ts
├── client.ts
├── service.ts
├── db.ts
└── query.ts
```

---

## Naming conventions

| Target | Convention | Example |
|---|---|---|
| Folder | kebab-case | `quest-list/`, `family-members/` |
| `_components/`, `_hooks/` | underscore prefix (excluded from routing) | `_components/`, `_hooks/` |
| Screen component file | PascalCase + `Screen` suffix | `QuestListScreen.tsx` |
| Layout component file | PascalCase + `Layout` suffix | `QuestViewLayout.tsx` |
| Sub-component file | PascalCase | `QuestCard.tsx` |
| Hook file | camelCase + `use` prefix | `useQuestList.ts` |
| Utility / config file | camelCase | `endpoints.ts`, `logger.ts` |
| Dynamic segment folder | `[id]` or `[slug]` | `[id]/`, `[childId]/` |

---

## Query string handling

When a route accepts query string parameters (e.g. `/quests?filter=active&page=2`),
define the parameter types in `query.ts` under the same API folder:

```ts
// app/api/quests/family/query.ts
export type FamilyQuestFilterType = {
  tags?: string[]
  name?: string
  categoryId?: string
}
```

On the frontend, pass query parameters as arguments to the custom hook.
Never embed raw `?key=value` strings in URLs — use typed parameters.

---

## Constraints

- `page.tsx` must never contain hooks, data fetching, or conditional logic
- `_components/` and `_hooks/` prefixes must be used — do not place components directly in a route folder without the prefix
- Never create a standalone component file at the route folder root (e.g. `app/(app)/quests/Card.tsx`) — use `_components/`
- The `app/(core)/` folder is the only place for project-wide shared components
