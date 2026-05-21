---
name: rules-organizer
description: |
  Organize .claude/rules/ into subfolders by scanning the codebase.
  Trigger when the user says "rules フォルダを整理して", "ルールを整理して",
  ".claude/rules を整頓したい", "organize rules folder", or invoked explicitly
  as `/claude-kit:rules-organizer`.
---

# rules-organizer — Organize .claude/rules/ into subfolders

Scans `.claude/rules/` and the codebase, proposes a folder structure, gets user confirmation, then executes the reorganization.

---

## Overview

A generic skill applicable to any project.
`core/` and `feature/` are mandatory folders; additional folders are proposed based on the codebase.

---

## Tasks

### Step 1: Collect existing rules

#### Condition

- Always — run first

#### Process

1. List all flat `.md` files directly under `.claude/rules/`
2. If subfolders already exist, note the current folder structure
3. Read the first 30 lines of each rule file to understand its content

→ Proceed to Step 2

#### Output

- List of rule files to organize
- Existing folder structure (if any)

---

### Step 2: Scan the codebase

#### Condition

- Step 1 complete

#### Process

1. Check the following to understand the project's nature:
   - Presence of `package.json` / `pyproject.toml` / `Cargo.toml` etc.
   - Directory structure: `src/`, `app/`, `components/`, etc.
   - Whether frontend, backend, or infrastructure exists
2. Determine optional folder candidates based on findings

→ Proceed to Step 3

#### Output

- One-line project summary
- List of optional folder candidates

#### Notes

##### Optional folder decision guide

| Folder | When to add |
|---|---|
| `ui/` | Frontend exists (`components/`, `pages/`, `views/`, etc.) |
| `api/` | Backend API rules are substantial / `routes/` or `handlers/` exist |
| `infra/` | Many infrastructure, CI/CD, or deploy-related rules |

---

### Step 3: Propose the folder structure

#### Condition

- Step 2 complete

#### Process

1. Present the migration plan to the user in table form:

   | File (current) | Target folder | Reason |
   |---|---|---|
   | `conventions.md` | `core/` | Project-wide coding conventions |
   | `voice.md` | `feature/` | Voice feature domain knowledge |
   | `architecture.md` | `ui/` | UI architecture rules |
   | ... | ... | ... |

2. List all proposed folders (mandatory + optional)
3. Mention that an `_overview.md` will be generated in each folder

→ Wait for user confirmation

#### Output

- Migration plan table
- Folder list

#### Notes

##### About `_overview.md`

- An overview file placed at the root of each folder
- Describes the category's purpose and lists the rules it contains
- Do NOT name it `_index.md` — that implies a file index rather than a domain overview

---

### Step 4: Receive user confirmation and adjustments

#### Condition

- Proposal presented in Step 3

#### Process

1. Apply any reclassification changes the user requests
2. Rename folders if requested
3. Add or remove folders as needed
4. Once the user confirms ("looks good", "OK", etc.) → proceed to Step 5

→ Proceed to Step 5

#### Output

- Finalized migration plan

---

### Step 5: Execute

#### Condition

- User confirmed in Step 4

#### Process

1. Create all finalized folders
2. Move each file using `git mv`
3. Generate `_overview.md` in each folder:

   ```markdown
   # {folder-name} — {one-line category description}

   ## About this folder

   {1–3 sentences describing what rules belong here and why}

   ## Files

   | File | Description |
   |---|---|
   | `{file}.md` | {one-line description} |
   ```

4. Update the root `_overview.md` (or `_index.md` if it exists) to reflect the new structure

→ Proceed to Step 6

#### Notes

##### Prohibitions

- Use `git mv` not `cp` — preserve git history

---

### Step 6: Report results

#### Condition

- Step 5 complete

#### Process

1. Report the list of moved files
2. Report the list of generated `_overview.md` files
3. Suggest next actions to the user (e.g., review and commit)

---

## References

### Mandatory folder definitions

| Folder | Role | What goes in |
|---|---|---|
| `core/` | Project-wide foundation rules | Coding conventions, workflow, environment setup, development process |
| `feature/` | Feature-specific domain knowledge | Per-feature implementation rules, specs, design decisions (1 feature = 1 file) |
