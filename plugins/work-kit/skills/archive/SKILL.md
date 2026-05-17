---
name: archive
description: |
  Archive completed PR entries from index.yaml to index.archive.yaml via a dedicated git branch.
  Trigger when the user says "アーカイブして", "index をアーカイブしたい", or invokes /work-kit:archive.
  Never invoke automatically — only when the user explicitly requests it.
---

# work-kit:archive — Archive Completed PR Entries

Moves completed (`completed: true`) entries from `index.yaml` to `index.archive.yaml`
and commits the result on a dedicated branch for the user to merge.

---

## Tasks

### Step 1: Check prerequisites

#### Condition

- Always — run first

#### Process

1. Verify that `.work/tasks/.gitignore` excludes only `index.yaml` (not `index.archive.yaml`)
2. Check whether `.work/` itself is gitignored:

```bash
git check-ignore -q .work/
```

   - Exit 0 (gitignored) → Report "Skipping archive: .work/ is excluded from the repository" and exit
   - Exit 1 (tracked) → Proceed to Step 2

→ Proceed to Step 2

---

### Step 2: Run the trim script

#### Process

1. Run trim to move completed entries to `index.archive.yaml`:

```bash
python plugins/work-kit/scripts/trim-index.py .work/tasks/index.yaml
```

2. If output is "Nothing to archive", report "No completed entries to archive" and exit

→ Proceed to Step 3

---

### Step 3: Create archive branch and commit

#### Process

1. Determine the branch name: `archive/trim-{YYYYMMDD}`
2. Create a worktree:

```bash
git worktree add -b archive/trim-{YYYYMMDD} ../$(basename $(pwd))-wt-archive
```

3. Copy `index.archive.yaml` into the worktree:

```bash
cp .work/tasks/index.archive.yaml ../$(basename $(pwd))-wt-archive/.work/tasks/index.archive.yaml
```

4. Commit inside the worktree:

```bash
cd ../$(basename $(pwd))-wt-archive
git add .work/tasks/index.archive.yaml
git commit -m "chore: archive completed PR entries to index.archive.yaml"
```

5. Remove the worktree (keep the branch):

```bash
git worktree remove ../$(basename $(pwd))-wt-archive
```

→ Proceed to Step 4

#### Notes

##### Prohibitions

- Never run `Remove-Item -Recurse` or `rm -rf` at the worktree root

---

### Step 4: Report completion

#### Process

1. Report:
   - Number of entries archived
   - Branch created: `archive/trim-{YYYYMMDD}`
2. Instruct the user to run `/work-kit:merge` to merge the archive branch
