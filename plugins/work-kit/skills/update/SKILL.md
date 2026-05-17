---
name: update
description: |
  Sync the current project's .work/ directory with the latest work-kit templates.
  Manual invocation only — use /work-kit:update.
---

# work-kit:update — Sync .work/ with Latest Templates

Applies the latest work-kit templates to an already-initialized `.work/` directory.
Update strategy differs by file type:

- **CLAUDE.md / CLAUDE.jp.md** — direct overwrite from template
- **tasks/.gitignore** — direct overwrite from template
- **QA.md / TODO.md templates** — agent reads both and applies only structural/format changes; existing content is never overwritten

---

## Tasks

### Step 1: Locate templates and verify .work/ exists

#### Condition

- Always — run first

#### Process

1. Identify the template directory:
   - `${CLAUDE_PLUGIN_DIR}/templates/.work/`
2. Check that `.work/` exists in the current project
3. If absent, tell the user to run `/work-kit:setup` first and exit

→ Proceed to Step 2

#### Output

- Template dir and current `.work/` both confirmed

---

### Step 2: Overwrite CLAUDE.md and CLAUDE.jp.md

#### Condition

- Step 1 complete

#### Process

1. Copy `CLAUDE.md` from the template to `.work/CLAUDE.md` (overwrite)
2. Copy `CLAUDE.jp.md` from the template to `.work/CLAUDE.jp.md` (overwrite)

#### Output

- `.work/CLAUDE.md` — updated to latest
- `.work/CLAUDE.jp.md` — updated to latest

---

### Step 3: Sync .gitignore

#### Condition

- Step 2 complete

#### Process

1. Copy `tasks/.gitignore` from the template to `.work/tasks/.gitignore` (overwrite)
2. Create the file if it does not exist

#### Output

- `.work/tasks/.gitignore` — updated to latest (or created)

---

### Step 4: Migrate index.yaml — add last_id if missing

#### Condition

- Step 3 complete
- `.work/tasks/index.yaml` exists

#### Process

1. Read `.work/tasks/index.yaml`
2. If `last_id` field is already present → skip this step
3. If `last_id` is absent:
   - Compute `last_id` = `max(id)` across all entries in the `prs` list (0 if empty)
   - Add `last_id: {N}` to the top of the `prs` section
   - Write the updated file

#### Output

- `last_id` present in `.work/tasks/index.yaml`
- If already present: report "index.yaml already has last_id — skipped"

#### Notes

- `index.yaml` is gitignored — no commit needed

---

### Step 5: Diff and patch QA.md files

#### Condition

- Step 4 complete

#### Process

1. Read the template at `tasks/yyyymmdd_xxx/PRXXX/QA.md`
2. Find all existing `QA.md` files under `.work/tasks/**/QA.md`
3. Identify additions or changes in the template's header, preamble, or operational guidelines
4. For each QA.md:
   - Apply only structural/format changes from the template
   - Never touch existing QA-XXX entries

#### Output

- If changes applied: list of updated files and what changed
- If up to date: report "QA.md files are up to date"

---

### Step 6: Diff and patch TODO.md files

#### Condition

- Step 5 complete

#### Process

1. Read the template at `tasks/yyyymmdd_xxx/PRXXX/TODO.md`
2. Find all existing `TODO.md` files under `.work/tasks/**/TODO.md`
3. Identify additions or changes in the template's section structure or headers
4. For each TODO.md:
   - Apply only structural/format changes from the template
   - Never touch existing task content (checklists, descriptions)

#### Output

- If changes applied: list of updated files and what changed
- If up to date: report "TODO.md files are up to date"

---

### Step 7: Report completion

#### Process

1. List all updated files
2. Report completion to the user
