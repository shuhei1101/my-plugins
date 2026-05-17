---
name: ui-kit:mock
description: >
  Generate a multi-variant mock for a single screen type as a single HTML file.
  Variants ("案 A / B / C / ...") are switched via tabs at the top of the page; the mock body
  renders below the tabs. Each variant should explore a meaningful design axis (layout, density,
  navigation pattern) — not just color changes. Mobile-responsive by default.
  Trigger when the user asks for a UI mock, design proposals, or wants to compare layout options
  before committing to one. Examples: "設定画面のモック作って", "トップ画面の案出して", "一覧詳細のモック数パターン欲しい".
---

# ui-kit:mock — Multi-Variant Mock Generator

Produces a single HTML file that shows several design variants of one screen, switchable via
top tabs. Each variant follows `principles.md` (FLOCSS + Design Tokens, JS rules) and
`ui-design.md` (UX patterns by screen type). Output goes to `tmp/mocks/` in the project.

---

## Tasks

### Step 1: Load references

Read in full:

```
{plugin_root}/references/principles.md   # FLOCSS, design tokens, JS rules
{plugin_root}/references/ui-design.md    # UX patterns by screen type
```

The plugin root is two levels above this skill file.

→ Proceed to Step 2

---

### Step 2: Confirm screen type

#### Process

Confirm with the user which **single** screen type the mock should explore:

| Type | Notes |
|---|---|
| **Top screen**        | Sidebar lists categories; main area shows a card grid of items per category |
| **Settings**          | Section-grouped form rows; sticky action bar; danger zone at bottom |
| **List + Detail**     | PC: 2-pane; mobile: list → detail navigation |

One screen type per mock — do not mix multiple types into one HTML file.

→ Proceed to Step 3

---

### Step 3: Determine the design axes for variants

#### Process

1. Pick 3–5 design axes that meaningfully differ across the variants. Examples:
   - Sidebar vs top-tab navigation
   - Dense vs spacious card grid (e.g. 2-col vs 4-col on PC)
   - Detail pane on right vs detail pane in a modal
   - Light theme vs dark-first theme
   - Inline editing vs separate edit screen
2. Each variant = one combination of axes worth comparing
3. **Don't** generate variants that differ only in color or microcopy — Claude flags these and skips them
4. Confirm the axes with the user before generating

→ Proceed to Step 4

---

### Step 4: Apply `frontend-design` skill

#### Process

Per `principles.md` Section 4, invoke `frontend-design:frontend-design` skill to commit to a clear
aesthetic direction for the mock. This sets typography, color palette, motion, and overall vibe.

The aesthetic direction is shared across all variants on the same mock file (so variants can be
compared on layout / pattern differences, not aesthetic).

→ Proceed to Step 5

---

### Step 5: Generate the mock HTML

#### Process

Create `tmp/mocks/{screen-type}-{YYYYMMDD}.html` (e.g. `tmp/mocks/settings-20260518.html`).

The file structure:

```html
<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{Screen Type} — Mock</title>
  <style>
    /* FLOCSS layers inline for self-contained mock:
       Foundation (reset + tokens) → Layout (l-*) → Component (c-*) → Project (p-*) → Utility (u-*) */
  </style>
</head>
<body>

  <!-- ── Tabs at the top ──────────────────────────────────── -->
  <nav class="l-mockTabs" role="tablist">
    <button class="l-mockTabs__tab" data-variant="a" aria-selected="true">案 A — {axis summary}</button>
    <button class="l-mockTabs__tab" data-variant="b" aria-selected="false">案 B — {axis summary}</button>
    <!-- ... more variants ... -->
  </nav>

  <!-- ── Mock body — one section per variant ──────────────── -->
  <main class="l-mockBody">
    <section data-variant="a" class="p-variant"> ... variant A content ... </section>
    <section data-variant="b" class="p-variant" hidden> ... variant B content ... </section>
    <!-- ... -->
  </main>

  <script>
    // @ts-check
    // Tab switching: clicking a tab shows the matching section, hides others
  </script>
</body>
</html>
```

Implementation rules:

- All styling inline in `<style>` (single-file mock — no external CSS)
- All JS inline in `<script>` (with `// @ts-check`)
- FLOCSS layer order preserved
- Design tokens defined in `:root` Foundation
- Each variant section: full screen layout including sidebar / header / main as per the chosen screen type
- Variants switchable via top tabs (one variant visible at a time via `hidden` attribute)
- **Mobile responsive**: use media queries per `ui-design.md` breakpoints (640 / 1024)

→ Proceed to Step 6

---

### Step 6: Verify and present

#### Process

1. Confirm the file exists at `tmp/mocks/...` and opens in a browser
2. Tell the user the path and the variants' axes
3. Suggest opening it for review; iterate based on feedback

→ Done

#### Output

- `tmp/mocks/{screen-type}-{date}.html` with N variants behind top tabs
- All variants follow `principles.md` + `ui-design.md`
- Mobile-responsive

---

## References

- `{plugin_root}/references/principles.md` — FLOCSS, design tokens, JS rules
- `{plugin_root}/references/ui-design.md` — UX patterns by screen type, responsive rules
- `{plugin_root}/skills/mock/templates/mock-skeleton.html` — starter HTML skeleton
