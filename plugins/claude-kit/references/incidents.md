# incidents — Recurrence Prevention Format

Documents the structure and usage of the `incidents` rule, which captures
failures, wrong assumptions, and misconceptions so they are not repeated.

---

## File Structure

```
.claude/rules/
└── incidents.md                    # Index — always loaded, kept short

.claude/references/incidents/
├── {slug}.md                       # Detail (English)
└── {slug}.jp.md                    # Detail (Japanese)
```

The index lives in `.claude/rules/` so it is always loaded as a system prompt.
The detail files live in `.claude/references/incidents/` so they are **not**
auto-loaded — Claude reads them only when the index links point there.

### incidents.md (index)

Always loaded into every session. Keep it short — every line costs context window
space. Write only a one-line summary per entry; full details live in the subfolder.

```markdown
# Incidents

| Date | Summary | Detail |
|---|---|---|
| YYYY-MM-DD | {one-line description of what went wrong and how to avoid it} | [detail](../references/incidents/{slug}.md) |
```

**Writing discipline**: Be ruthless about brevity. One line per incident. If a
summary needs more than ~80 chars, shorten it — the reader follows the link.

### {slug}.md (detail — English)

```markdown
# {Title}

**Date**: YYYY-MM-DD
**Category**: {command-error | wrong-assumption | tool-misuse | other}

## What Happened

{Concrete description: what was tried, what failed, what the actual correct approach is}

## How to Avoid

{Specific rule or check to apply next time}

## Context

{Optional: project, environment, or conditions where this applies}
```

### {slug}.jp.md (detail — Japanese)

Same structure as `{slug}.md`, written in Japanese.

---

## Naming the slug

Use kebab-case. Be specific enough to be scannable:

- `python-encode-utf8-not-cp932`
- `git-worktree-path-relative`
- `marketplace-version-out-of-sync`

---

## When to write

Write an incident entry when:
- A command was run and failed, and the correct command is now known
- Claude gave a wrong answer based on a wrong assumption, and the user corrected it
- A tool, flag, or API behaved differently than expected

Do **not** write an entry for:
- General knowledge that belongs in a skill or rule
- Things already documented elsewhere
- Obvious mistakes unlikely to recur
