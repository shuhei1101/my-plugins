# session-kit Plugin Developer Guide

session-kit maintains a single **session marker** per Claude Code session so that
other plugins can detect when the context was reset by `/compact` and re-inject
anything that was lost. It also garbage-collects stale session temp files.

---

## What it does

| Hook | Action |
|---|---|
| `PreCompact` | Touch the **session marker** (compaction is about to drop context) |
| `SessionStart` | **TTL cleanup**: delete stale session temp files older than 1 day |

It does **nothing else** — no prompt injection, no blocking, no output.

### Why no `/clear` handling

`/clear` changes the `session_id` itself, so a fresh session naturally re-injects
(its new `session_id` has no tokens; old tokens belong to the old `session_id`).
The only reset that keeps the same `session_id` is `/compact`, so the marker is
touched on `PreCompact` only.

`resume` keeps the same `session_id` but restores the conversation (injected
content is back in context), so it needs no marker bump either.

---

## The session marker contract (shared with other plugins)

| | Value |
|---|---|
| Path | `/tmp/claude-session-ctx-gen-{session_id}` (via `tempfile.gettempdir()`) |
| Meaning | mtime = time of the last context reset (`/compact`) for this session |
| Producer | session-kit (`hooks/ctx_marker.py`, on `PreCompact`) |
| Consumers | Any plugin with a per-file "injection token" — e.g. py-kit / next-kit `inject_references.py` |

### How consumers use it

A consumer that writes a per-file injection token compares mtimes:

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

## TTL cleanup (SessionStart)

Empty marker/token files would otherwise accumulate in `/tmp` forever (each
session leaves its `session_id`-keyed files behind). On every `SessionStart`,
session-kit deletes files older than **1 day** matching:

| Glob (under `tempfile.gettempdir()`) | Owner | What |
|---|---|---|
| `claude-session-ctx-gen-*` | session-kit | session markers |
| `*-references-injection-*` | py-kit / next-kit / future `*-kit` | injection tokens |

1 day is safe because no session lasts that long; an active session's files are
recent (< 1 day) so they are never swept, and parallel sessions are protected for
the same reason. Worst case of an over-eager sweep is a harmless re-injection.

> Deleting other plugins' injection tokens is a **filename-convention coupling**
> only (session-kit globs `/tmp`, it never executes another plugin's code). The
> swept globs are listed above and in `hooks/ctx_marker.py` (`_CLEANUP_GLOBS`).

---

## Why a separate plugin (not centralized hook logic)

The cross-plugin contract here is a **file path / filename convention only** —
consumers `stat()` the marker, they never execute session-kit's script. This
avoids the `${CLAUDE_PLUGIN_ROOT}` cross-plugin path-resolution problem that
caused `refs-inject-kit` to be rejected (see incident
`premature-cross-plugin-centralization`). The context-generation fact is
genuinely **session-global** (one fact per session), so a single producer is the
natural design.

---

## Versions

| Version | Main change |
|---|---|
| 1.1.0 | SessionStart repurposed from `/clear` marker-bump to 1-day TTL cleanup of stale temp files; marker now bumped on PreCompact only (PR151) |
| 1.0.0 | Initial: PreCompact + SessionStart(clear) context-generation marker (PR150) |
