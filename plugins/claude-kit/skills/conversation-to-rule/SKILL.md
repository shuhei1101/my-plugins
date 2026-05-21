---
name: conversation-to-rule
description: |
  Analyze the current session's conversation history and generate path-scoped rules
  under .claude/rules/ based on discovered file relationships and project structure knowledge.
  Trigger when the user says "会話からルール作って", "今の作業をルール化して",
  or invoked explicitly as `/claude-kit:conversation-to-rule`.
---

# conversation-to-rule — Generate Rules from Conversation History

Looks back at the current session, extracts file dependency knowledge and folder structure
insights discovered during the work, and persists them as `.claude/rules/` path-scoped rules.

---

## Overview

During implementation and investigation, implicit knowledge accumulates:
"when touching this file, always check that one too" or "config lives over there."
This skill captures that knowledge as rules so future sessions load it automatically.

Two types of output are generated:
1. **File-link rules** — group interdependent files under `paths:` and prompt cross-checks on edit
2. **Folder structure index** — append path→role mappings to CLAUDE.md if not already documented

---

## Tasks

### Step 1: Analyze the conversation history

#### Condition

- Always — run first

#### Process

1. Review the entire conversation and extract:

   **A. File-link candidates**
   - Multiple files belonging to the same feature or domain (impl / test / config / spec)
   - Cases where editing one file required editing another
   - Any moment where a file relationship was noticed

   **B. Folder structure knowledge**
   - "Config lives here", "routing is here", "constants are here" — path roles discovered
   - Important directories or files found for the first time during this session

2. Build an internal list (report to user in the next step)

→ Proceed to Step 2

#### Output

- File-link candidate list
- Folder structure knowledge list

---

### Step 2: Confirm findings with the user

#### Condition

- Step 1 complete

#### Process

1. Present the extracted candidates:

   ```
   [File-link candidates]
   - src/models/user.py ↔ tests/test_user.py ↔ docs/specs/user.md
     Reason: model changes required test and spec updates

   [Folder structure knowledge]
   - Config: config/settings.yaml
   - Routing: src/routes/
   ```

2. Ask:
   - Should any candidates be removed?
   - Are there additional file links to add?
   - Any folder structure knowledge missing?

3. Apply user corrections and finalize the list

→ Proceed to Step 3

#### Output

- Finalized file-link groups (one or more)
- Finalized folder structure knowledge

---

### Step 3: Check for overlap with existing rules

#### Condition

- Step 2 complete

#### Process

1. Glob `.claude/rules/**/*.md` and read each file's `paths:` pattern
2. Check whether the files finalized in Step 2 are already covered by an existing rule
3. If overlap found:
   - Propose extending the existing rule instead of creating a new one
   - If user agrees, extend the existing rule (skip Step 4 for that domain)

→ Proceed to Step 4 (only if new rules are needed)

#### Output

- List of domains that need new rule files
- Extension content for existing rules (if any)

---

### Step 4: Launch `rule-creator` to write the rules

#### Condition

- Step 3 complete (new rules needed)

#### Process

1. Invoke the `claude-kit:rule-creator` skill
2. Pass the finalized file-link information as input:
   - Domain name (derived from conversation context)
   - File list (converted to glob patterns)
   - One-line domain description ("why these files must stay in sync")
3. Follow rule-creator's steps to create `.claude/rules/<name>.md` and `.claude/rules-jp/<name>.md`

→ Proceed to Step 5

#### Notes

##### References

- Follow the `claude-kit:rule-creator` skill procedure

---

### Step 5: Record folder structure index

#### Condition

- Folder structure knowledge was extracted in Step 2

#### Process

1. Read the project root `CLAUDE.md`
2. Check whether a `## Repository Structure` section exists:

   **Section exists:**
   - Compare existing content against the new knowledge
   - Append only what is missing (path roles not yet documented)
   - If the same content is already there, make no changes

   **Section does not exist:**
   - Append a new section to the end of `CLAUDE.md`:
     ```markdown
     ## Repository Structure

     | Path | Role |
     |---|---|
     | `config/settings.yaml` | Application configuration |
     | `src/routes/` | Route definitions |
     ```

3. If changes were made, report the diff to the user

→ Proceed to Step 6

#### Notes

##### Prohibitions

- Do not delete or overwrite existing content — append only
- Do not make any other changes to CLAUDE.md

---

### Step 6: Report results and propose a commit

#### Condition

- Steps 4 and 5 complete

#### Process

1. List all created and updated files
2. Ask the user whether to commit
3. If the user agrees, commit the changes

#### Output

- List of created / updated files
- Commit confirmation for the user

---

## References

### Required sections for rule files

| Section | Content | Required |
|---|---|---|
| `paths:` frontmatter | Glob patterns that trigger the rule | **Required** |
| `## Overview` | What domain this rule governs | Required |
| `## Related Files` | File paths and their roles | Recommended |
| `## When Editing` | Checklist when any file in the domain changes | Recommended |
| `## Rule Maintenance` | How to update the rule when files are added/removed | Recommended |

### Official docs

- Path-scoped rules: **https://code.claude.com/docs/en/memory**
