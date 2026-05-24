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

Read each note and assign a promotion type using the criteria below.

| Type | Target | When to use |
|---|---|---|
| **A — Rule** | `.claude/rules/` | File dependencies, "edit X → also update Y", path structure discoveries |
| **B — CLAUDE.md** | `CLAUDE.md` | Project-wide conventions, prohibitions, naming rules (needed every session) |
| **C — Reference** | `.claude/references/` | Long tables, design diagrams, detailed specs (linked from rules) |
| **D — Discard** | Delete | Temporary comparisons, rejected ideas, completed investigation notes |

→ Proceed to Step 3

#### Output

- Each note's assigned type (A/B/C/D) with reasoning

---

### Step 3: Cross-check against existing artifacts

#### Condition

- Step 2 complete

#### Process

For notes typed A, B, or C, check whether existing artifacts can absorb the content:

| Type | Where to look |
|---|---|
| A | `.claude/rules/` — scan filenames and headings |
| B | Project `CLAUDE.md` / `plugins/*/CLAUDE.md` |
| C | `.claude/references/` — scan filenames |

- **Existing file can absorb it** → plan to append (no new file needed)
- **No existing file** → plan to create new

→ Proceed to Step 4

#### Output

- Promotion plan: each note's target path (existing or new) and action (append or create)

---

### Step 4: Present plan and get user approval

#### Condition

- Step 3 complete

#### Process

1. Display the plan in this format:

   ```
   ## Note Promotion Plan

   | Note | Type | Target | Action |
   |---|---|---|---|
   | foo.md | A — Rule | .claude/rules/feature/foo.md | Create new |
   | bar.md | B — CLAUDE.md | plugins/work-kit/CLAUDE.md | Append |
   | baz.md | D — Discard | — | Delete |
   ```

2. Ask: "Proceed with this plan? Let me know if you want any changes."

→ Proceed to Step 5 after user approval

#### Output

- User-approved promotion plan

#### Notes

##### Prohibitions

- Do not edit or delete any files before user approval

---

### Step 5: Execute promotions

#### Condition

- Step 4 complete (user approved)

#### Process

Execute the plan in order:

1. **Type A — Rule**: invoke `/claude-kit:rule-creator` to create or update the rule
2. **Type B — CLAUDE.md**: invoke `/claude-kit:claude-creator` to update CLAUDE.md
3. **Type C — Reference**: create or append to the reference file directly
4. **Type D — Discard**: delete the note file

→ Proceed to Step 6

#### Output

- Target files created or updated

#### Notes

##### For rules and CLAUDE.md

Use the corresponding creator skill — do not edit directly.
The creator skills enforce correct structure, version bumps, and JP mirror sync.

---

### Step 6: Offer to delete promoted notes

#### Condition

- Step 5 complete

#### Process

1. Propose deleting notes that were successfully promoted:
   ```
   These notes have been promoted. OK to delete them?
   - .work/notes/foo.md (→ .claude/rules/feature/foo.md)
   - .work/notes/bar.md (→ appended to CLAUDE.md)
   ```
2. Delete only if the user approves.

→ Done

#### Notes

- Declining to delete is valid ("keep as reference"). Do not force.
- Discarded notes (Type D) were already deleted in Step 5 — no re-confirmation needed.

---

## References

### Promotion type quick reference

| Content type | Target |
|---|---|
| File dependencies, "edit X → update Y" | Rule (`.claude/rules/`) |
| Naming conventions, folder structure, prohibitions (every session) | `CLAUDE.md` |
| Long tables, design diagrams, detailed specs (linked from rules) | `.claude/references/` |
| Temporary comparisons, rejected ideas, completed investigation | Discard |

### Creator skill map

| Promotion type | Skill to use |
|---|---|
| Rule | `/claude-kit:rule-creator` |
| CLAUDE.md | `/claude-kit:claude-creator` |
| Reference | Direct file creation (no skill needed) |
