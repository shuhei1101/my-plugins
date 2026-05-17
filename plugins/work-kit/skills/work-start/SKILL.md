---
name: work-start
description: |
  Start a new PR: determine PR number, collect details, add index.yaml entry in main repo,
  create worktree, then create all task documents INSIDE the worktree.
  Trigger when the user says "新しい PR を作って", "新しい作業を始めたい", "work-start して",
  "start new work", or "create a new PR".
---

# work-kit:work-start — Start a New PR

Creates the worktree first, then creates all task documents inside it.
This prevents task documents from being created in the main repository.

---

## Tasks

### Step 1: Determine the next PR number

#### Condition

- Always — run first

#### Process

1. If the user has already specified a PR number or branch name, use that value
2. Otherwise run the following command and use the printed number:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py next-id .work/tasks/index.yaml
```

→ Proceed to Step 2

#### Output

- Next PR number confirmed

---

### Step 2: Collect request details

#### Condition

- Step 1 complete

#### Process

1. Determine the following:
   - **Title**: short kebab-case label used in the folder name
   - **Type**: `feat` / `fix` / `refactor` / `docs` / `chore` / `test`
   - **TODO list**: what will be done this PR (becomes the checklist)
   - **Spec**: does a related spec exist in `.work/specs/`? Or does one need to be created?
   - **Open questions**: anything unclear or undecided

→ Proceed to Step 3

#### Output

- Title, type, TODO list, spec info, and open questions confirmed

---

### Step 3: Add entry to index.yaml (main repository)

#### Condition

- Step 2 complete

#### Process

1. Run the following command to add the new PR entry:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py add .work/tasks/index.yaml \
  --id {N} \
  --title "PR{N} — {title}" \
  --type {type} \
  --summary "{summary}" \
  --task "{YYYYMMDD}_{title}"
```

→ Proceed to Step 4

#### Output

- `.work/tasks/index.yaml` updated with the new PR entry and `last_id` (main repository)

#### Notes

- `index.yaml` is excluded by `.work/tasks/.gitignore` — no commit to master is needed

---

### Step 4: Create the worktree and branch

#### Condition

- Step 3 complete

#### Process

1. Create the worktree:

```bash
git worktree add -b PR{N}/{type}/{title} ../$(basename $(pwd))-wt-PR{N}
```

→ Proceed to Step 5

#### Output

- Worktree created at `../repo-wt-PR{N}`
- Branch `PR{N}/{type}/{title}` exists

#### Notes

##### Prohibitions

- Never commit directly to master/main

---

### Step 5: Create task folder, PR folder, TODO.md, and QA.md (inside worktree)

#### Condition

- Step 4 complete

#### Process

All files must be created **inside the worktree (`../repo-wt-PR{N}/`)**, not the main repository.

1. Create `../repo-wt-PR{N}/.work/tasks/{YYYYMMDD}_{title}/`
2. Create `../repo-wt-PR{N}/.work/tasks/{YYYYMMDD}_{title}/PR{N}/`
3. Create `TODO.md` using the template at `.work/tasks/yyyymmdd_xxx/PRXXX/TODO.md`
4. Create `QA.md` using the template at `.work/tasks/yyyymmdd_xxx/PRXXX/QA.md`

→ Proceed to Step 6

#### Output

- `../repo-wt-PR{N}/.work/tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md` created
- `../repo-wt-PR{N}/.work/tasks/{YYYYMMDD}_{title}/PR{N}/QA.md` created

---

### Step 6: Maintain the spec document (inside worktree)

#### Condition

- Step 5 complete

#### Process

1. Check `.work/specs/` inside the worktree for a related spec
2. If found → update the relevant sections for this PR
3. If not found → create a new spec using the template at `.work/specs/xxx.md`
4. Add a link to the spec in TODO.md's `## 仕様参照` section

→ Proceed to Step 7

---

### Step 7: Record open questions in QA.md (inside worktree)

#### Condition

- Step 6 complete

#### Process

1. Append any open questions from Step 2 to `PR{N}/QA.md` inside the worktree as QA-XXX entries
2. Skip if there are no open questions

→ Proceed to Step 8

---

### Step 8: Commit created content, report to user, then start implementation

#### Process

1. Commit all created files inside the worktree (branch: `PR{N}/{type}/{title}`)
2. Report what was created: branch name, worktree path, TODO.md path, spec path
3. Start implementation:
   - **If QA entries exist** → ask the user for confirmation before starting
   - **If no QA entries** → proceed with implementation immediately

#### Notes

##### Prohibitions

- Never commit to anywhere other than the created worktree (`PR{N}/{type}/{title}` branch)

##### Commit granularity

- Commit in meaningful units that are easy for the user to understand
- Do not split commits too finely
- Do not mix planning documents (TODO, specs, etc.) and implementation code in the same commit
