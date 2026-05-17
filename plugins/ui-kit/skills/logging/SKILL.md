---
name: ui-kit:logging
description: >
  Set up a frontend logging convention — introduce a logger module (not raw console.log),
  emit JSON Lines, define what to log at each level (debug/info/warn/error), and add a
  runtime level switch. Trigger when a frontend project needs structured logs, when adding
  observability to a development-support screen, or when reviewing existing logging code.
  Examples: "ログ整備して", "console.log 散らかってるのを整理", "操作ログを出すようにして".
---

# ui-kit:logging — Frontend Logging Setup

Introduces a small logger module to a frontend project, defines what to log at each level,
and outputs JSON Lines that downstream tools (Claude / log viewers / `jq`) can parse.

Default level set: `debug` / `info` / `warn` / `error`. Critical incidents are logged at
`error` with a clear marker — no separate `critical` level in the frontend (the level set
mirrors common browser console categories).

---

## Tasks

### Step 1: Load principles

Read for context:

```
{plugin_root}/references/principles.md   # see Section 3 (JS Rules) and Section 1 (DRY)
```

The plugin root is two levels above this skill file.

→ Proceed to Step 2

---

### Step 2: Inspect existing logging

#### Process

1. Search the project for `console.log` / `console.info` / `console.warn` / `console.error` usage.
2. Note any existing logger module.
3. Identify entry points (page boot, event handlers, API calls) where logs are emitted or missing.

→ Proceed to Step 3

---

### Step 3: Create the logger module (if absent)

#### Process

Place a small module at e.g. `static/logger.js` (or the project's JS directory). Use the
template below — adjust paths and storage key to fit the project:

```js
// @ts-check
/**
 * Minimal JSON-Lines logger for the browser.
 *
 * Levels: debug < info < warn < error
 * Default level: error in production, debug while developing.
 * Storage key: localStorage["log.level"] — overrides the default.
 *
 * Output: console.<level>(JSON.stringify({ ts, level, msg, ...ctx }))
 */

/** @typedef {"debug"|"info"|"warn"|"error"} LogLevel */

const ORDER = /** @type {const} */ ({ debug: 10, info: 20, warn: 30, error: 40 });

/** @returns {LogLevel} */
function currentLevel() {
  const stored = /** @type {LogLevel | null} */ (
    /** @type {any} */ (localStorage.getItem("log.level"))
  );
  if (stored && stored in ORDER) return stored;
  return "error";
}

/**
 * @param {LogLevel} level
 * @param {string}   msg
 * @param {Record<string, unknown>} [ctx]
 */
function emit(level, msg, ctx) {
  if (ORDER[level] < ORDER[currentLevel()]) return;
  const record = { ts: new Date().toISOString(), level, msg, ...(ctx || {}) };
  // One line per record — never pretty-print on disk
  // eslint-disable-next-line no-console
  console[level](JSON.stringify(record));
}

/** @param {string} msg @param {Record<string, unknown>} [ctx] */
export const debug = (msg, ctx) => emit("debug", msg, ctx);
/** @param {string} msg @param {Record<string, unknown>} [ctx] */
export const info  = (msg, ctx) => emit("info",  msg, ctx);
/** @param {string} msg @param {Record<string, unknown>} [ctx] */
export const warn  = (msg, ctx) => emit("warn",  msg, ctx);
/** @param {string} msg @param {Record<string, unknown>} [ctx] */
export const error = (msg, ctx) => emit("error", msg, ctx);

/** @param {LogLevel} level */
export const setLevel = (level) => localStorage.setItem("log.level", level);
```

→ Proceed to Step 4

---

### Step 4: Apply the level-by-level guide

#### Process

For every place that emits a log, choose the right level based on the table below.
When refactoring existing `console.log` calls, sort each into one of these:

| Level | When to use | Examples |
|---|---|---|
| `debug` | Verbose internal trace, only useful during development. Off by default in production. | Function entry/exit with args, intermediate state, "matched route X", "cache miss for key Y" |
| `info`  | Normal operation, user actions, state transitions. Useful in production to follow what happened. | "user clicked Save", "page rendered: user_list", "form submitted: { fields: 3 }" |
| `warn`  | Recoverable anomaly. Something unusual but handled (retry, fallback, deprecated path). | "API retry attempt 2/3", "missing optional field — using default", "deprecated route called" |
| `error` | Unrecoverable failure, including critical incidents. Requires attention. | "API 500", "uncaught render exception", "data corruption detected — refused to save" |

Notes:
- No separate `critical` level — frontend tools (browser console, log aggregators) commonly
  collapse the high end of the spectrum. Use `error` and mark severity in the message:
  `error("PAYMENT_GATEWAY_DOWN", { incident: "critical" })`.
- Be generous with `info` for user actions and state transitions — these are the trail
  you'll follow when debugging.
- Keep each call to one line of payload — never spread huge objects.

→ Proceed to Step 5

---

### Step 5: Wire global error capture

#### Process

In the page bootstrap, capture uncaught errors and unhandled promise rejections:

```js
// @ts-check
import { error } from "./logger.js";

window.addEventListener("error", (e) => {
  error("uncaught_error", {
    message: e.message,
    file: e.filename,
    line: e.lineno,
    col: e.colno,
  });
});

window.addEventListener("unhandledrejection", (e) => {
  error("unhandled_rejection", { reason: String(e.reason) });
});
```

→ Proceed to Step 6

---

### Step 6: Replace raw console calls

#### Process

1. Replace every `console.log(...)` in non-test code with `logger.info(...)` (or another level per the guide).
2. Allow temporary `console.debug` for ad-hoc work but remove before commit.
3. The `debug-fab` widget collects all `console.<level>` calls anyway — so even after switching to the
   logger, the FAB panel will still surface the entries.

→ Done

#### Output

- Logger module installed, level switch available via `localStorage["log.level"]` (or `setLevel(...)`)
- All call sites converted to use the logger
- Global error capture wired
- Each line is a single JSON record on its own line (JSON Lines)

---

## References

- `{plugin_root}/references/principles.md` — Section 3 (JS Rules) and Section 1 (Centralization)
- `{plugin_root}/skills/debug-fab/SKILL.md` — debug widget that surfaces these logs in-screen
