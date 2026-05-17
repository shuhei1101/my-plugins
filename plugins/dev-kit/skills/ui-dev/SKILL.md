---
name: dev-kit:ui-dev
description: >
  UI conventions for development-support screens (admin panels, internal tools, debug pages).
  Every dev screen must include a floating debug button that opens a modal showing related files
  and recent JS logs, and a "Copy" button that exports them as JSON for pasting into Claude Code.
  Trigger when creating or editing development-only UI screens (not for end-user production screens).
  Examples: "管理画面作って", "内部ツール用 UI を追加", "開発用デバッグ画面を直して".
---

# dev-kit:ui-dev — Development Screen UI Conventions

Adds a shared floating debug widget to every development-support screen. The widget collects
related files and recent JS logs and exposes a one-click "Copy as JSON" so the developer can
paste the snapshot into Claude Code for debugging assistance.

This skill ships a **shared module** (`templates/uidev.css` + `templates/uidev.js`) — each screen
imports it once and declares only the screen-specific related files. Never copy the widget code
into individual screens.

---

## Tasks

### Step 1: Load related references

Read for context:

```
{plugin_root}/references/common.md      # logging conventions (mandatory)
{plugin_root}/references/frontend.md    # frontend overview (reference)
{plugin_root}/references/html.md        # HTML conventions (reference)
{plugin_root}/references/css.md         # CSS conventions (reference)
{plugin_root}/references/js.md          # JS conventions (reference)
```

The plugin root is two levels above this skill file. Focus on the **logging** section in `common.md`:
JSON Lines format, logger required, operation logs encouraged, one-line entries short.

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

1. Copy `{plugin_root}/skills/ui-dev/templates/uidev.css` and `uidev.js` into the project's static
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
  "html":    ["pages/user_list.html"],
  "css":     ["styles/user_list.css"],
  "js":      ["scripts/user_list.js"],
  "backend": ["api/users.py"]
}'>
```

Multiple elements can each declare a subset; entries are merged.

**B. `window.__uidevFiles` global (for dynamic additions)**

```html
<script>
  window.__uidevFiles = {
    html:    ["pages/user_list.html"],
    backend: ["api/users.py"]
  };
</script>
```

→ Proceed to Step 6

#### Notes

##### What to register

- `html`:    page templates / partial templates rendering this screen
- `css`:     stylesheets specific to this screen (skip global resets)
- `js`:      scripts specific to this screen (skip framework runtime)
- `backend`: API handlers / route functions called by this screen
- `other`:   anything else relevant (config files, data sources)

Skip framework/library files. The goal is "files Claude needs to read to debug this screen."

---

### Step 6: Apply logging conventions

#### Process

1. Confirm the project uses a logger (not raw `console.log`) per `references/common.md`.
2. If absent, introduce one. Output format must be JSON Lines.
3. Add operation logs at key user interactions and state transitions.
4. Keep each log line short — never dump large objects across multiple lines.

→ Done

#### Output

- Shared widget loaded on the screen
- Related files declared
- Logger active and emitting JSON Lines

---

## Operation flow (for the developer)

1. Open the dev screen in the browser
2. Click the 🐛 button (bottom-right by default, or Ctrl+Shift+D)
3. Adjust log level / line count if needed (default: error and above, 100 lines)
4. Click 📋 Copy — JSON payload is now on the clipboard
5. Paste into Claude Code with "これでデバッグして" → Claude reads related files and logs together

---

## References

See:

- `{plugin_root}/references/common.md` — logging conventions (mandatory section)
- `{plugin_root}/references/frontend.md` — frontend overview
- `{plugin_root}/references/html.md` / `css.md` / `js.md` — language references
- `{plugin_root}/skills/ui-dev/templates/CLAUDE.md` — widget usage details (auto-loaded when working in that folder)
