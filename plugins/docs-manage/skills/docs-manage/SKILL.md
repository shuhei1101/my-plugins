---
name: docs-manage
description: Manages project documentation with QA-driven decision tracking. Always apply this skill when: working inside the docs/ folder, adding questions to docs/qa.md, recording decisions in docs/qa_history.md, checking for document duplication, initializing project docs, or any request involving documentation organization, undecided matters, or decision history. Trigger immediately whenever the user mentions docs management, QA, decision tracking, or document deduplication — even if "docs" is not explicitly said.
---

# docs-manage — Project Documentation & QA-Driven Decision Management

Manages project documentation: initializes structure, tracks open design questions, records decisions, and maintains a single source of truth across all spec documents.

---

## Overview

Documentation is organized into four areas under `docs/`:

```
docs/
├── specs/           ← Design and specification documents (flat — no subfolders)
├── qa.md            ← Open design questions (QA-XXX series)
├── qa_history.md    ← Resolved QA log (append-only)
└── incident.md      ← Incident log (INC-XXX series, optional)
```

**Core invariant:** One fact lives in exactly one document. Before writing, always check for duplicates.

---

## Tasks

### Step 1: Identify the operation

#### Condition

- Always — before doing anything else

#### Process

1. Determine what the user is requesting:

   | User request | Go to |
   |---|---|
   | New project or `docs/` does not exist | Step 2 (Initialize) |
   | Raise an undecided matter / design question | Step 3 (Add QA entry) |
   | Confirm a decision on an existing QA entry | Step 4 (Close QA entry) |
   | Write information to a spec document | Step 5 (Duplicate check + write) |

→ Proceed to the appropriate step

#### Output

- Confirmed operation type

---

### Step 2: Initialize the docs structure

#### Condition

- `docs/` does not exist, or user wants to set up documentation for a new project

#### Input

- Project root directory

#### Process

1. Glob-scan for existing `docs/` to detect current state.
2. Create `docs/qa.md` — open design questions (empty if none yet; see template in References).
3. Create `docs/qa_history.md` — resolved QA log (empty if none yet).
4. Optionally create `docs/incident.md` — incident log (create only if the project needs it).
5. Add a docs link to the project root `README.md` (preserve all existing content).

If `docs/` already exists: diff against existing files and propose merging — do not overwrite without confirming.

→ Proceed to Step 5 to write files

#### Output

- `docs/qa.md`, `docs/qa_history.md` created or verified

---

### Step 3: Add a new QA entry

#### Condition

- User raises an undecided matter or design question that needs a decision

#### Input

- User's description of the undecided matter

#### Process

1. Determine the next QA number:
   - Grep both `docs/qa.md` and `docs/qa_history.md` for `QA-(\d+)`
   - Next number = max found + 1. Never reuse a number.
2. Draft the QA entry using the template in References.
3. Key rules for the QA entry:
   - The `推奨方式` (recommended approach) field is **mandatory** — always pick one option with a 1–2 line reason. Hedging like "user decides" is forbidden.
   - Heading must end with the literal token `未決定`: `## QA-XXX: {title} 未決定`
   - For deferred entries (to decide later), append `（後で）`: `未決定（後で）`
   - Multiple sub-questions → split into `### QA-XXX-1`, `### QA-XXX-2` sub-sections
4. **Always append new entries to the bottom** of `docs/qa.md` to preserve chronological order.

→ Proceed to Step 5 to write files

#### Output

- New QA entry appended to the bottom of `docs/qa.md`

---

### Step 4: Close a QA entry

#### Condition

- User confirms a decision on an existing QA entry

#### Input

- QA number or title
- The chosen option and rationale

#### Process

1. Identify the QA entry in `docs/qa.md` by number or title.
2. Determine the master spec document where the decision should be written (see Master Document Principle in References).
3. Run a duplicate check (Step 5) before writing.
4. Prepare three concurrent writes (delegate to background subagents):
   - **A** — Apply the decision to the target spec document in `docs/specs/`.
   - **B** — Delete the entire QA block from `docs/qa.md`. No partial residue, no "decided" markers — remove the entry completely.
   - **C** — Append a summary entry to the bottom of `docs/qa_history.md` (see template in References).

→ Proceed to Step 5 to write files

#### Output

- Decision applied to the spec document, QA entry removed from qa.md, history entry appended to qa_history.md

#### Notes

##### Prohibitions

- Do not write only to `qa_history.md` without also updating the target spec document — both must happen together

---

### Step 5: Duplicate check then write

#### Condition

- Any step that produces content to be written to `docs/`

#### Input

- Target file and content to write

#### Process

1. Grep the target keyword across `docs/specs/` (full-text search).
2. If a duplicate is found:
   - Apply the Master Document Principle (see References) to determine the authoritative location.
   - In non-master documents, replace duplicated content with a reference link:
     ```markdown
     For details, see [Master Doc — Section](docs/specs/master.md#section)
     ```
   - After updating a master document, grep for old anchor names to fix stale references in other docs.
3. Delegate all file writes to background subagents (`run_in_background=true`):
   - Main session stays focused on decisions and communication with the user.
   - Subagents handle actual file writes in parallel without waiting for completion.
4. After updating a spec document (not on initial creation), append or update the last-updated line at the bottom:
   ```markdown
   **Last updated**: YYYY-MM-DD — {one-line description of what changed}
   ```

→ Done

#### Output

- Files written, last-updated lines updated, duplicate check passed

#### Notes

##### Prohibitions

- Do not create subfolders inside `docs/specs/` — all spec files live flat at the same level
- Do not write the same fact in multiple documents — one spec, one document
- Do not leave TBD / 要検討 / 後で決める markers inside spec bodies — file a QA entry instead, and leave only a link in the spec body

---

## References

### QA entry template (`docs/qa.md`)

```markdown
## QA-XXX: {title} 未決定

**背景**: {why this decision is needed, with links to related docs}.

### QA-XXX-1: {sub-question summary}

| 案 | 内容 |
|---|---|
| A | {description of option A} |
| B | {description of option B} |

**推奨方式**: {A / B / C} — {1–2 line rationale}

**決定したら**: {target spec document / section to update}

---
```

### QA history entry template (append to `docs/qa_history.md`)

```markdown
## QA-XXX: {title}

- **質問内容**: {brief summary of the original question, 1–2 lines}
- **決定した内容**: {chosen option and rationale, 1–3 lines}
- **決定日**: YYYY-MM-DD
- **転記先**: [{doc name}](docs/specs/{file}.md#{section})

---
```

### Master Document Principle

| Information type | Master document |
|---|---|
| Feature spec | Feature-specific doc in `docs/specs/` |
| Cross-feature common spec | `共通仕様.md` or equivalent |
| Open design questions | `docs/qa.md` |
| Decided design with rationale | Feature-specific spec doc (not qa.md) |
| API spec | Dedicated API spec doc |

Non-master documents must reference the master via a link — never duplicate the content.

---

## Project Rule Deployment

**On first use in a project**, check if `.claude/rules/specs-work.md` exists. If not, create it:

1. Check: `Glob(".claude/rules/specs-work.md")` in the project root.
2. If missing, create `.claude/rules/specs-work.md` with this content:

```markdown
---
paths:
  - "docs/specs/**/*.md"
  - "docs/qa.md"
  - "docs/qa_history.md"
---

# Spec / Document Work

## Master Document Principle

One fact, one document. Before editing any spec file, check whether the same content exists elsewhere. If it does, link instead of duplicating.

## Folder layout

- All spec files live at the same level under `docs/specs/`. **No subfolders.**

## Open questions → docs/qa.md

While editing a spec, if anything is not yet decided, add a QA entry to `docs/qa.md` immediately. Never leave TBD / 要検討 markers inside the spec body — leave only a link: `[QA-XXX](docs/qa.md#qa-xxx) で検討中`.

## Closing a QA entry

1. Apply the decision to the target spec document.
2. Delete the entire QA block from `docs/qa.md`.
3. Append a summary to `docs/qa_history.md`.
```

3. Create `.claude/rules-jp/specs-work.md` as a stub:

```markdown
> **このファイルは日本語ミラーです。本体は `.claude/rules/specs-work.md`。**
```

4. Commit: `git add .claude/rules/ && git commit -m "chore: add specs-work rule"`
