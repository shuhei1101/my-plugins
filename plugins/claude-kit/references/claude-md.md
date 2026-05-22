# CLAUDE.md Design Guide

Reference for designing, creating, and evaluating `CLAUDE.md` and `CLAUDE.jp.md` files.
Japanese mirror: `references/claude-md.jp.md`

---

## When it loads

| Placement | When loaded |
|---|---|
| Project root | At every session start — always loaded |
| Subfolder | Lazily, when Claude reads any file in that folder or its subfolders |

---

## Important: keep it thin

The root CLAUDE.md is **loaded on every session** — the more content it has, the more context it consumes.

### Extraction destination guide

| Content nature | Action |
|---|---|
| Needed only when specific files are edited | Move to `.claude/rules/` |
| Multi-step workflow or procedure | Move to `.claude/skills/` |
| Relevant only to a specific folder | Move to that subfolder's `CLAUDE.md` |
| Detailed explanation or reference (read occasionally) | Move to `.claude/references/`; write only the path in CLAUDE.md |
| Spec or doc already in the project | Write only the path; do not duplicate content |

---

## About `.claude/references/`

A place for content that belongs in CLAUDE.md conceptually but does not need to be loaded every session.
Write only the file path in CLAUDE.md — Claude reads the file when it actually needs it.

---

## Required sections

| Section | Content | Required |
|---|---|---|
| Title | H1 heading | Required |
| `## Overview` | Project or folder description | Required |
| `## Folder structure` | Path-to-summary table | Recommended |
| `## Constraints` | Rules and prohibitions Claude must always follow | Recommended |

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

---

## Line count guideline

- Target under 200 lines for root CLAUDE.md
- If it exceeds 200 lines, extract domain-specific content to `.claude/rules/`
