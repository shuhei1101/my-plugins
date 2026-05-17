# UI Design — ui-kit Shared Reference

UI / UX patterns and conventions for development-support screens.
Read alongside `principles.md`. Used by `mock`, `implement`, and `debug-fab` skills.

---

## Navigation & Layout

### Mandatory: URL query strings for all screen switching

Every interaction that switches what the user sees — tabs, sidebar items, list↔detail,
pagination, filters, sort — **must** update the URL via query string. The URL is the single
source of truth for "where I am". See `principles.md` Section 1 ("Reflect screen state in the URL")
for the centralized `url-state.js` helper.

Examples: `?tab=settings`, `?nav=tools`, `?view=detail&id=42`, `?page=3&filter=active`.

This makes a pasted URL fully describe the user's context to Claude when they ask for help.

### Primary structures

| Structure | When to use |
|---|---|
| **Sidebar + main**           | Default for tool-like screens (top page, settings, list/detail) |
| **2-pane (list + detail)**   | Browsing a list and seeing details simultaneously (PC). On mobile, falls back to list-then-detail navigation |
| **3-pane (nav + list + detail)** | Heavy multi-resource browsing (rare in dev tools, e.g. inbox-style) |
| **Top tabs**                 | Switching between siblings under the same parent (e.g. user "Profile / Settings / Activity") |

Avoid bare top-only navigation without a sidebar in a tool app — sidebars discoverable everything.

### Header

- Fixed at top, full width
- Left: app / page title
- Right: user menu / global actions (search, notifications)
- **Do not** put "Home" link in the header title. "Home" lives in the sidebar (see Sidebar)
- Height: 56–64px (PC), 48–56px (mobile)

### Sidebar (PC)

- Fixed left, full height
- Always visible on PC (≥ 1024px); collapse to drawer on mobile
- Items to include:
  - **Home** (first item, dashboard / top page)
  - **Section headers** for grouping (e.g. "Tools", "Settings", "Admin")
  - **Recent / favorites** (optional, for frequently used items)
  - **Account / sign-out** at the bottom
- Active item: visually distinct (background, left bar accent)
- Width: 240–280px

### Drawer (Mobile)

- Slide-in from left, overlay with backdrop
- Open via "hamburger" icon in header (top-left)
- Closes on backdrop tap or item selection
- Same items as PC sidebar

### Action buttons (Save / Delete / etc.)

- **Primary action** position is fixed per screen type:
  - **Form screens (settings, edit)**: bottom-right, sticky footer with the action bar
  - **List screens**: top-right of the list (or floating button on mobile)
  - **Detail screens**: top-right of the detail pane
- **Destructive actions** (Delete): always confirm via modal; visually red but secondary in placement
- Never place primary actions in the header (reserved for navigation)

---

## Responsive

### Breakpoints

| Width      | Tier     |
|---|---|
| < 640px    | Mobile   |
| 640–1024px | Tablet   |
| ≥ 1024px   | PC       |

Define as CSS Custom Properties or media query aliases in Foundation.

### Tier-specific behavior

| Pattern              | PC                          | Mobile |
|---|---|---|
| Sidebar              | Always visible (fixed)      | Drawer (hamburger) |
| 2-pane list + detail | Side-by-side                | Single column; list → detail navigation |
| 3-pane               | Three columns               | Single column; tabs or back-nav |
| Top tabs             | Horizontal row              | Horizontal scroll if overflow |
| Action button bar    | Sticky footer or top-right  | Fixed bottom (full-width) |
| Touch targets        | Min 32px                    | Min **44px** (Apple HIG) |

---

## Screen Types

### Top screen

- Sidebar lists categories (e.g. "Tools", "Reports")
- Click a category → main area shows a **card grid** of items in that category
- Each card: icon + name + short description
- Click a card → navigate to that item's dedicated screen

### Settings screen

- Sections grouped by topic (e.g. "Account", "Notifications", "Advanced")
- Each section has a heading + a stack of form rows
- Action bar at bottom (Save / Cancel / Reset)
- Validation errors: inline next to the field (see Forms below)
- For destructive settings: separate "Danger zone" section at the bottom with red accent

### List + Detail screen (2-pane on PC)

- Left pane (PC width ~ 280–360px): list of items
  - Per-item: title + 1-2 lines of metadata
  - Selected item: highlighted
- Right pane: detail of selected item
- Mobile: shows the list; tapping an item navigates to the detail; back button returns
- Toolbar above the list: search, filter, sort, "New" button

---

## Forms

### Field anatomy

- Label above the input (always visible — never use placeholder-only labels)
- Helper text below the input (small, dim)
- Validation error: replaces helper text, in danger color, with a small icon

### Validation patterns

- **Inline error** (preferred): show immediately under the field as the user blurs or submits
- **Summary error**: top of the form for multi-field submission failures (rare; complement inline, don't replace)

### Confirmation dialogs

Required for **irreversible actions**: delete, leave unsaved changes, sign out, etc.
- Title: clear action verb ("Delete user account?")
- Body: explain consequence + how to undo (or that it's irreversible)
- Primary button: the destructive verb in danger color
- Secondary button: "Cancel" (default focus)
- Esc key closes; backdrop click closes

### Keyboard shortcuts

| Action | Shortcut |
|---|---|
| Submit form | `Cmd/Ctrl + Enter` |
| Save | `Cmd/Ctrl + S` (catch the browser default) |
| Close modal / drawer | `Esc` |
| Focus search | `/` (when not in input) |
| Help | `?` |

Document any custom shortcuts in a Help modal accessible via `?`.

---

## State & Feedback

### Loading states

- **Skeleton screens** for predictable layouts (list rows, card grids)
- **Spinners** for indeterminate operations under 3s
- For long operations (> 3s): progress bar + cancel button if possible
- Disable submit buttons + show inline spinner during form submit

### Empty states

- Icon + heading + short helper text + primary action
- Example: "No users yet" / "Add your first user" / [+ Add user] button

### Error states

- Page-level errors: full-page card with icon, description, and retry button
- Component-level errors: inline card replacing the failed component
- Network errors: toast notification (auto-dismiss after ~5s)

### Toast notifications

- Position: bottom-right (PC), top-center (mobile)
- Auto-dismiss: 4–6s for success/info, **manual dismiss** for errors
- Max visible: 3 stacked, oldest pushed out
- Severity colors: success (green), info (blue), warning (amber), error (red)

---

## Accessibility

- Color contrast: WCAG AA minimum (`4.5:1` text, `3:1` UI components)
- All interactive elements reachable by Tab; focus ring visible
- Skip-to-content link as the first focusable element
- ARIA roles for landmarks (`role="navigation"`, `role="main"`, etc.)
- Modal: focus trap; return focus to opener on close
- Form fields: `<label for>` or wrapped; `aria-describedby` for helper text

---

## Dark Mode

- Toggle in the sidebar (bottom area) or user menu
- Persist preference in `localStorage["theme"]` ("light" / "dark" / "auto")
- Default: `auto` (follow system via `prefers-color-scheme`)
- Implement via `:root[data-theme="dark"] { --color-bg: ...; ... }` overrides on Design Tokens

---

## Motion

### Principles

- Motion is purposeful, never decorative
- Duration: 150–250ms for most micro-interactions
- Easing: `cubic-bezier(0.4, 0.0, 0.2, 1)` (Material standard) or `ease-out` for entrances
- Reduced motion: respect `@media (prefers-reduced-motion: reduce)` — disable non-essential animations

### Common transitions

| Element | Transition |
|---|---|
| Drawer / sidebar | Slide-in 200ms ease-out |
| Modal | Fade + scale (0.96 → 1) 180ms |
| Toast | Slide-up + fade 200ms |
| Hover state | 120ms ease-out background/color |
| Page transition | None (instant) — animation here is usually friction, not delight |

Avoid bouncy springs, looping animations, or "wow factor" effects in tool screens — keep it calm.

---

## Implement every pattern as a shared component

**Mandatory**: all patterns described in this document must be implemented as **shared
components**, never duplicated per screen. Anything that appears (or is likely to appear) on
two or more screens goes here.

### Components to share by default

| Group | Items |
|---|---|
| Navigation     | **Header**, **Sidebar**, **Drawer** (mobile), Top tab bar |
| Buttons        | **Buttons** (primary / secondary / ghost / danger variants), Icon button, **FAB** (Floating Action Button) |
| Overlays       | **Modal**, **Confirmation dialog**, **Toast** notifications, Keyboard-shortcut help modal |
| Form           | **Form field** (label + input + helper + error), Form group, Inline error, Form summary |
| State          | **Loading skeleton**, Spinner, Progress bar, **Empty state card**, **Error card** |
| Surfaces       | **Card**, Card grid, Action bar, Section heading |
| Misc           | Theme toggle, Motion-aware wrapper, Icon |

This is the **default list**. If a piece is likely to be reused, add it here even if only one
screen uses it today. "よく使うものはここに入れる" — when in doubt, add it to the shared layer.

### Placement

- All of the above live in the project's `c-*` (Component) layer
- Composites built specifically for one screen (e.g. `p-userList`, `p-settingsAccount`) live in
  the `p-*` (Project) layer and **import the `c-*` components** above instead of reimplementing them

### Workflow

When implementing or mocking a screen, the **first step is always to look up the existing
shared components** (`c-*`, `p-*`) before writing new markup. See the `ui-kit:implement`
skill and the `.claude/rules/common-component-first.md` rule for the enforced workflow.

---

## Mock generation hand-off

When generating mocks via `ui-kit:mock`, apply the patterns in this document.
Each mock variant ("案 A/B/C/...") should explore a meaningful axis of difference
(e.g. sidebar layout vs top-tab layout, dense vs spacious card grid), not just color changes.
