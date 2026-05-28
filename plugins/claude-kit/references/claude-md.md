# CLAUDE.md Authoring Guide

How to design, create, and evaluate `CLAUDE.md` (and its `CLAUDE.jp.md` mirror) for a project or
subfolder. This guide is self-contained: when injected (because you are editing a `CLAUDE.md`),
follow it to author the file directly. Read `common.md` alongside it.
Japanese mirror: `references/claude-md.jp.md`

---

## When it loads

| Placement | When loaded |
|---|---|
| Project root | At every session start — always loaded |
| Subfolder | Lazily, when Claude reads any file in that folder or its subfolders |

**Root** CLAUDE.md defines the overall project workflow, commit rules, server management, and the
folder-scoped rule table. **Subfolder** CLAUDE.md describes that folder's contents and local
conventions, giving Claude context without loading it every session.

---

## Important: keep it thin

The root CLAUDE.md is loaded on **every** session — the more content, the more context it consumes.

### Extraction destination guide

| Content nature | Action |
|---|---|
| Needed only when specific files are edited | Move to `.claude/rules/` |
| Multi-step workflow or procedure | Move to `.claude/skills/` |
| Relevant only to a specific folder | Move to that subfolder's `CLAUDE.md` |
| Detailed explanation/reference (read occasionally) | Move to `.claude/references/`; write only the path in CLAUDE.md |
| Spec/doc already in the project | Write only the path; do not duplicate content |

### Line count guideline

- Target under 200 lines for the root CLAUDE.md
- If it exceeds 200 lines, extract domain-specific content to `.claude/rules/`

---

## Authoring workflow

### Step 1 — Gather details

- **Location** — project root (`CLAUDE.md`) or a subfolder (e.g. `src/CLAUDE.md`)?
- **For root**: overall workflow steps, prohibitions, folder-scoped rule table entries
- **For subfolder**: what files are in the folder, their roles, local conventions
- **Content overview** — what instructions/descriptions to include

### Step 2 — Validate that CLAUDE.md is the right type

| If the content is… | Verdict |
|---|---|
| Project-wide workflow or global conventions | ✅ CLAUDE.md (root) — correct |
| Single-folder conventions/descriptions | ✅ CLAUDE.md (subfolder) for co-location; `.claude/rules/` if auditability matters more |
| Cross-path file sync ("edit X → also update Y, Z elsewhere") | ⚠️ `.claude/rules/` |
| A multi-step workflow with user interaction | ⚠️ `.claude/skills/` |
| Mix | ⚠️ Split across file types |

### Step 3 — Write `CLAUDE.jp.md` first, then translate

CLAUDE.md uses a **description format, not a step format**. Author `CLAUDE.jp.md` in Japanese first,
keep it under ~200 lines (extract domain content to `.claude/rules/` if longer), then produce the
English `CLAUDE.md` (by hand or via the `jp-mirror-translator` agent). Stamp both (see `common.md`).

---

## About `.claude/references/`

For content that conceptually belongs in CLAUDE.md but does not need loading every session.
Write only the file path in CLAUDE.md — Claude reads the file when it actually needs it.

---

## Required sections

| Section | Content | Required |
|---|---|---|
| Title | H1 heading | Required |
| `## Overview` | Project/folder description | Required |
| `## Folder structure` | Path-to-summary table | Recommended |
| `## Constraints` | Rules and prohibitions Claude must always follow | Recommended |
| (Other sections) | Add freely as needed | Optional |

---

## Structure example

```markdown
# Project Name

## Overview
Description of this project or folder.

## Folder structure

| Path | Summary |
|------|---------|
| `src/` | Implementation code |
| `docs/specs/` | Specification documents |
| `.claude/` | Claude Code configuration |

## Constraints

- Always run `npm test` before committing
- Never push directly to `main`
```

---

## Subfolder CLAUDE.md vs rules

| Priority | Choice |
|---|---|
| **Keep rules co-located with the code** (proximity) | Subfolder `CLAUDE.md` |
| **See all active rules in one place** (auditability) | `.claude/rules/<name>.md` |

Cross-path linking always belongs in `.claude/rules/`.
