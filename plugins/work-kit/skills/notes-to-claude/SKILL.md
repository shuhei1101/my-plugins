---
name: notes-to-claude
description: |
  Promote `.work/notes/` content to permanent Claude artifacts (rules, CLAUDE.md, references).
  Trigger when the user says "promote notes", "notes-to-claude", "turn notes into rules",
  "clean up notes", "move notes to rules", or "永続化したい" / "ノートを昇格" / "notes を整理".
---

# work-kit:notes-to-claude — Promote Notes to Permanent Knowledge

Analyzes `.work/notes/` files and converts valuable temporary memos into
permanent Claude artifacts: rules, CLAUDE.md additions, or reference files.

---

## Overview

`.work/notes/` holds disposable working notes — meeting minutes, design memos, investigation scratchpads.
They are not auto-loaded by Claude. Run this skill periodically to extract durable knowledge and clean up.
Notes that don't need promotion can stay indefinitely; promoted notes should be deleted.

**Prerequisite**: `claude-kit` plugin must be installed (provides the creator skills used in Step 5).

**Relation to `claude-refactor`**:
- `claude-refactor` audits what is *already inside* `.claude/` — detects bloat, duplicates, type mismatches.
- `notes-to-claude` ingests knowledge *from* `.work/notes/` *into* `.claude/`.
These skills are complementary: run `notes-to-claude` first to populate `.claude/`, then `claude-refactor` to keep it tidy.

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

### Step 2: Analyze and classify each note

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

→ Proceed to Step 3

#### Output

- Each note's assigned type (A/B/C/D) with reasoning

---

### Step 3: Cross-check against existing artifacts (proliferation guard)

#### Condition

- Step 2 complete

#### Process

For notes typed A, B, or C, check whether an existing artifact can absorb the content.
**Do not create a new file if an existing one covers the same domain.**

| Type | Where to look |
|---|---|
| A | `.claude/rules/` — scan filenames and first 20 lines of each rule |
| B | Project `CLAUDE.md` — check whether the section already exists |
| C | `.claude/references/` — scan filenames |

Decision:
- **Existing file covers the domain** → plan to append (no new file needed)
- **No existing file** → plan to create new

→ Proceed to Step 4

#### Output

- Promotion plan: each note → target path (existing or new) + action (append or create new)

---

### Step 4: Present plan and get user approval

#### Condition

- Step 3 complete

#### Process

1. Display the plan:

   ```
   ## Note Promotion Plan

   | Note | Type | Target | Action |
   |---|---|---|---|
   | foo.md | A — Rule | .claude/rules/feature/foo.md | Create new |
   | bar.md | B — CLAUDE.md | CLAUDE.md | Append to §Conventions |
   | baz.md | C — Reference | .claude/references/bar-detail.md | Create new |
   | qux.md | D — Discard | — | Delete |
   ```

2. Ask: "Proceed with this plan? Let me know if you want any changes."

→ Proceed to Step 5 after user approval

#### Notes

##### Prohibitions

- Do not edit or delete any files before user approval

---

### Step 5: Execute promotions

#### Condition

- Step 4 complete (user approved)

#### Process

Execute the approved plan one item at a time. Use the creator skills below — **do not edit target files directly**.

| Type | Creator skill | Notes |
|---|---|---|
| **A — Rule** | `/claude-kit:rule-creator` | Handles `paths:` frontmatter, folder placement, JP mirror, and link rules |
| **B — CLAUDE.md** | `/claude-kit:claude-creator` | Handles thinness principle, JP mirror, and subsection placement |
| **C — Reference** | (direct file creation) | No creator skill needed; create `.claude/references/{slug}.md` directly |
| **D — Discard** | (delete) | `rm .work/notes/{file}` |

For rule placement (Type A), use the folder structure in References to decide where the rule file goes.

→ Proceed to Step 6

#### Output

- Target files created or updated

---

### Step 6: Offer to delete promoted notes

#### Condition

- Step 5 complete

#### Process

1. List promoted notes and ask for deletion confirmation:
   ```
   These notes were promoted. OK to delete them?
   - .work/notes/foo.md (→ .claude/rules/feature/foo.md)
   - .work/notes/bar.md (→ appended to CLAUDE.md)
   ```
2. Delete only if the user approves.

→ Done

#### Notes

- Declining to delete is valid. Do not force.
- Discarded notes (Type D) were already deleted in Step 5.

---

## References

### Promotion type decision table

Derived from `claude-kit` references (common.md, rules.md, claude-md.md).
These criteria are embedded here so no cross-plugin file reads are needed at runtime.

| Content nature | Best target | Reason |
|---|---|---|
| Cross-path file sync: "edit X → also update Y" | Rule | Path-matched auto-load — only fires when those files are opened |
| Domain-specific conventions tied to a folder or file type | Rule | Narrow `paths:` keeps context cost low |
| Project-wide prohibition, naming convention, or onboarding info | CLAUDE.md | Loaded every session; must be universally applicable |
| Multi-step workflow the user would invoke explicitly | Skill (`.claude/skills/`) | On-demand; not appropriate for notes-to-claude |
| Long table, diagram, or detailed spec referenced occasionally | `.claude/references/` | On-demand load keeps CLAUDE.md thin |
| One-time observation, temporary state, rejected idea | Discard | Not worth persisting |

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
| `work-kit:notes-to-claude` (this skill) | `.work/notes/` temporary memos | Populate `.claude/` with new knowledge |
| `claude-kit:conversation-to-claude` | Session conversation history | Capture session learnings as Claude artifacts |
| `claude-kit:claude-refactor` | Existing `.claude/` contents | Audit, deduplicate, and reorganize what's already there |
