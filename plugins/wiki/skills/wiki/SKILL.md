---
name: wiki
description: Manages project documentation using a Wiki structure with Issue-driven decision tracking. Always apply this skill when: working inside the wiki/ folder, creating or updating wiki/home.md, adding issues to wiki/Issues.md, recording decisions in wiki/イシュー履歴.md, checking for document duplication, initializing a project wiki, or any request involving documentation organization, undecided matters, or decision history. Trigger immediately whenever the user mentions wiki management, Issues.md, decision tracking, document deduplication, or home.md updates — even if "wiki" is not explicitly said.
---

# Wiki — Project Documentation & Issue-Driven Decision Management

## Folder Structure

```
wiki/
├── home.md            ← Navigation hub (links to all documents)
├── Issues.md          ← Open / undecided issues
├── イシュー履歴.md    ← Decision history log (append-only)
└── {feature}.md       ← Feature-specific documents (flat, no subdirs)
```

**Invariants:**
- All documents live directly under `wiki/` — never create subdirectories
- `home.md` must be updated whenever a document is added or removed
- `Issues.md` holds only unresolved issues; decided ones move to `イシュー履歴.md`

---

## Initializing the Wiki

When creating a wiki for a new or existing project:

1. Glob-scan for existing `wiki/` to detect current state
2. Create (or update) `wiki/home.md` — navigation hub with links to all docs
3. Create `wiki/Issues.md` — open issues (empty if none yet)
4. Create `wiki/イシュー履歴.md` — decision history (empty if none yet)
5. Add a wiki entry link to the project root `README.md` (preserve all existing content)
6. Optionally append wiki operation rules to `CLAUDE.md` (ask the user)

If `wiki/` already exists, diff against existing files and propose merging — do not overwrite without confirming.

---

## Adding a New Issue

When the user raises an undecided matter or a question that needs a decision:

1. Determine the next issue number by grepping both `wiki/Issues.md` and `wiki/イシュー履歴.md` for `ISSUE-(\d+)`. Next number = max + 1. Never reuse a number.
2. Append to `wiki/Issues.md`:

```markdown
## ISSUE-XXX: {Title}  {未決定 | 検討中 | 保留}

**Background**: {why this issue matters}

**Options**:
- **A**: ...
- **B**: ...

**Recommended**: {A/B} — {reason}

**Related docs**: [{doc name}](wiki/{file}.md)
```

For large issues with multiple sub-questions, use `### ISSUE-XXX-1`, `### ISSUE-XXX-2`.

---

## Deciding an Issue

When the user confirms a decision:

1. Identify the issue in `Issues.md` by number or title
2. Determine the master document for the decision (see Master Document Principle below)
3. Run a duplicate check before writing (see Duplicate Check Rules below)
4. Delegate all file writes to background subagents in parallel:

   - **A** — Append the decision (with rationale) to the master feature document
   - **B** — Remove the resolved issue from `wiki/Issues.md`
   - **C** — Append to the bottom of `wiki/イシュー履歴.md`:

     ```markdown
     ## ISSUE-XXX: {Title}

     - **Question**: {brief summary of the original issue}
     - **Decision**: {chosen option and rationale, 1–3 lines}
     - **Date**: YYYY-MM-DD
     - **Written to**: [{doc name}](wiki/{file}.md#{section})

     ---
     ```

   - **D** — Update `wiki/home.md` links if a new document was created

---

## Checking for Duplicates

Before writing any information to a document:

1. Grep the target keyword across `wiki/` (full-text search)
2. If duplicate found, apply the Master Document Principle to determine the authoritative location
3. In non-master documents, replace duplicated content with a reference link:

```markdown
For details, see [Master Doc — Section](wiki/master.md#section)
```

After updating a master document, grep for the old anchor/section name to find and fix stale references in other docs.

**Bad** (same spec duplicated):
```markdown
# 共通仕様.md
## Failure threshold: STT: 3, TTS: 2

# feature-x.md
## Failure threshold: STT: 3, TTS: 2   ← duplicate
```

**Good** (single source of truth):
```markdown
# 共通仕様.md  ← master
## Failure threshold: STT: 3, TTS: 2

# feature-x.md
For thresholds, see [共通仕様.md — Failure threshold](共通仕様.md#failure-threshold)
```

---

## Updating home.md

When documents are added, removed, or renamed:

1. Glob `wiki/` to get the current file list
2. Diff against links currently in `home.md`
3. Propose categorized sections (e.g., Features / Spec / API / Reference — adapt to the project)
4. Delegate the rewrite to a background subagent

---

## Master Document Principle

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

## Last-Updated Tracking

After every document update (not on initial creation), append or update this line at the bottom:

```markdown
**Last updated**: YYYY-MM-DD — {one-line description of what changed}
```

Examples:
```
**Last updated**: 2026-04-27 — Added hot-reload/restart classification per ISSUE-029
**Last updated**: 2026-04-27 — Changed T2 from parallel to single call (sections 3 & 4)
```

This allows a separate AI session to immediately understand when and why a file was last changed.

---

## Subagent Delegation for File Writes

All file writes (document creation, updates, appends) must be delegated to background subagents:

- Main session: focuses on decisions, analysis, and communicating with the user
- Subagents: handle actual file writes in the background (`run_in_background=true`)
- Do not wait for subagent completion before continuing to the next task

Subagent instruction template:
```
Task: {which file to write and what content}

Content:
{specific content in heredoc format}

Rules:
1. Grep wiki/ for duplicates before writing
2. Apply Master Document Principle if duplicates found
3. Update wiki/home.md if a new document was created
4. Update the **Last updated** line at the bottom
5. Report what was updated (1–3 lines) when done
```

---

## What NOT to Do

- Do not create subdirectories inside `wiki/`
- Do not write the same decision in multiple documents — one spec, one document
- Do not add a new document without also updating `home.md`
- Do not leave stale content — when a document is deleted, remove its `home.md` link
- Do not perform file writes synchronously in the main session — always delegate to background subagents
