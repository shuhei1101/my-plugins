---
name: ui-kit:debug-fab
description: Embed a floating debug button (FAB) on every development-support screen. Clicking the FAB directly enters element picker mode — select elements, then click the FAB (📋 N) or the top-center Copy button to paste a JSON snapshot into Claude Code for debugging. Trigger when creating or editing development-only UI screens (admin panels, internal tools, debug pages) — not production user-facing screens. Examples: "管理画面作って", "内部ツール用 UI を追加", "開発用デバッグ画面を直して".
---

# ui-kit:debug-fab — Floating Debug Button

Adds a shared floating debug widget (FAB + top copy bar) to every development-support screen.
Click the FAB to enter element picker mode. Select elements on the page, then copy a JSON
snapshot (selected elements + related files + recent error logs) directly to the clipboard.

This skill ships a **shared module** (`templates/uidev.css` + `templates/uidev.js`) — each screen
imports it once and declares only the screen-specific related files. Never copy the widget code
into individual screens.

---

## Tasks

### Step 1: Load related references

Read for context:

```
{plugin_root}/references/principles.md   # UI principles (DRY, CSS, JS, frontend-design)
```

Plus the logging skill's conventions:

```
{plugin_root}/skills/logging/SKILL.md    # logging conventions
```

The plugin root is two levels above this skill file.

→ Proceed to Step 2

---

### Step 2: Confirm this is a development screen

#### Process

Confirm with the user that the screen being worked on is a **development-support** screen
(admin panel / internal tool / debug page) — not a production user-facing screen.

If it is a production screen, **do not apply this skill** and stop.

→ Proceed to Step 3

---

### Step 3: Place the shared widget files in the project

#### Process

1. Copy `{plugin_root}/skills/debug-fab/templates/uidev.css` and `uidev.js` into the project's static
   assets directory (e.g. `static/`, `public/`, `assets/`).
2. If the files already exist in the project, do not overwrite — just confirm the path.
3. Confirm the URLs from which the browser will load them.

→ Proceed to Step 4

#### Notes

- These two files are the **single source of truth** for the widget. All dev screens load them.
- Do not edit the templates inline per screen. If a project needs to customize the widget, branch
  the files in the project (not in this skill).

---

### Step 4: Add the widget loader to the screen

#### Process

1. Add the following to the screen's HTML `<head>`:

   ```html
   <link rel="stylesheet" href="/static/uidev.css" />
   <script src="/static/uidev.js" defer></script>
   ```

2. The widget auto-initializes after DOM ready. No further JS wiring is needed.

→ Proceed to Step 5

---

### Step 5: Declare related files on the screen

#### Process

Pick one of the two registration methods (or both, they merge):

**A. `data-debug-files` attribute (preferred — declarative)**

```html
<body data-debug-files='{
  "html": ["pages/user_list.html"],
  "css":  ["styles/user_list.css"],
  "js":   ["scripts/user_list.js"]
}'>
```

Multiple elements can each declare a subset; entries are merged.

**B. `window.__uidevFiles` global (for dynamic additions)**

```html
<script>
  window.__uidevFiles = {
    html: ["pages/user_list.html"],
    js:   ["scripts/user_list.js"]
  };
</script>
```

→ Proceed to Step 6

#### Notes

##### What to register

- `html`: page templates / partial templates rendering this screen
- `css`:  stylesheets specific to this screen (skip global resets)
- `js`:   scripts specific to this screen (skip framework runtime)

Skip framework / library files. The goal is "files Claude needs to read to debug this screen."
Backend / API targets are intentionally NOT registered here — they can be derived from the JS
files (look for `fetch` / API calls). Likewise for config files, data sources, etc.

---

### Step 6: Apply logging conventions

#### Process

Confirm the project follows `ui-kit:logging` conventions:
- Logger object (not raw `console.log` in handlers)
- JSON Lines output format
- Operation logs at key user interactions and state transitions
- Each log line short (no multi-line object dumps)

If the project does not yet have a logger, run `/ui-kit:logging` first.

→ Done

#### Output

- Shared widget loaded on the screen
- Related files declared
- Logger active and emitting JSON Lines

---

## Operation flow (for the developer)

1. Open the dev screen in the browser
2. Click the 🐛 button (bottom-right, fixed) — element picker mode starts immediately
3. Click elements to select (cyan = hover, green = selected; re-click to deselect)
4. Copy in one of two ways:
   - Click the **📋 N** FAB (bottom-right) → copies JSON and exits picker
   - Click the **📋 コピー** button (top center, always visible) → copies JSON
5. Paste into Claude Code with "これでデバッグして" → Claude reads related files, logs, and selected elements together

`Esc` cancels picker mode without copying.

---

## References

See:

- `{plugin_root}/references/principles.md` — UI principles (mandatory)
- `{plugin_root}/skills/logging/SKILL.md` — logging conventions
- `{plugin_root}/skills/debug-fab/templates/CLAUDE.md` — widget usage details (auto-loaded when working in that folder)
