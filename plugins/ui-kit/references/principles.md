# UI Principles — ui-kit Shared Reference

Conventions for **development-support UI** screens (admin panels, internal tools, debug pages).
Every skill in `ui-kit` references this document. Read in full when writing any UI code in scope.

---

## 1. Centralization (DRY)

The single biggest rule: **never duplicate the same concept in two places**.

- Design values (colors, spacing, typography) → CSS Custom Properties in the Foundation layer
- DOM selectors → constants in a shared module, never raw strings scattered across handlers
- Network endpoints → an `api/` layer, never `fetch('...')` inside UI code
- Repeated DOM structure → a small component, not copy-pasted markup

When the same string or pattern appears 3+ times, extract it. Audit duplication via the
companion rules under `.claude/rules/` (which load whenever you touch related files).

---

## 2. CSS Architecture — FLOCSS + Design Tokens

### Layer model

| Layer | Prefix | Purpose |
|---|---|---|
| Foundation | (none) | Reset + Design Tokens (`:root` custom properties) |
| Layout     | `l-`   | Page-level layout & grid (e.g. `l-grid`, `l-sidebar`) |
| Object — Component | `c-` | Reusable small components (e.g. `c-button`, `c-card`) |
| Object — Project   | `p-` | Project-specific components (e.g. `p-userList`) |
| Object — Utility   | `u-` | Single-purpose utilities (e.g. `u-mt8`, `u-textCenter`) |

Inside a component, use BEM-style naming: `c-button__icon--large`.

### Design tokens

All design values must come from CSS Custom Properties defined in the Foundation layer:

```css
:root {
  /* color */
  --color-bg:        #fff;
  --color-text:      #111;
  --color-primary:   #2e7fff;
  --color-danger:    #ff6b6b;

  /* spacing (8px grid) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 16px;
  --space-4: 24px;

  /* typography */
  --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  --font-mono: ui-monospace, Menlo, Consolas, monospace;

  /* radius / shadow */
  --radius-md: 8px;
  --shadow-md: 0 4px 16px rgba(0,0,0,.12);
}
```

Never hardcode hex colors, pixel values, or font stacks inside `c-*` / `p-*` / `l-*` rules.
Always reference tokens via `var(--token)`.

### Dependency direction

Outer (Utility) → Inner (Foundation). A `c-*` rule can use Foundation tokens but never
reaches into another `c-*` or `p-*` component. Cross-cutting changes go through tokens.

---

## 3. JavaScript Rules

### Mandatory file header

Every JS file starts with:

```js
// @ts-check
```

This enables TypeScript-server-driven type checking in editors without requiring a build step.

### Type annotations via JSDoc

All exported functions, public variables, and complex objects carry JSDoc types:

```js
/**
 * @param {string} userId
 * @param {{ includeDeleted?: boolean }} [opts]
 * @returns {Promise<User>}
 */
export async function fetchUser(userId, opts = {}) { ... }

/** @typedef {{ id: string; name: string; createdAt: string }} User */
```

Use `@typedef` for shared shapes. Use `@template` for generics. Avoid bare `any`.

### Layer separation

| Layer | Responsibility |
|---|---|
| **UI**    | DOM access, event handlers, render. Imports state and api. Never calls `fetch` directly. |
| **State** | In-memory state, derivations. Pure functions where possible. No DOM. |
| **API**   | All network I/O. Wraps `fetch`. Returns typed promises. No DOM access. |

Cross-layer calls flow downward only (UI → State → API). State and API never import UI.

### Function-oriented over class-oriented

Default to plain functions + closures. Reach for classes only when you genuinely need instance
identity (rare in vanilla DOM code). No inheritance chains.

### Inline scripts: minimal

Avoid `<script>` blocks inline in HTML and `onclick="..."` attribute handlers.
Use external `.js` files with `addEventListener`. One small exception: a tiny boot snippet that
loads the main module is acceptable.

### CSS class ↔ JS DOM access linkage

DOM access selectors must match the FLOCSS classes defined in CSS. The companion rule under
`.claude/rules/` loads when you touch matching files and checks the sync.

Prefer querying by FLOCSS class:

```js
const btn = document.querySelector(".c-button");           // ok
const list = document.querySelector(".p-userList__items"); // ok
```

Or expose stable IDs through tokens / constants:

```js
const SELECTORS = {
  userListItems: ".p-userList__items",
  userListEmpty: ".p-userList__empty",
};
```

Avoid magic strings scattered through handlers.

---

## 4. Mandatory: `frontend-design` skill

For **any** UI visual / UX work — components, pages, layout decisions, typography, color, motion —
invoke `frontend-design:frontend-design` skill **without exception**.

The skill enforces:
- A clear conceptual / aesthetic direction (not generic AI defaults)
- Distinctive typography and color choices
- Intentional motion and spatial composition
- Production-grade implementation matched to the aesthetic vision

Do not write UI by ad-hoc taste. Route every visual decision through this skill.
