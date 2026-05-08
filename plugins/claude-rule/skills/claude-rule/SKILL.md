---
name: claude-rule
description: Authoring conventions for Claude instruction files (CLAUDE.md, SKILL.md, prompts). Always apply this skill when: creating or editing a CLAUDE.md file, creating or editing a SKILL.md file, writing prompt files or instruction documents that Claude will read, asking about the bilingual (.jp.md) documentation convention, or setting up a new project that will use Claude Code. Trigger immediately when the user says "create CLAUDE.md", "write a skill", "make a prompt", "create instructions for Claude", "write a SKILL.md", or any request to author a file that Claude will use as directives.
---

# Claude Instruction File Authoring Rules

These rules apply whenever you create or edit any file that Claude reads as instructions — including `CLAUDE.md`, `SKILL.md`, and standalone prompt files.

## Core Rule: AI Directives Must Be Written in English

Claude Code auto-loads instruction files by exact filename (`CLAUDE.md`, `SKILL.md`). Always write the content of these files in English. This ensures Claude receives clear, unambiguous instructions without translation overhead.

## Bilingual File Convention

Every instruction file has a paired Japanese translation file for the human author's reference.

| Auto-loaded by Claude (English) | Human reference only (Japanese) |
|---------------------------------|---------------------------------|
| `CLAUDE.md` | `CLAUDE.jp.md` |
| `SKILL.md` | `SKILL.jp.md` |

**`.jp.md` files are never auto-loaded by Claude Code.** They are purely for the human to read, understand, and verify the intended content before and after editing the English original.

Why this split exists: the human author thinks and communicates in Japanese, but Claude must receive instructions in English. The `.jp.md` file acts as the human's working copy — it captures intent in the author's native language and makes it easy to verify that the English file says exactly what was intended.

## Update Workflow

When a change is needed in an instruction file:

1. **Update `.jp.md` first** — write or revise the change in Japanese. Confirm the intent is expressed correctly.
2. **Then update the English original** — apply the equivalent change to the authoritative English file.
3. **Keep both files in sync at all times.** Never update one without updating the other.

The user will give you instructions in Japanese. Your job is to:
- Receive the intent in Japanese (via the `.jp.md` or user message)
- Write or update the authoritative English file accordingly
- Keep the `.jp.md` in sync

## File Naming Summary

| File | Language | Loaded by Claude? | Purpose |
|------|----------|-------------------|---------|
| `CLAUDE.md` | English | Yes (auto) | Project-level instructions |
| `CLAUDE.jp.md` | Japanese | No | Human reference for CLAUDE.md |
| `SKILL.md` | English | Yes (auto) | Skill definition |
| `SKILL.jp.md` | Japanese | No | Human reference for SKILL.md |

## Creating a New Instruction File

When creating any Claude instruction file from scratch:

1. Draft the Japanese version first (`*.jp.md`) to lock in intent
2. Translate and write the English version (exact name, no suffix)
3. Both files should be committed together

## What NOT to Do

- Do not write Japanese content inside `CLAUDE.md` or `SKILL.md` — Claude reads these directly
- Do not create `.jp.md` files with different content than their English counterpart
- Do not skip creating the `.jp.md` — the human author needs it for future edits
