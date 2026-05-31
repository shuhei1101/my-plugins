---
name: dev-kit:html-mock
description: >
  Generate a multi-variant mock for a single screen type as a single HTML file.
  Variants ("案 A / B / C / ...") are switched via tabs at the top of the page; the mock body
  renders below the tabs. Each variant should explore a meaningful design axis (layout, density,
  navigation pattern) — not just color changes.
  Trigger when the user asks for a UI mock, design proposals, or wants to compare layout options
  before committing to one. Examples: "設定画面のモック作って", "トップ画面の案出して", "一覧詳細のモック数パターン欲しい".
---

# dev-kit:html-mock — Multi-Variant Mock Generator

Produces a single HTML file that shows several design variants of one screen, switchable via
top tabs. Each variant follows `principles.md` (FLOCSS + Design Tokens, JS rules) and
`ui-design.md` (UX patterns by screen type). Output goes to `tmp/mocks/` in the project.

---

## Tasks

### Step 1: Load references AND inventory shared resources

#### Process

1. Read in full:

   ```
   {plugin_root}/references/html/基本方針.md   # FLOCSS, design tokens, JS rules
   {plugin_root}/references/html/UIデザイン.md    # UX patterns by screen type
   ```

2. **Inventory shared resources in the project** (mandatory — applies to mocks too, so
   variants reuse existing components instead of inventing parallel ones):
   - `static/js/constants.js` (or equivalent) — design tokens
   - `static/js/routes.js` (or equivalent) — route names / URL patterns
   - The component layer of CSS — every `c-*` definition
   - The component layer of JS — every shared component module

   If these don't exist in the project yet, note their absence — the mock should still hint at
   what would belong there.

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
| **List + Detail**     | PC: 2-pane |

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

**Determine output location by project type:**

| Project type | Output location | Reason |
|---|---|---|
| FastAPI / Flask / Django or any web server | Directory served by the running server (see below) | Mock is accessible via the live server immediately |
| No server / static project | `tmp/mocks/` | Served by a local HTTP server |

**For FastAPI and similar server projects:**

1. Check whether a mock/dev listing page already exists (e.g. `/dev/mocks`, `/debug/mocks`)
2. If it exists, place the HTML in the template directory that route reads (e.g. `templates/mocks/`, `app/templates/dev/`)
3. If it does not exist, create a new dev mock route and decide on a template directory, then place the HTML there
4. Add an entry for the mock listing to the routing config (e.g. `router.py`, `urls.py`)

File name: `{screen-type}-{YYYYMMDD}.html` (e.g. `settings-20260518.html`).

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

→ Proceed to Step 6

---

### Step 6: Start a server and give the user a URL

#### Process

**For FastAPI and similar server projects:**

1. Check whether the server is already running (e.g. `ps aux | grep uvicorn`)
2. If already running, use that port
3. If not running, find a free port and start the server:
   ```bash
   # Find a free port
   python -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()"
   # Start the server (example: FastAPI)
   uvicorn app.main:app --port {free_port} --reload &
   ```
4. Tell the user the mock listing URL (e.g. `http://localhost:{port}/dev/mocks`)

**For no-server / static projects:**

1. Find a free port and start `python -m http.server`:
   ```bash
   PORT=$(python -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()")
   python -m http.server $PORT --directory tmp/mocks &
   echo "http://localhost:$PORT/{filename}.html"
   ```
2. Tell the user the URL that was started

**Both cases:**

- Always give the user a **URL they can click to open immediately** — never just a file path
- Report each variant's design axis alongside the URL
- When the mock is approved, recommend `/dev-kit:html-implement` for the implementation phase
  (it enforces shared-resource reuse during real implementation)

→ Done

#### Output

- Mock HTML (in the server's template directory for server projects, or `tmp/mocks/` otherwise)
- A browser-ready URL
- All variants follow `principles.md` + `ui-design.md`

---

## References

- `{plugin_root}/references/html/基本方針.md` — FLOCSS, design tokens, JS rules
- `{plugin_root}/references/html/UIデザイン.md` — UX patterns by screen type
- `{plugin_root}/skills/mock/templates/mock-skeleton.html` — starter HTML skeleton
