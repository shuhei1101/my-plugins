---
name: plugin-migrate
description: |
  Bring the current project's plugin-generated artifacts in line with the currently installed
  plugin versions: overwrite work's static `.work/` templates (CLAUDE.md, .gitignore) and
  migrate `index.yaml` to the latest schema. Other plugins' generated artifacts are out of scope
  unless they ship their own equivalent skill.
  Manual invocation only — use /work:plugin-migrate.
---

# work:plugin-migrate — Sync Plugin-Generated Artifacts to Latest Versions

Replaces the older `update` skill (PR168). Scope is **work's own static templates** only:
the `.work/` CLAUDE.md, `.gitignore` files, and `index.yaml` schema migration.

Per-plugin diff logic for *other* plugins is intentionally out of scope here — each plugin
owns its own update path and ships its own equivalent skill if needed (e.g. a hypothetical
`/{plugin}:plugin-migrate`). This skill never reaches across plugin boundaries.

---

## Tasks

### Step 1: Verify .work/ exists and prepare a working branch

#### Condition

- Always — run first

#### Process

1. Check that `.work/` exists in the current project
2. If absent, tell the user to run `/work:setup` first and exit
3. Invoke `/work:start` to create a working branch dedicated to this sync
   (so the generated edits land on a reviewable branch, not master)
4. Wait until the worktree and branch are created

→ Proceed to Step 2

#### Output

- `.work/` confirmed; working branch / worktree ready
- All subsequent file edits and commits in later steps happen inside this worktree on the working branch

---

### Step 2: Overwrite workspace templates inside `.work/`

#### Condition

- Step 1 complete

#### Process

1. Locate the work plugin template root: `${CLAUDE_PLUGIN_ROOT}/templates/.work/`
2. Copy the following files from the template into the project (overwrite):
   - `CLAUDE.md` → `.work/CLAUDE.md`
   - `CLAUDE.jp.md` → `.work/CLAUDE.jp.md`
   - `tasks/.gitignore` → `.work/tasks/.gitignore`
   - `issues/.gitignore` → `.work/issues/.gitignore` (if present in the template)
3. Report which files were overwritten

→ Proceed to Step 3

#### Output

- `.work/CLAUDE.md`, `.work/CLAUDE.jp.md`, `.work/tasks/.gitignore` updated to the latest

---

### Step 3: Migrate `.work/tasks/index.yaml` (add `last_id` if missing)

#### Condition

- Step 2 complete
- `.work/tasks/index.yaml` exists

#### Process

1. Read `.work/tasks/index.yaml`
2. If `last_id` is already present → skip this step
3. If `last_id` is absent:
   - Compute `last_id` = `max(id)` across all entries (0 if empty)
   - Add `last_id: {N}` to the top of the index file
   - Write the updated file

→ Proceed to Step 4

#### Output

- `last_id` present in `index.yaml`
- If already present: report "index.yaml already has last_id — skipped"

#### Notes

- `index.yaml` is gitignored — no commit needed for it
- This is the only schema migration this skill performs; deeper rewrites belong in dedicated
  one-off scripts shipped alongside the breaking version bump

---

### Step 4: Review and commit

#### Condition

- Step 3 complete

#### Process

1. Show the user `git status` and `git diff` of the worktree
2. Commit grouped changes with a descriptive message:
   - `chore: sync work .work/ templates to v{version}`

→ Proceed to Step 5

---

### Step 5: Report completion

#### Process

1. List every file that was updated
2. If no files changed, report "All work plugin artifacts already up to date"
3. Suggest the user run `/work:merge` to merge the sync branch when ready

→ Done
