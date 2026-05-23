---
name: ui-kit:debug-fab-modify
description: Modify the debug-fab widget UI or behavior (uidev.js / uidev.css). Use when changing FAB behavior, adding/removing buttons, altering picker mode logic, or updating copy payload. Guides through the full change loop: implement → sync docs → bump version → verify example.html. Examples: "FABの動作変えて", "コピーボタン追加して", "ピッカーモードの挙動直して".
---

# ui-kit:debug-fab-modify — Widget Change Workflow

Guides changes to `uidev.js` / `uidev.css` through implementation, doc sync, version bump,
and manual verification in `example.html`.

---

## Architecture overview (read before touching code)

```
templates/
  uidev.js        ← widget logic (picker, copy, DOM)
  uidev.css       ← widget styles (FAB, top bar, picker highlights)
  example.html    ← manual smoke-test page
  CLAUDE.md       ← usage docs (auto-loaded when in this folder)
SKILL.md          ← skill definition (operation flow, references)
```

Key design constraints:
- **FAB is fixed bottom-right** — no position toggle
- **Top copy bar** visible only during picker mode (`body.uidev-picker-active`)
- **`copyAndStop(feedbackBtn)`** is the single shared handler for both FAB and top button; `feedbackBtn` receives the "✓" feedback — `fab` when triggered from FAB, `topCopyBtn` when triggered from the top button
- **On copy failure**, `stop()` is NOT called — picker stays active so the user can retry
- **`refresh()`** updates both FAB label and top button label simultaneously
- Log buffer is always captured but never displayed visually

---

## Tasks

### Step 1: Identify the change type

| Change type | Files to touch |
|---|---|
| Picker behavior (select, toggle, copy) | `uidev.js` → `startPicker()` |
| FAB appearance or click action | `uidev.js` → `init()` + `startPicker()`, `uidev.css` |
| Top bar button (label, visibility, action) | `uidev.js` → `refresh()` / `copyAndStop()`, `uidev.css` |
| Copy payload shape | `uidev.js` → `buildPayload()` |
| New UI element | `uidev.js` → `buildDOM()`, `uidev.css` |

→ Proceed to Step 2

---

### Step 2: Implement the change

#### Key functions in `uidev.js`

| Function | Role |
|---|---|
| `buildDOM()` | Creates FAB + top bar HTML |
| `startPicker(root)` | Enters picker mode; attaches all picker event listeners |
| `refresh()` | Updates FAB label + top button label based on `currentSelected.size` |
| `copyAndStop(feedbackBtn)` | Shared copy handler — copies if selection > 0, shows feedback on `feedbackBtn`; calls `stop()` only on success |
| `onTopCopyClick()` | Named wrapper that calls `copyAndStop(topCopyBtn)` — used so `removeEventListener` works correctly |
| `stop()` | Exits picker mode; removes all listeners, resets FAB and top button |
| `buildPayload(elements)` | Builds JSON with page, files, logs, elements |

#### CSS conventions

- FAB styles: `.uidev-fab`, `.uidev-fab[data-picker-active="true"]`
- Top bar visibility: `.uidev-top-bar { display: none }` / `body.uidev-picker-active .uidev-top-bar { display: block }`
- Picker highlights: `.uidev-picker-highlight` (hover), `.uidev-picker-selected` (selected)

→ Proceed to Step 3

---

### Step 3: Sync documentation

After any behavior or UI change, update **both**:

1. **`SKILL.md`** — Operation flow section (numbered steps, what each button does)
2. **`templates/CLAUDE.md`** — Operations table (Action → Result rows)

Checklist:
- [ ] Does the operation flow in `SKILL.md` match the new behavior?
- [ ] Does the Operations table in `CLAUDE.md` accurately describe each button?

→ Proceed to Step 4

---

### Step 4: Bump version

Update both files:

```
plugins/ui-kit/.claude-plugin/plugin.json  →  "version": "x.y.z"
.claude-plugin/marketplace.json            →  "version": "x.y.z"  (ui-kit entry)
```

| Change | Bump |
|---|---|
| Bug fix | PATCH |
| New UI element or behavior change | MINOR |
| Complete redesign | MAJOR |

→ Proceed to Step 5

---

### Step 5: Verify in example.html

Open `templates/example.html` in a browser and confirm:

- [ ] FAB (🐛) click → picker mode starts
- [ ] Top bar appears; shows "要素を選択してください"
- [ ] Click element → selected (green outline); top button → "📋 コピー (N件)"
- [ ] FAB click (0 selected) → picker exits (cancel)
- [ ] FAB click (N selected) → copies JSON + FAB shows "✓ コピーしました" + exits picker
- [ ] Top button click (N selected) → copies JSON + button shows "✓ コピーしました" + exits picker
- [ ] Top button click (0 selected) → exits picker (cancel)
- [ ] `Esc` → picker exits without copying

If `example.html` no longer demonstrates the changes accurately, update it.

→ Done

---

## References

- `{plugin_root}/skills/debug-fab/templates/CLAUDE.md` — widget usage and JSON schema
- `{plugin_root}/skills/debug-fab/SKILL.md` — integration skill (how to embed on a screen)
- `.claude/rules/debug-fab-template-sync.md` — file sync checklist (auto-loaded)
