---
name: ui-kit:flocss-apply
description: >
  Apply FLOCSS + Design Tokens architecture to a screen. Works for both new screens
  (lay out the FLOCSS layers from scratch) and existing screens (classify current
  styles into FLOCSS layers and centralize hardcoded values into design tokens).
  Trigger when starting a new UI screen, when an existing screen needs CSS cleanup,
  or when the user explicitly asks for FLOCSS migration.
  Examples: "FLOCSS で書き直して", "デザイントークンに揃えて", "新しい管理画面のCSS設計して".
---

# ui-kit:flocss-apply — Apply FLOCSS + Design Tokens

Applies the FLOCSS layered architecture combined with Design Tokens (CSS Custom Properties)
to a screen. Works for both **new screens** (build the layers from scratch) and **existing
screens** (re-classify current styles into FLOCSS layers).

---

## Tasks

### Step 1: Load principles

Read:

```
{plugin_root}/references/principles.md   # see Section 2 (CSS Architecture)
```

Key points:
- Layers: Foundation → Layout (`l-`) → Object (`c-` Component / `p-` Project / `u-` Utility)
- Internal naming: BEM (`c-button__icon--large`)
- All design values from `:root` CSS Custom Properties
- Dependency: outer never reaches inward; cross-cutting changes go through tokens

→ Proceed to Step 2

---

### Step 2: Determine mode (new vs existing)

#### Process

| Signal | Mode |
|---|---|
| User says "新しい画面"、"new screen"、no CSS yet | **New** — Step 3 |
| User says "既存"、"書き直して"、CSS already exists | **Existing** — Step 7 |

If ambiguous, ask. Then branch.

---

## New Screen Path (Steps 3–6)

### Step 3: Set up Foundation (tokens)

#### Process

1. Create or extend `static/css/foundation.css` (or the project's CSS location) with:
   - A minimal reset (margin/padding/box-sizing/font basics)
   - Design tokens under `:root`:
     - `--color-*` — color palette
     - `--space-*` — 4px or 8px grid
     - `--font-*` — body / mono stacks, sizes, line-heights
     - `--radius-*`, `--shadow-*`
2. If the project will have dark mode, define `:root[data-theme="dark"] { --color-bg: ...; ... }`.
3. Confirm tokens with the user before continuing.

→ Proceed to Step 4

---

### Step 4: Plan the Layout layer (`l-`)

#### Process

1. Identify page-level layout blocks (header, main, sidebar, footer, grid frames).
2. Create `l-` classes for each: `l-page`, `l-grid`, `l-sidebar`, `l-main`.
3. Layout rules use only token values for spacing.

→ Proceed to Step 5

---

### Step 5: Plan Components (`c-`) and Project parts (`p-`)

#### Process

1. List reusable atoms/molecules — these become `c-*` (e.g. `c-button`, `c-card`, `c-input`).
2. List screen-specific composites that combine `c-*` and add domain logic — `p-*`
   (e.g. `p-userList`, `p-loginForm`).
3. For each, sketch the BEM substructure: `c-button { } c-button__icon { } c-button--primary { }`.
4. Confirm structure with the user before generating CSS.

→ Proceed to Step 6

---

### Step 6: Add Utilities (`u-`) sparingly

#### Process

1. Define a small set of utilities for one-off adjustments: `u-mt8`, `u-textCenter`, `u-hidden`.
2. Each utility is single-purpose. Do not duplicate component styles as utilities.
3. Utilities live in their own file `utility.css` loaded last.

→ Proceed to Step 11 (common final step)

#### Output

- `foundation.css` (reset + tokens) → `layout.css` (`l-*`) → `component.css` (`c-*`) → `project.css` (`p-*`) → `utility.css` (`u-*`)
- Loaded in that order; specificity stays low and predictable

---

## Existing Screen Path (Steps 7–10)

### Step 7: Inventory current styles

#### Process

1. List existing CSS files for this screen.
2. Categorize each rule mentally:
   - reset-like → Foundation
   - layout structure → Layout
   - reusable widget → Component
   - screen-specific composite → Project
   - one-off helper → Utility
3. Identify hardcoded values (colors, paddings, radii) that should become tokens.

→ Proceed to Step 8

---

### Step 8: Introduce/extend Foundation tokens

#### Process

1. If `foundation.css` (or equivalent) does not exist, create it.
2. Move recurring hardcoded values into `:root` tokens.
3. Replace usages with `var(--token)` references.
4. Confirm token names with the user (they become a contract).

→ Proceed to Step 9

---

### Step 9: Rename classes into FLOCSS layers

#### Process

1. Rename layout rules → `l-` prefix (`.layout-grid` → `.l-grid`).
2. Rename reusable widgets → `c-` prefix (`.button` → `.c-button`, sub-elements `.c-button__icon`).
3. Rename screen-specific composites → `p-` prefix (`.user-list` → `.p-userList`).
4. Move one-off helpers → `u-` prefix or fold them into components.
5. Update every consumer — HTML markup, JS `querySelector`, tests.

#### Notes

The `.claude/rules/` rule for CSS-JS linkage will fire and require checking both files. Follow it.

→ Proceed to Step 10

---

### Step 10: Verify & cleanup

#### Process

1. Confirm no hardcoded design values remain inside `c-/p-/l-` rules.
2. Confirm `u-` utilities are single-purpose and not duplicating component styles.
3. Confirm load order: foundation → layout → component → project → utility.
4. Visually verify the screen still renders correctly.

→ Proceed to Step 11

#### Output

- Existing styles reclassified into FLOCSS layers
- Hardcoded values consolidated into design tokens

---

## Common final step

### Step 11: Install the CSS-JS link rule

#### Process

Copy the rule templates into the project. **Both English and Japanese versions** — English
auto-loads, Japanese is a human reference mirror.

| From (plugin) | To (project) |
|---|---|
| `{plugin_root}/templates/rules/css-js-link.md`              | `.claude/rules/css-js-link.md` |
| `{plugin_root}/templates/rules/css-js-link.jp.md`           | `.claude/rules-jp/css-js-link.md` (drop `.jp` suffix) |
| `{plugin_root}/templates/rules/common-component-first.md`   | `.claude/rules/common-component-first.md` |
| `{plugin_root}/templates/rules/common-component-first.jp.md`| `.claude/rules-jp/common-component-first.md` |

Skip any pair whose destination already exists (do not overwrite).
Create the `.claude/rules-jp/` directory if missing.

The rules auto-load whenever Claude reads a `.css`, `.js`, or `.html` file and enforce:
- FLOCSS class definitions are kept in sync with JS / HTML usage
- New UI work reads existing shared components / constants / routes first

→ Done

#### Notes

- This step applies to both new and existing paths
- If the project already has the file, leave it untouched
- If the project's FLOCSS prefix set differs from the default (`c-`/`p-`/`l-`/`u-`), edit the
  rule body to match before committing

---

## References

- `{plugin_root}/references/principles.md` — Section 2 (CSS Architecture), Section 1 (DRY)
- FLOCSS reference (external): <https://github.com/hiloki/flocss>
