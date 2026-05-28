# session-kit Plugin Developer Guide

session-kit maintains a single **context-generation marker** per Claude Code
session so that other plugins can detect when the context was reset by
`/compact` or `/clear` and re-inject anything that was lost.

---

## What it does

| Hook | Action |
|---|---|
| `PreCompact` | Touch the marker (compaction is about to drop context) |
| `SessionStart` (source=`clear`) | Touch the marker (`/clear` wiped the context) |

It does **nothing else** — no prompt injection, no blocking, no output. The hook
only updates the marker's mtime.

`startup` and `resume` are intentionally NOT touched:
- `startup`: a fresh session has a new `session_id`; there are no stale tokens to invalidate.
- `resume`: the conversation is restored, so previously injected content is back in context.

---

## The marker contract (shared with other plugins)

| | Value |
|---|---|
| Path | `/tmp/claude-session-ctx-gen-{session_id}` (via `tempfile.gettempdir()`) |
| Meaning | mtime = time of the last context reset (compact / clear) for this session |
| Producer | session-kit (`hooks/ctx_marker.py`) |
| Consumers | Any plugin with a "once per session" injection token — e.g. py-kit / next-kit `inject_references.py` |

### How consumers use it

A consumer that writes a per-file "already injected" token compares mtimes:

```python
marker = pathlib.Path(tempfile.gettempdir()) / f"claude-session-ctx-gen-{session_id}"
if token.exists():
    # re-inject only if a reset happened after the last injection
    if not (marker.exists() and marker.stat().st_mtime_ns > token.stat().st_mtime_ns):
        return  # still valid → skip
token.touch()  # (re)inject and refresh the token mtime
```

**Graceful fallback**: if session-kit is not installed the marker never exists,
so consumers behave as plain once-per-session (the pre-session-kit behavior).
session-kit is an **optional companion** — consumers must not hard-fail when it
is absent.

---

## Why a separate plugin (not centralized hook logic)

The cross-plugin contract here is a **file path convention only** — consumers
`stat()` the marker, they never execute session-kit's script. This avoids the
`${CLAUDE_PLUGIN_ROOT}` cross-plugin path-resolution problem that caused
`refs-inject-kit` to be rejected (see incident `premature-cross-plugin-centralization`).
The context-generation fact is genuinely **session-global** (one fact per session),
so a single producer is the natural design.

---

## Versions

| Version | Main change |
|---|---|
| 1.0.0 | Initial: PreCompact + SessionStart(clear) context-generation marker (PR150) |
