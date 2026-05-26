# Next.js App Router — URL Constant Management

## Rule: centralize all URLs in endpoints.ts

All URL strings are defined as constants in `app/(core)/endpoints.ts`.
Never hardcode URL strings directly in components or hooks.

---

## URL definition patterns

### Static URL

```ts
export const HOME_URL = "/home"
export const FAMILIES_URL = "/families"
export const NOTIFICATIONS_URL = "/notifications"
```

### Dynamic URL (contains an ID)

Define as a function:

```ts
export const FAMILY_URL = (id: string) => `/families/${id}`
export const FAMILY_VIEW_URL = (id: string) => `/families/${id}/view`
export const QUEST_URL = (id: string) => `/quests/family/${id}`
export const CHILD_QUEST_URL = (childId: string, questId: string) =>
  `/children/${childId}/quests/${questId}`
```

### Grouped URLs for a feature with many sub-routes

Use an object when a feature has 3+ related URLs:

```ts
export const SETTINGS_URL = {
  root: "/settings",
  profile: "/settings/profile",
  notifications: "/settings/notifications",
  privacy: "/settings/privacy",
  about: "/settings/about",
}
```

### API endpoint URLs

Backend API routes are also defined here (prefixed with `/api`):

```ts
export const FAMILY_API_URL = "/api/families"
export const FAMILY_DETAIL_API_URL = (id: string) => `/api/families/${id}`
```

---

## Naming conventions

| Pattern | Format | Example |
|---|---|---|
| Static frontend route | `{FEATURE}_URL` | `HOME_URL`, `FAMILIES_URL` |
| Dynamic frontend route | `{FEATURE}_{ACTION}_URL = (id) => ...` | `FAMILY_VIEW_URL`, `QUEST_EDIT_URL` |
| Grouped feature | `{FEATURE}_URL = { root, sub1, sub2 }` | `SETTINGS_URL` |
| API endpoint | `{FEATURE}_API_URL` | `FAMILY_API_URL` |

---

## Usage

```ts
import { FAMILY_URL, HOME_URL, FAMILY_API_URL } from "@/app/(core)/endpoints"

// Navigation
router.push(HOME_URL)
router.push(FAMILY_URL(familyId))

// API fetch
const res = await fetch(FAMILY_API_URL)
const res = await fetch(FAMILY_DETAIL_API_URL(id))
```

---

## Adding a new URL

1. Open `app/(core)/endpoints.ts`
2. Follow the naming convention above
3. For dynamic routes, always use the function form
4. Add the constant — do not hardcode the string anywhere else

---

## Constraints

```ts
// ❌ Never hardcode URL strings
router.push("/families/123/view")
fetch("/api/families")

// ✅ Always use constants
router.push(FAMILY_VIEW_URL(familyId))
fetch(FAMILY_DETAIL_API_URL(familyId))
```
