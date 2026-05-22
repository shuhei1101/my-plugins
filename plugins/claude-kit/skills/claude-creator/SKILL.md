---
name: claude-creator
description: |
  Create or overhaul a CLAUDE.md (and its CLAUDE.jp.md mirror) for a project or subfolder.
  Trigger when the user says "CLAUDE.md を作って", "CLAUDE.md を書いて", "create a CLAUDE.md",
  "クロードのガイドを作りたい", "このフォルダの CLAUDE.md を作って", or asks to set up
  Claude Code instructions for a project or specific folder.
---

# claude-creator — CLAUDE.md Authoring

Creates a CLAUDE.md and its paired CLAUDE.jp.md mirror for a project or subfolder.

---

## Overview

CLAUDE.md can be placed in two locations with different behaviors:

| Placement | When loaded |
|---|---|
| Project root | Loaded at every session start |
| Subfolder | Loaded lazily when Claude reads any file in that folder or its subfolders |

**Project root CLAUDE.md**: Defines the overall project workflow, commit rules, server management,
and the folder-scoped rule table.

**Subfolder CLAUDE.md**: Describes the folder's contents and conventions.
Useful for giving Claude context about what files in this folder do and how to work with them,
without loading that context at every session start.

---

## Tasks

### Step 0: Read background materials

#### Condition

- Always — before doing anything else

#### Process

1. Read the official Claude Code documentation on CLAUDE.md:
   **https://code.claude.com/docs/en/memory**

2. Read the file-type usage reference (`references/file-types.md` in this plugin).
   Contains: CLAUDE.md thinning principles, when to use rules vs skills vs hooks vs references,
   file type decision criteria, and JP/EN mirror rules.

→ Proceed to Step 1

---

### Step 1: Gather creation details

#### Condition

- Step 0 complete

#### Input

- User's description of what they want to create

#### Process

1. Ask the user for:
   - **Location** — project root (`CLAUDE.md`) or a specific subfolder (e.g., `src/CLAUDE.md`)?
   - **For root**: overall workflow steps, prohibitions, folder-scoped rule table entries
   - **For subfolder**: what files are in this folder, what are their roles, any local conventions
   - **Content overview** — what instructions or descriptions should be included?

→ Proceed to Step 2

#### Output

- Location (root or subfolder path), content overview

---

### Step 2: Validate against file-type guide

#### Condition

- Step 1 complete

#### Input

- Location and content collected in Step 1
- File-type guide (`references/file-types.md` in this plugin)

#### Process

1. Check whether the content truly belongs in CLAUDE.md:

   | If the content is… | Suggest |
   |---|---|
   | Single-folder conventions or descriptions | ✅ CLAUDE.md (subfolder) if co-location is preferred. `.claude/rules/` is also valid if auditability matters more |
   | Project-wide workflow or global conventions | ✅ CLAUDE.md (root) — correct choice |
   | Cross-path file sync ("edit X → also update Y, Z in different folders") | ⚠️ `.claude/rules/` is more appropriate |
   | A multi-step workflow with user interaction | ⚠️ `.claude/skills/` is more appropriate |
   | Mix of the above | ⚠️ Consider splitting across file types |

2. If the content fits CLAUDE.md → confirm and proceed
3. If a different file type is more appropriate → explain why and offer to redirect to `rule-creator` or `skill-creator`

→ Proceed to Step 3 if CLAUDE.md is confirmed appropriate

#### Output

- Confirmed: the content fits CLAUDE.md

#### Notes

##### Branching

- Rules fit better → explain and offer to switch to `rule-creator`
- Skill fits better → explain and offer to switch to `skill-creator`
- Mixed → suggest splitting: CLAUDE.md for the folder description part, rules/skills for the rest

---

### Step 3: Write CLAUDE.jp.md first

#### Condition

- Step 2 complete

#### Input

- Placement and content outline from Step 1

#### Process

1. Write `CLAUDE.jp.md` (or `<subfolder>/CLAUDE.jp.md`) in Japanese following the structure
   example in §References (not step-based — CLAUDE.md uses a description format, not a step format)
2. Keep the file under ~200 lines — move domain-specific content to `.claude/rules/` if needed

→ Proceed to Step 4

#### Output

- `CLAUDE.jp.md` written

#### Notes

##### Checklist

- [ ] Body written in Japanese — CLAUDE.jp.md is the Japanese human reference, not English
- [ ] Under ~200 lines (if longer, move domain-specific content to `.claude/rules/`)

---

### Step 4: Translate to CLAUDE.md (English)

#### Condition

- CLAUDE.jp.md written

#### Input

- CLAUDE.jp.md content

#### Process

1. Translate line-by-line to English
2. Write `CLAUDE.md` — the file Claude Code reads as directives
3. Keep heading structure identical to CLAUDE.jp.md

→ Proceed to Step 5

#### Output

- `CLAUDE.md` written

#### Notes

##### Checklist

- [ ] Body written in English (Claude Code reads this directly — no Japanese)
- [ ] Heading structure identical to CLAUDE.jp.md

---

### Step 5: Final verification

#### Condition

- Both files written

#### Process

1. Check that both files exist with matching structure
2. Confirm file is under ~200 lines
3. Present result to the user for review

#### Notes

##### Checklist

- [ ] `CLAUDE.md` — English, auto-loaded by Claude Code
- [ ] `CLAUDE.jp.md` — Japanese mirror, human reference only
- [ ] Matching heading structure
- [ ] Under ~200 lines

---

## References

### Required sections for CLAUDE.md

The same structure applies for both root and subfolder placements.

| Section | Content | Required |
|---|---|---|
| Title | H1 heading | Required |
| `## Overview` | Description of this project/folder | Required |
| `## Folder Structure` | Table of paths and their descriptions | Recommended |
| `## Constraints` | Rules Claude must always follow; prohibitions | Recommended |
| (Other sections) | Add freely as needed | Optional |

### Structure example

```markdown
# Project Name

## Overview

Description of this project/folder.

## Folder Structure

| Path | Overview |
|------|----------|
| `src/` | Implementation code |
| `docs/specs/` | Design specifications |
| `.claude/` | Claude Code configuration |

## Constraints

- Always run `npm test` before committing
- Never push directly to `main`

## {Additional sections (add freely as needed)}
```

### Official docs

- CLAUDE.md structure and placement: **https://code.claude.com/docs/en/memory**
