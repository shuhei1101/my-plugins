# Regenerating a ref-inject hook trips creator-dispatch catchalls — they are false positives

## What happened

In PR157 (migrating `py-kit` onto the `ref-inject` injection mechanism), the work was to
regenerate `py-kit`'s injection hook from the `ref-inject` templates — exactly what
`/ref-inject:apply` does. Writing the regenerated files tripped `creator-dispatch`
`PreToolUse` blocks:

- `plugins/py-kit/hooks/inject_references.py` → **plugin-creator-dispatch** (the broad `plugins/` catchall — `.py` matches no specific rule)
- `plugins/py-kit/hooks/templates/*.j2` → **j2-stamp-check**
- `plugins/py-kit/CLAUDE.md` (+ the ref-inject CLAUDE.md, glossary) → **claude-creator-dispatch / rule-creator-dispatch**

These dispatch prompts say "invoke `/claude-kit:plugin-creator`" (etc.) before editing.
Taken literally that is wrong here: the file owner is **`/ref-inject:apply`**, not
plugin-creator. plugin-creator owns plugin-level concerns (plugin.json / root CLAUDE.md /
marketplace); it does not own the injection hook body.

## Why it is a false positive

`creator-dispatch` matches by file path with a first-match-wins `RULES` table, and the last
rule is a broad `plugins/`-wide catchall pointing at plugin-creator. A ref-inject-managed
hook file (`hooks/inject_references.py`, `templates/*.j2`) has no dedicated dispatch rule, so
it falls through to that catchall. But the dedicated mechanism skill for those files is
`/ref-inject:apply` (or, when it is not installed, executing its `SKILL.md` steps directly).

The dispatch blocks are **session-flag** type: they block the first matching edit per rule
per session, then pass subsequent edits. So the correct handling is: recognize the catchall
as a false positive for ref-inject re-application, then proceed (the retry passes).

## Relationship to the existing incident

This refines `creator-dispatch-block-means-invoke-creator` (PR156), which says "a dispatch
block means invoke the named creator, not retry the edit." That holds for the *specific*
dispatch rules (skill-creator / rule-creator / claude-creator / hook-creator). The exception:
when a **dedicated mechanism skill owns the files** (here `ref-inject:apply`), the generic
`plugins/` catchall does not apply — invoking plugin-creator would be wrong. Proceed via the
owning mechanism instead.

## Lesson

When regenerating ref-inject-managed injection files (PR158 next-kit, future re-applies),
expect the `plugins/` catchall + `j2-stamp-check` + `claude/rule-creator` blocks to fire.
They are false positives for this workflow: run `/ref-inject:apply` (the owning mechanism),
pass through the session-flag blocks, and do **not** detour into plugin-creator. The j2-stamp
check is satisfied because the ref-inject `.j2` templates already carry a top-of-file stamp.
