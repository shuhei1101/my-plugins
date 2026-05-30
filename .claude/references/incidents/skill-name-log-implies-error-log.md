# Skill named `*-log` was read as error-log

## Background

In PR131, the sub-skill that persists one issue to disk was named `issue-log`,
following the rationale "this skill *logs* an issue record". The SKILL.md described
it as a shared sub-skill for recording an issue, called by `issue-scan` and
`issue-create`.

## What the user pointed out

> ログっていうのはちょっと微妙やな
> なんかただログログって感じがするから
> なんかエラーログみたいなイメージやから
> それはちょっと変かな

"Log" reads as "error log" / "debug log" — the kind of throwaway append-only
stream you grep through after a failure. A skill whose job is to **create a
persistent issue record** should use a verb that signals persistence, not
streaming-log noise.

## Lesson

Renamed `issue-log` → `issue-save`. Updated all callers (`issue-scan`,
`issue-create`) and the TODO / notes.

When naming a skill / function / module whose job is to **persist data**:

| Avoid | Prefer | Reason |
|---|---|---|
| `log` | `save`, `write`, `record`, `persist` | "log" implies error/debug stream, not durable storage |
| `dump` | `save`, `export` | "dump" implies one-off ad-hoc output |

Reserve `log` for code that emits debug/error/audit lines into a log stream.

## Recurrence prevention

When proposing a name for a record-writing skill or function, default to
`save` / `write` / `record`. Only use `log` when the artifact is genuinely a
log line in a logging system.
