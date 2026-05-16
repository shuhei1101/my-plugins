# Claude Code File Type Usage Guide

This document defines when to use `CLAUDE.md`, `.claude/rules/`, and `.claude/skills/`.
Referenced in Step 0 of each creator skill.
Japanese mirror: `references/file-types.jp.md`

---

## CLAUDE.md

### When it loads

| Placement | When loaded |
|---|---|
| Project root | At every session start — always loaded |
| Subfolder | Lazily, when Claude reads any file in that folder or its subfolders |

A subfolder CLAUDE.md is not loaded at session start.
It loads the moment Claude accesses a file in that directory.

### Purpose

- Describing the contents and conventions of a folder
- General rules that apply whenever Claude works in this folder
- Brief overview of what files in the folder do

### Good examples

- "This folder contains X. When editing, watch out for Y."
- "Files in this folder follow the X format."

### Not a good fit

- Multi-step workflows or procedures → `.claude/skills/` is more appropriate

---

## `.claude/rules/` (Path-scoped rules)

### When it loads

Loads when Claude **reads** a file matching the `paths:` pattern.

- ✅ Reading a file → loads
- ✅ Editing a file (Claude reads before editing) → loads
- ❌ Shell-only commands (`mv`, `rm`, etc.) without reading → does not load
- ❌ Working without accessing a matching file → does not load

### Purpose

**Primary purpose: cross-path linking to prevent missed updates.**

The key advantage is that `paths:` can span multiple different folders.
Bundle related files — source, tests, specs, config — into one rule so that
when any one of them is read, Claude is reminded to check the others.

### When to use

- Related files are **spread across multiple different folders**
- You want to define a linked rule: "if X changes, Y and Z must also be updated"
- You need to manage a domain (e.g., model definitions) that spans multiple locations

### Good examples

- Register `src/models/*.py`, `tests/test_models.py`, and `docs/specs/models.md` under `paths:`
  → Whenever any one is read, Claude is prompted to verify and update the others
- A cross-reference table with "update when" conditions for each related file

### Single-folder content: `.claude/rules/` vs subfolder `CLAUDE.md`

Either can hold folder-specific conventions. The choice depends on your priority:

| Priority | Choice |
|---|---|
| **See all active rules in one place** (auditability) | `.claude/rules/<name>.md` |
| **Keep rules co-located with the code** (proximity) | Subfolder `CLAUDE.md` |

Cross-path linking ("if X changes, also update Y in a different folder") always belongs in `.claude/rules/`.

---

## `.claude/skills/`

### When it loads

- When explicitly invoked as `/skill-name`
- When the `description` frontmatter condition is matched (auto-trigger)

Do not use `disable-model-invocation: true`. It blocks all model invocations including via the Skill tool. Control auto-triggering through the `description` frontmatter instead.

### Purpose

Define multi-step workflows and procedures.

### Good examples

- PR creation flow, documentation authoring, information gathering / listing routines
- Complex tasks that involve back-and-forth with the user

### Not a good fit

- Simple rules that fit in 1-2 lines → write in `CLAUDE.md` or `.claude/rules/`

---

## Summary

| File | When read | What to write |
|---|---|---|
| `CLAUDE.md` (root) | Every session start | Project-wide conventions and workflow |
| `CLAUDE.md` (subfolder) | When Claude accesses that folder | Folder description and local conventions (co-location preferred) |
| `.claude/rules/<name>.md` | When a matching file is read | Cross-path links and missed-update prevention. Single-folder also fine (auditability preferred) |
| `.claude/skills/<name>/SKILL.md` | When invoked | Workflow procedures and step-by-step tasks |
