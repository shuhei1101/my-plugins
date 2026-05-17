# debug-fab templates

> Japanese mirror: `CLAUDE.jp.md` (human reference only — not auto-loaded by Claude Code).
> When editing: update the JP mirror first, then apply the same change here.

Shared debug widget templates provided by the `ui-kit:debug-fab` skill.
Source files for the floating debug button + modal that every development-support screen must embed.

---

## Folder Structure

| File | Role |
|---|---|
| `uidev.css` | Styles for the floating button + debug modal |
| `uidev.js`  | Logger hook + modal control + copy handler |
| `example.html` | Minimal embedding example (reference when integrating into a screen) |
| `CLAUDE.md` / `CLAUDE.jp.md` | This usage guide (auto-loaded) |

---

## How to use in a screen

### ① Load CSS / JS once (shared across screens)

```html
<link rel="stylesheet" href="/static/uidev.css" />
<script src="/static/uidev.js" defer></script>
```

From the moment `uidev.js` loads, it captures all `console.log/info/warn/error/debug` calls.
`window.onerror` and `unhandledrejection` are also captured automatically.

### ② Declare related files on the screen

**A. `data-debug-files` attribute (preferred)**

```html
<body data-debug-files='{
  "html": ["pages/user_list.html"],
  "css":  ["styles/user_list.css"],
  "js":   ["scripts/user_list.js"]
}'>
```

Multiple elements can each declare a subset; entries are merged:

```html
<form data-debug-files='{"js":["scripts/auth.js"]}'>...</form>
<table data-debug-files='{"js":["scripts/user_list.js"]}'>...</table>
```

**B. `window.__uidevFiles` global**

```html
<script>
  window.__uidevFiles = {
    html: ["pages/user_list.html"],
    css:  ["styles/user_list.css"],
    js:   ["scripts/user_list.js"]
  };
</script>
```

A and B can coexist (both are merged). Use B for dynamic additions; A is simpler for static.

---

## Operations

| Action | Result |
|---|---|
| Click the 🐛 (default bottom-right, or configured position) | Opens the debug modal |
| Click the "📋 Copy" button in the header | Copies related files + logs as JSON to clipboard |
| Click the "🎯 要素選択" button in the header | Enters element picker mode — see below |
| `Ctrl + Shift + D` | Toggle modal open/close |
| Level / line-count selectors in the modal | Filter display + copy (saved to localStorage) |
| "Button position" selector in the header | Move the floating button (saved to localStorage) |
| "XPath format" selector | Choose short vs full XPath for the element picker (saved to localStorage) |

### Element picker mode

1. Click "🎯 要素選択" in the modal header
2. The modal hides and a hint bar appears: hover an element to highlight it
3. Click the target element → its info is copied to clipboard as JSON
4. `Esc` cancels the mode without copying

Copied JSON shape:

```json
{
  "page": "/path",
  "url":  "https://.../path?tab=...",
  "element": {
    "xpath":   "//*[@id=\"user-list\"]/li[3]/button",
    "mode":    "short",
    "tag":     "BUTTON",
    "id":      null,
    "classes": ["c-button", "c-button--ghost"],
    "text":    "Edit"
  },
  "capturedAt": "ISO8601"
}
```

XPath mode (`short` / `full`) is chosen in the modal's "要素ピッカー設定" section.

---

## Copied JSON schema

```json
{
  "page": "{location.pathname}",
  "url":  "{location.href}",
  "files": {
    "html": [], "css": [], "js": []
  },
  "logs": {
    "limit": 100,
    "level": "error",
    "entries": [
      { "ts": "ISO8601", "level": "log|info|warn|error|debug", "args": ["..."] }
    ]
  },
  "capturedAt": "ISO8601"
}
```

Paste directly into Claude Code with "debug this for me" and Claude will read the related files and logs together.

---

## Constraints

- `uidev.js` initializes only once per page even if loaded multiple times (`window.__uidevLoaded` guard).
- Never load this on production user-facing screens — `debug-fab` is for development-support screens only.
- Log buffer is capped at 2000 entries (oldest discarded).
- Do not modify these templates inline per screen. If a project needs customization, fork the files inside the project (not here).
