---
name: docs-manage
description: Manages project documentation with Issue-driven decision tracking. Always apply this skill when: working inside the wiki/ or docs/ folder, creating or updating home.md, adding issues to Issues.md, recording decisions in イシュー履歴.md, checking for document duplication, initializing project docs, or any request involving documentation organization, undecided matters, or decision history. Trigger immediately whenever the user mentions docs management, QA, decision tracking, document deduplication, or home.md updates — even if "docs" is not explicitly said.
---

# docs-manage — Project Documentation & Issue-Driven Decision Management

Manages the project wiki: initializes structure, tracks open issues, records decisions, and maintains a single source of truth across all documents.

---

## Overview

All project knowledge lives in `wiki/` (flat — no subdirectories):

```
wiki/
├── home.md            ← Navigation hub (links to all documents)
├── Issues.md          ← Open / undecided issues
├── イシュー履歴.md    ← Decision history log (append-only)
└── {feature}.md       ← Feature-specific documents
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
   | New project or `wiki/` does not exist | Step 2 (Initialize) |
   | Raise an undecided matter / question | Step 3 (Add Issue) |
   | Confirm a decision on an existing issue | Step 4 (Decide Issue) |
   | Document added, removed, or renamed | Step 5 (Update home.md) |
   | Write information to a wiki document | Step 6 (Duplicate check + write) |

→ Proceed to the appropriate step

#### Output

- Confirmed operation type

---

### Step 2: Initialize the wiki

#### Condition

- `wiki/` does not exist, or user wants to set up docs for a new project

#### Input

- Project root directory

#### Process

1. Glob-scan for existing `wiki/` to detect current state.
2. Create or update `wiki/home.md` — navigation hub with links to all docs.
3. Create `wiki/Issues.md` — open issues (empty if none yet).
4. Create `wiki/イシュー履歴.md` — decision history (empty if none yet).
5. Add a wiki link to the project root `README.md` (preserve all existing content).
6. Ask the user whether to append wiki operation rules to `CLAUDE.md`.

If `wiki/` already exists: diff against existing files and propose merging — do not overwrite without confirming.

→ Proceed to Step 6 to write files

#### Output

- `wiki/home.md`, `wiki/Issues.md`, `wiki/イシュー履歴.md` created or verified

---

### Step 3: Add a new issue

#### Condition

- User raises an undecided matter or question that needs a decision

#### Input

- User's description of the undecided matter

#### Process

1. Determine the next issue number:
   - Grep both `wiki/Issues.md` and `wiki/イシュー履歴.md` for `ISSUE-(\d+)`
   - Next number = max found + 1. Never reuse a number.
2. Draft the issue entry using the template in References.
3. For large issues with multiple sub-questions, use `### ISSUE-XXX-1`, `### ISSUE-XXX-2`.

→ Proceed to Step 6 to write files

#### Output

- New issue entry ready to append to `wiki/Issues.md`

---

### Step 4: Decide an issue

#### Condition

- User confirms a decision on an existing issue

#### Input

- Issue number or title
- The chosen option and rationale

#### Process

1. Identify the issue in `Issues.md` by number or title.
2. Determine the master document for the decision (see Master Document Principle in References).
3. Run a duplicate check (Step 6) before writing.
4. Prepare four concurrent writes (all delegated to background subagents):
   - **A** — Append the decision with rationale to the master feature document.
   - **B** — Remove the resolved issue from `wiki/Issues.md`.
   - **C** — Append a history entry to `wiki/イシュー履歴.md` (see template in References).
   - **D** — Update `wiki/home.md` links if a new document was created.

→ Proceed to Step 6 to write files

#### Output

- Decision recorded in master doc, issue removed from Issues.md, history entry appended

---

### Step 5: Update home.md

#### Condition

- A document was added, removed, or renamed in `wiki/`

#### Input

- Current state of `wiki/` directory

#### Process

1. Glob `wiki/` to get the current file list.
2. Diff against links currently in `home.md`.
3. Propose categorized sections (e.g., Features / Spec / API / Reference — adapt to the project).

→ Proceed to Step 6 to write files

#### Output

- Updated `home.md` link list ready

---

### Step 6: Duplicate check then write

#### Condition

- Any step that produces content to be written to `wiki/`

#### Input

- Target file and content to write

#### Process

1. Grep the target keyword across `wiki/` (full-text search).
2. If a duplicate is found:
   - Apply the Master Document Principle (see References) to determine the authoritative location.
   - In non-master documents, replace duplicated content with a reference link:
     ```markdown
     For details, see [Master Doc — Section](wiki/master.md#section)
     ```
   - After updating a master document, grep for old anchor names to find and fix stale references in other docs.
3. Delegate all file writes to background subagents (`run_in_background=true`):
   - Main session stays focused on decisions and communication with the user.
   - Subagents handle actual file writes in parallel without waiting for completion.
4. After each write, append or update the last-updated line at the bottom:
   ```markdown
   **Last updated**: YYYY-MM-DD — {one-line description of what changed}
   ```

→ Done

#### Output

- Files written, last-updated lines updated, duplicate check passed

#### Notes

##### Prohibitions

- Do not create subdirectories inside `wiki/`
- Do not write the same fact in multiple documents — one spec, one document
- Do not add a new document without also updating `home.md`
- Do not leave stale content — when a document is deleted, remove its `home.md` link
- Do not perform file writes in the main session — always delegate to background subagents

---

## References

### Issue entry template

```markdown
## ISSUE-XXX: {Title}  {未決定 | 検討中 | 保留}

**Background**: {why this issue matters}

**Options**:
- **A**: ...
- **B**: ...

**Recommended**: {A/B} — {reason}

**Related docs**: [{doc name}](wiki/{file}.md)
```

### Decision history template (append to `wiki/イシュー履歴.md`)

```markdown
## ISSUE-XXX: {Title}

- **Question**: {brief summary of the original issue}
- **Decision**: {chosen option and rationale, 1–3 lines}
- **Date**: YYYY-MM-DD
- **Written to**: [{doc name}](wiki/{file}.md#{section})

---
```

### Master Document Principle

| Information type | Master document |
|---|---|
| Feature spec | Feature-specific doc (e.g., `feature-x.md`) |
| Cross-feature common spec | `共通仕様.md` or equivalent |
| Undecided matters | `wiki/Issues.md` |
| Decided design with rationale | Feature-specific doc (not Issues.md) |
| API spec | Dedicated API doc |
| AI config / LLM roles | Dedicated AI config doc (if it exists) |

Non-master documents must reference the master via a link — never duplicate the content.

---

## Project Rule Deployment

**On first use in a project**, check if `.claude/rules/wiki-work.md` exists. If not, create it:

1. Check: `Glob(".claude/rules/wiki-work.md")` in the project root.
2. If missing, create `.claude/rules/wiki-work.md` with this content:

```markdown
---
paths:
  - "wiki/**/*.md"
---

# Wiki / Document Work

## Master Document Principle

One fact, one document. Before editing any wiki file, check whether the same content exists elsewhere. If it does, link instead of duplicating.

## Folder layout

- All wiki files live at the same level under `wiki/`. **No subfolders.**
- `wiki/home.md` is the navigation hub. Every doc must be linked from it.

## Adding / removing docs

- Creating a new wiki doc → add a link in `wiki/home.md`.
- Deleting a wiki doc → remove its link from `wiki/home.md` and any cross-references.

## Editing a wiki doc

Before writing, grep the keyword across `wiki/` to check for duplicates. If a duplicate exists, link from non-master docs to the master; never copy the content.

## Last-Updated tracking

After every document update (not initial creation), append or update at the bottom:

\`\`\`markdown
**Last updated**: YYYY-MM-DD — {one-line description of what changed}
\`\`\`

## What NOT to do

- Do not create subdirectories inside `wiki/`
- Do not write the same fact in multiple documents
- Do not add a new document without also updating `home.md`
```

3. Create `.claude/rules-jp/wiki-work.md` as a stub:

```markdown
> **このファイルは日本語ミラーです。本体は `.claude/rules/wiki-work.md`。**
```

4. Commit: `git add .claude/rules/ && git commit -m "chore: add wiki-work rule"`
