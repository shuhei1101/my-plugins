---
name: claude-rule
description: Authoring conventions for Claude instruction files (CLAUDE.md, SKILL.md, .claude/rules/, prompts). Always apply this skill when: creating or editing a CLAUDE.md file, creating or editing a SKILL.md file, creating or editing files under .claude/rules/, writing prompt files or instruction documents that Claude will read, asking about the bilingual (.jp.md) documentation convention, or setting up a new project that will use Claude Code. Trigger immediately when the user says "create CLAUDE.md", "write a skill", "make a prompt", "create instructions for Claude", "write a SKILL.md", "set up .claude/rules/", or any request to author a file that Claude will use as directives.
---

# Claude Instruction File Authoring Rules

These rules apply whenever you create or edit any file that Claude reads as instructions — `CLAUDE.md`, `SKILL.md`, `.claude/rules/*.md`, or standalone prompt files.

## Core Rule: AI Directives Must Be Written in English

Claude Code auto-loads instruction files. Always write the content of these files in English so Claude receives clear, unambiguous instructions without translation overhead.

## Bilingual File Convention

Every instruction file has a paired Japanese mirror for the human author's reference. **Where the mirror lives depends on how Claude Code loads the file:**

### Filename-anchored auto-load (CLAUDE.md, SKILL.md)

Claude Code looks for these by **exact filename**. Co-locate the JP mirror as `<basename>.jp.md`:

| Auto-loaded by Claude (English) | Human reference only (Japanese) |
|---------------------------------|---------------------------------|
| `CLAUDE.md` | `CLAUDE.jp.md` |
| `SKILL.md` | `SKILL.jp.md` |

Because Claude only matches the exact filename, `CLAUDE.jp.md` and `SKILL.jp.md` are never auto-loaded.

### Recursive directory auto-load (`.claude/rules/`)

Claude Code recursively discovers **every** `.md` file under `.claude/rules/`, regardless of suffix. A `.jp.md` placed inside `.claude/rules/` would be auto-loaded — the suffix does not exclude it.

To keep a Japanese mirror without it being auto-loaded, put it in a parallel directory:

| Auto-loaded by Claude (English) | Human reference only (Japanese) |
|---------------------------------|---------------------------------|
| `.claude/rules/<name>.md` | `.claude/rules-jp/<name>.md` |

`.claude/rules-jp/` is not a directory Claude Code scans, so files there are excluded automatically — no `claudeMdExcludes` setting required.

## Update Workflow

When a change is needed in an instruction file:

1. **Update the JP mirror first** — write or revise the change in Japanese. Confirm the intent is expressed correctly.
2. **Then update the English original** — apply the equivalent change to the authoritative English file.
3. **Keep both in sync at all times.** Never update one without updating the other.

The user gives instructions in Japanese. Your job is to:
- Receive intent in Japanese (via the JP mirror or user message)
- Write or update the authoritative English file accordingly
- Keep the JP mirror in sync

## CLAUDE.md vs `.claude/rules/`

Choose the location based on how often the instruction is needed:

- **CLAUDE.md** — instructions Claude needs every session (worktree workflow, commit conventions, server management, project-wide meta-rules). Loaded into every session, so keep it under **~200 lines**.
- **`.claude/rules/<name>.md` with `paths:` frontmatter** — instructions specific to a folder or file pattern. Loaded only when Claude reads a matching file. Keeps CLAUDE.md lean and avoids spending context on rules that are not currently relevant.

Path-scoped frontmatter:

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "src/api/**/*.tsx"
---

# API rules
- ...
```

A rule file without `paths:` is loaded unconditionally, just like CLAUDE.md.

## Two patterns for path-scoped rules

1. **Process / convention rules** — instructions on how to work in a folder (e.g., wiki editing conventions, prompt-authoring rules). Self-contained.
2. **Source ↔ documentation linking rules** — short rules whose main purpose is listing the wiki/spec docs that govern a folder. When Claude edits source under that path, the rule injects "the relevant specs are X, Y, Z" so the implementation stays aligned with the docs.

## Meta-rule: when editing a rule file

When you edit a file under `.claude/rules/`:

1. Check whether wiki / docs referenced from that rule still match the rule's content. Update them if they have drifted (one source of truth).
2. Update the matching `.claude/rules-jp/<same-name>.md` so the Japanese mirror stays in sync.

## File Naming Summary

| File | Language | Loaded by Claude? | Purpose |
|------|----------|-------------------|---------|
| `CLAUDE.md` | English | Yes (auto) | Project-level instructions |
| `CLAUDE.jp.md` | Japanese | No | Human reference for CLAUDE.md |
| `SKILL.md` | English | Yes (auto) | Skill definition |
| `SKILL.jp.md` | Japanese | No | Human reference for SKILL.md |
| `.claude/rules/<name>.md` | English | Yes (when `paths:` matches, or always if no `paths:`) | Folder-scoped or always-on rule |
| `.claude/rules-jp/<name>.md` | Japanese | No (parallel directory not scanned) | Human reference for the rule |

## Creating a New Instruction File

When creating any Claude instruction file from scratch:

1. Draft the Japanese version first (`*.jp.md` or under `.claude/rules-jp/`) to lock in intent
2. Translate and write the English version
3. Both files are committed together

## What NOT to Do

- Do not write Japanese content inside `CLAUDE.md`, `SKILL.md`, or `.claude/rules/*.md` — Claude reads these directly
- Do not place the Japanese mirror of a rule inside `.claude/rules/` (it would be auto-loaded). **Always use `.claude/rules-jp/`.**
- Do not create a JP mirror with different content from its English counterpart
- Do not skip creating the JP mirror — the human author needs it for future edits
