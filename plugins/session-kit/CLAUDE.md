# session-kit Plugin Developer Guide

session-kit manages the lifetime of the **injection tokens** that other plugins
(py-kit / next-kit) drop in `/tmp`. It deletes the current session's tokens on
every user prompt (so references re-inject each conversation turn) and
garbage-collects stale tokens on session start.

It has **no marker file** and consumers do not depend on it: they just create and
check their own tokens; session-kit deletes those tokens externally.

---

## What it does

| Hook | Action |
|---|---|
| `UserPromptSubmit` | Delete the **current session's** injection tokens (`*-references-injection-{session_id}-*`) |
| `SessionStart` | **TTL cleanup**: delete injection tokens older than 1 day |

It does **nothing else** — no prompt injection, no blocking, no output.

### Why delete tokens on UserPromptSubmit (per-turn cache)

An injection token means "this rule's references were already injected." Keeping
it for the whole **session** is too long: in a long conversation the injected
guidance ends up buried far above and Claude may forget it. Deleting the session's
tokens on every `UserPromptSubmit` makes the cache **per conversation turn** — the
references re-inject the next time Claude touches a matching file in a new turn,
while still de-duplicating repeated touches *within* a single turn.

`/compact` and `/clear` need no special handling: after `/compact` the next user
prompt clears the tokens (re-inject), and `/clear` changes the `session_id` so a
fresh session re-injects naturally.

---

## The injection-token convention (shared with other plugins)

| | Value |
|---|---|
| Path | `/tmp/{plugin}-references-injection-{session_id}-{patternhash}` (via `tempfile.gettempdir()`) |
| Meaning | empty file = "this rule's references were already injected this turn" |
| Key | per matched **injection_rules pattern** (not per file), so all files matching a pattern share it |
| Producer / reader | py-kit / next-kit `inject_references.py` (create on inject, skip the pattern if its token exists) |
| Lifecycle manager | session-kit (delete-on-`UserPromptSubmit`, TTL-GC-on-`SessionStart`) |
| Swept glob | `*-references-injection-*` (see `hooks/session_gc.py` `_TOKEN_GLOB`) |

**Graceful fallback**: if session-kit is not installed, tokens are simply never
deleted per turn (consumers behave as once-per-pattern for the whole session) and
pile up until the OS clears `/tmp`. session-kit is an **optional companion**;
consumers must not depend on it.

The TTL is 1 day: no session lasts that long, so an active session's tokens are
recent and never swept; parallel sessions are protected for the same reason. The
worst case of an over-eager sweep is a harmless re-injection.

---

## Why a separate plugin (not centralized hook logic)

The cross-plugin contract here is a **filename convention only** — session-kit
globs `/tmp`, it never executes another plugin's code, and consumers never call
session-kit. This avoids the `${CLAUDE_PLUGIN_ROOT}` cross-plugin path-resolution
problem that caused `refs-inject-kit` to be rejected (see incident
`premature-cross-plugin-centralization`). Token lifetime is a session-global
concern, so a single manager is the natural design.

---

## Versions

| Version | Main change |
|---|---|
| 1.1.0 | Pivot to token-deletion: UserPromptSubmit deletes the session's injection tokens each turn (no marker file); SessionStart GCs stale tokens (1-day TTL) (PR151) |
| 1.0.0 | Initial: PreCompact + SessionStart(clear) context-generation marker (PR150, superseded) |
