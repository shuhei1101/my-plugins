# Common — dev-kit Shared Reference

Conventions shared across frontend, backend, and any other implementation context.
Topics include logging, Markdown style, comment policies, and other format-agnostic rules.

---

## Logging

This section is referenced by `dev-kit:ui-dev` and applies to every language/framework
that emits runtime logs (frontend JS, backend Python/Node, etc.).

### Rules

1. **Always use a logger** — never call `console.log` (JS) or `print` (Python) directly in
   non-script code. Route through a logger object that controls level and format.
2. **Output format: JSON Lines** — each log record is one JSON object on its own line.
   This is the only format Claude / log aggregators / `jq` can reliably parse.
   ```jsonl
   {"ts":"2026-05-17T12:34:56.789Z","level":"info","msg":"user logged in","userId":"u_42"}
   {"ts":"2026-05-17T12:34:57.001Z","level":"warn","msg":"rate limit nearing","remaining":3}
   ```
3. **Emit operation logs generously** — user actions, state transitions, API calls in/out,
   and decision branches should each produce a log line. "What is currently happening"
   should be visible from logs alone.
4. **Each log line is short** — never dump large objects across many lines.
   Summarize: `{"items": 1284, "first": "a", "last": "z"}` instead of pasting the full list.
   If full detail is needed, log a reference (path/ID) and write the full payload to a file.
5. **Levels: `debug` / `info` / `warn` / `error`** — pick one per record.
   - `debug` — verbose internal state, off by default in production
   - `info`  — normal operations, user actions, state transitions
   - `warn`  — recoverable anomalies, retries, fallbacks taken
   - `error` — unrecoverable failures requiring attention
6. **Production default level is `error`** — switch to `debug` only while investigating.
   The level must be configurable at runtime (env var, config file, or UI).
7. **Never log secrets** — passwords, tokens, full credit cards, PII beyond what is
   required. Redact at the logger layer.

### Required fields per record

| Field | Required | Notes |
|---|---|---|
| `ts`    | yes | ISO 8601 UTC, millisecond precision |
| `level` | yes | one of debug/info/warn/error |
| `msg`   | yes | short human-readable summary (≤ 120 chars) |
| `...`   | optional | structured context (IDs, counts, durations). Avoid nested objects deeper than 2 levels. |

### Why JSON Lines specifically

- One record per line → tail-friendly, grep-friendly, `jq` / `jq -s` friendly
- Each line is self-contained → no parse state needed for partial logs
- Pretty-print only when displayed to a human, never on disk

---

## Future topics

> **TODO**: Content to be added in future PRs.
>
> Planned topics:
> - Markdown style (headings, lists, tables, code fences)
> - Cross-language commit message conventions
> - Cross-cutting commenting rules (when to write English vs Japanese)
