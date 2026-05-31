---
name: plugin-migrate
description: |
  Bring the current project's plugin-generated artifacts in line with the currently installed
  plugin versions: sync work's `.work/.gitignore` files, remove legacy `.work/CLAUDE.md`, and
  migrate `index.yaml` to the latest schema. Other plugins' generated artifacts are out of scope
  unless they ship their own equivalent skill.
  Manual invocation only — use /work:plugin-migrate.
---

# work:plugin-migrate — Sync Plugin-Generated Artifacts to Latest Versions

Replaces the older `update` skill (PR168). Scope is **work's own static templates** only:
the `.work/` `.gitignore` files, removal of legacy `CLAUDE.md`, and `index.yaml` schema migration.

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

### Step 2: Remove legacy `.work/CLAUDE.md` and sync `.gitignore` files

#### Condition

- Step 1 complete

#### Process

1. If `.work/CLAUDE.md` exists, remove it with `git rm`
   - `.work/CLAUDE.md` was a static file that is now handled by ref-inject; it is no longer shipped in the template
   - If `.work/CLAUDE.jp.md` exists, remove it the same way
2. Write the following `.gitignore` files with the hardcoded content below (overwrite):
   - `.work/tasks/.gitignore` → content: `index.yaml`
   - `.work/issues/.gitignore` → content: `_index.yaml` (create `.work/issues/` first if it does not exist)
3. Report which files were changed

→ Proceed to Step 3

#### Output

- `.work/CLAUDE.md` / `.work/CLAUDE.jp.md` removed (if they existed)
- `.work/tasks/.gitignore`, `.work/issues/.gitignore` updated to the latest

---

### Step 3: Migrate `.work/tasks/index.yaml` to the branch-keyed schema

#### Condition

- Step 2 complete
- `.work/tasks/index.yaml` exists

#### Process

1. Read `.work/tasks/index.yaml` (and `.work/tasks/index.archive.yaml` if present)
2. If no entry has `id` or `tags` and there is no top-level `last_id` → already migrated, skip
3. Otherwise migrate to the branch-keyed schema:
   - Remove `id` and `tags` from every entry
   - Remove the top-level `last_id` key
   - Keep only `branch`, `title`, `type`, `summary`, `task`, `completed`
   - Apply the same normalization to `index.archive.yaml`
   - Write the updated file(s)

→ Proceed to Step 4

#### Output

- `index.yaml` (and `index.archive.yaml`) use the branch-keyed schema (no `id` / `last_id` / `tags`)
- If already migrated: report "index.yaml already uses the branch-keyed schema — skipped"

#### Notes

- The branch index is keyed by `branch`; there is no numeric `id` or `last_id`
- `index.yaml` is gitignored — no commit needed for it; `index.archive.yaml` is git-tracked
- The migration is idempotent — running it again after migration is a no-op

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
