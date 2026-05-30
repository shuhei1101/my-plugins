---
name: notes-to-claude
description: |
  Promote `.work/notes/` content to permanent Claude artifacts (rules, CLAUDE.md, references).
  Trigger when the user says "promote notes", "notes-to-claude", "turn notes into rules",
  "clean up notes", "move notes to rules", or "永続化したい" / "ノートを昇格" / "notes を整理".
---

# workspace:notes-to-claude — Promote Notes to Permanent Knowledge

Analyzes `.work/notes/` files and converts valuable temporary memos into
permanent Claude artifacts: rules, CLAUDE.md additions, or reference files.
Fully automatic — no confirmation prompts.

---

## Overview

`.work/notes/` holds disposable working notes — meeting minutes, design memos, investigation scratchpads.
They are not auto-loaded by Claude. Run this skill periodically to extract durable knowledge and clean up.
Promoted notes are deleted automatically. Discarded notes are also deleted immediately.

No confirmation steps. This skill always runs on a branch, so all changes are reviewable via commits.

**Prerequisite**: `claude-kit` plugin must be installed (provides the creator skills used in Step 3).

**Relation to other skills**:
- `claude-refactor` audits what is *already inside* `.claude/` — detects bloat, duplicates, type mismatches.
- `notes-to-claude` ingests knowledge *from* `.work/notes/` *into* `.claude/`.
Run `notes-to-claude` first to populate `.claude/`, then `claude-refactor` to keep it tidy.

---

## Tasks

### Step 1: List notes

#### Condition

- Always — run first

#### Process

1. List files under `.work/notes/`:
   ```bash
   ls .work/notes/
   ```
2. If no files exist, report "No notes to promote" and stop.

→ Proceed to Step 2

#### Output

- List of note files

---

### Step 2: Analyze, classify, and plan

#### Condition

- Step 1 complete

#### Process

Read each note and assign a promotion type using the decision table in References.

| Type | Target | When to use |
|---|---|---|
| **A — Rule** | `.claude/rules/` | File dependencies ("edit X → also update Y"), path structure, domain conventions triggered when specific files are opened |
| **B — CLAUDE.md** | `CLAUDE.md` | Project-wide conventions, prohibitions, naming rules that must be present **every session** regardless of which files are open |
| **C — Reference** | `.claude/references/` | Long tables, design diagrams, detailed specs — too heavy for CLAUDE.md but needed on demand (linked from rules or CLAUDE.md) |
| **D — Discard** | Delete | Temporary comparisons, rejected ideas, completed investigation notes no longer needed |

Also apply the proliferation guard (see References): if an existing artifact covers the same domain, plan to append rather than create a new file.

→ Proceed to Step 3

#### Output

- Each note's type (A/B/C/D), target path, and action (append or create new)

---

### Step 3: Execute promotions

#### Condition

- Step 2 complete

#### Process

Execute the plan one item at a time. **Do not edit target files directly — always use the creator skill.**

| Type | Creator skill | Notes |
|---|---|---|
| **A — Rule** | `/claude-kit:rule-creator` | Handles `paths:` frontmatter, folder placement, JP mirror, and link rules |
| **B — CLAUDE.md** | `/claude-kit:claude-creator` | Handles thinness principle, JP mirror, and subsection placement |
| **C — Reference** | (direct file creation) | No creator skill needed; create `.claude/references/{slug}.md` directly |
| **D — Discard** | (delete) | `rm .work/notes/{file}` |

For rule placement (Type A), use the folder structure guide in References.

→ Proceed to Step 4

#### Output

- Target files created or updated

---

### Step 4: Delete promoted notes

#### Condition

- Step 3 complete

#### Process

1. Delete all notes that were promoted (Type A / B / C):
   ```bash
   rm .work/notes/{file}
   ```
2. Discarded notes (Type D) were already deleted in Step 3 — no duplicate action needed.

→ Done

#### Output

- All promoted and discarded notes removed from `.work/notes/`

---

## References

### Promotion type decision table

Derived from `claude-kit` references (common.md, rules.md, claude-md.md).
Embedded here so no cross-plugin file reads are needed at runtime.

| Content nature | Best target | Reason |
|---|---|---|
| Cross-path file sync: "edit X → also update Y" | Rule | Path-matched auto-load — only fires when those files are opened |
| Domain-specific conventions tied to a folder or file type | Rule | Narrow `paths:` keeps context cost low |
| Project-wide prohibition, naming convention, or onboarding info | CLAUDE.md | Loaded every session; must be universally applicable |
| Multi-step workflow the user would invoke explicitly | Skill (`.claude/skills/`) | On-demand; not appropriate for notes-to-claude |
| Long table, diagram, or detailed spec referenced occasionally | `.claude/references/` | On-demand load keeps CLAUDE.md thin |
| One-time observation, temporary state, rejected idea | Discard | Not worth persisting |

### Proliferation guard (existing artifact check)

| Type | Where to look |
|---|---|
| A — Rule | `.claude/rules/` — scan filenames and first 20 lines |
| B — CLAUDE.md | Project `CLAUDE.md` — check whether the section already exists |
| C — Reference | `.claude/references/` — scan filenames |

If an existing file covers the domain → append to it (no new file).

### Rule folder placement guide

| Folder | Use when |
|---|---|
| `core/` | Project-wide conventions, workflow, environment setup |
| `feature/` | Feature- or domain-specific rules (1 feature = 1 file) |
| `ui/` | Frontend component or page rules (if frontend exists) |
| `api/` | Backend routing or handler rules (if applicable) |

### Creator skill summary

| Skill | What it enforces |
|---|---|
| `/claude-kit:rule-creator` | `paths:` frontmatter, correct folder, JP mirror at `.claude/rules-jp/` |
| `/claude-kit:claude-creator` | CLAUDE.md thinness principle, JP mirror, subsection structure |
| `/claude-kit:skill-creator` | Step structure, `description` frontmatter, JP mirror |
| `/claude-kit:hook-creator` | Hook event type, settings.json wiring, loop-prevention |

### Relationship to other skills

| Skill | Starting point | Goal |
|---|---|---|
| `workspace:notes-to-claude` (this skill) | `.work/notes/` temporary memos | Populate `.claude/` with new knowledge |
| `claude-kit:claude-refactor` | Existing `.claude/` contents | Audit, deduplicate, and reorganize what's already there |
