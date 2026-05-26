# Next.js App Router — Component Design Patterns

## Three-layer component hierarchy

```
page.tsx              → Next.js page (thin wrapper, no logic)
  └── {Feature}Screen.tsx  → Screen component (state wiring + layout)
        └── _components/   → UI sub-components (presentational)
```

### page.tsx

Renders the Screen component only. No hooks, no logic.

```tsx
// app/(app)/families/new/page.tsx
import { FamilyNewScreen } from "./FamilyNewScreen"
export default function Page() {
  return <FamilyNewScreen />
}
```

### Screen component

The main component for each page. Responsible for:
- Calling hooks (data fetching, event handlers)
- Composing sub-components
- Handling conditional rendering (loading, error, empty states)

```tsx
// app/(app)/families/new/FamilyNewScreen.tsx
"use client"
import { ScreenWrapper } from "@/app/(core)/_components/ScreenWrapper"
import { PageHeader } from "@/app/(core)/_components/PageHeader"
import { useFamilyNew } from "./_hooks/useFamilyNew"

export const FamilyNewScreen = () => {
  const { form, onSubmit, isLoading } = useFamilyNew()
  return (
    <ScreenWrapper>
      <PageHeader title="家族を作る" />
      {/* form content */}
    </ScreenWrapper>
  )
}
```

### Sub-components (`_components/`)

Presentational components scoped to a feature. Receive data via props.

---

## Required shared components

These components from `app/(core)/_components/` must be used as described.

### ScreenWrapper — required in every Screen

All Screen components must wrap their content in `ScreenWrapper`.
It applies correct padding and max-width automatically.

```tsx
<ScreenWrapper>
  {/* screen content */}
</ScreenWrapper>
```

### PageHeader

Use for the top-of-page header with title, description, and optional action buttons.

```tsx
<PageHeader
  title="クエスト一覧"
  description="家族のクエストを管理します"
  actions={<button onClick={handleCreate}>新規作成</button>}
/>
```

### LoadingButton

Use for buttons that trigger async operations (API calls, navigation).
Prevents double-submit and shows a spinner during loading.

```tsx
<LoadingButton loading={isLoading} onClick={handleSubmit}>
  保存する
</LoadingButton>
```

### NavigationButton

For link-style navigation buttons with an icon.

```tsx
<NavigationButton href={FAMILY_URL(familyId)} label="家族プロフィール" icon={<IconUser />} />
```

### ScrollableTabs

Horizontally scrollable tabs for features with multiple views.

```tsx
<ScrollableTabs
  tabs={[{ label: "一覧", value: "list" }, { label: "完了", value: "done" }]}
  value={activeTab}
  onChange={setActiveTab}
/>
```

---

## App Shell components (`app/(app)/_components/`)

These components define the overall app layout. Do not modify them when working on a feature.

| Component | Role |
|---|---|
| `AppShellContent.tsx` | Root layout — renders SideMenu (PC) or BottomBar (mobile) |
| `SideMenu.tsx` | PC sidebar navigation |
| `BottomBar.tsx` | Mobile bottom tab bar |

### FAB customization per screen

Use `useFAB()` from `FABContext` to add screen-specific FAB actions:

```tsx
import { useFAB } from "@/app/(core)/_components/FABContext"

const MyScreen = () => {
  const { setFabActions } = useFAB()
  useEffect(() => {
    setFabActions([{ label: "新規作成", icon: <IconPlus />, onClick: handleCreate }])
    return () => setFabActions([])   // clear on unmount
  }, [])
}
```

---

## Constraints

- `ScreenWrapper` is mandatory in every Screen component
- `"use client"` directive is required on Screen components and any component that uses hooks
- Do not use `console.log` — use `logger` from `@/app/(core)/logger`
- Check `app/(core)/_components/` for existing components before building a new one
