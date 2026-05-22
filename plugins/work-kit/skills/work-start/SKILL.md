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

### Step 4: Create the worktree and branch (via worktree-kit)

#### Condition

- Step 3 complete

#### Process

1. **If `worktree-kit` is installed**: invoke `/worktree-kit:work-add` with the PR number and branch:

   > `/worktree-kit:work-add PR{N} {type}/{title}`

2. **If `worktree-kit` is NOT installed**: skip worktree creation and notify the user:

   > ⚠️ worktree-kit がインストールされていないため、ワークツリーの作成をスキップします。  
   > `.work/` フォルダ管理のみで作業を続けます。  
   > ワークツリーを使用したい場合は `worktree-kit` プラグインをインストールしてください。

→ Proceed to Step 5

#### Output

- (worktree-kit present) Worktree created at `../repo-wt-PR{N}`, branch `PR{N}/{type}/{title}` exists
- (worktree-kit absent) No worktree; proceed with `.work/` folder management only

#### Notes

##### Prohibitions

- Never commit directly to master/main

---

### Step 5: Determine the task folder (autonomous judgment)

#### Condition

- Step 4 complete

#### Process

1. Read all folder names under `.work/tasks/` in the worktree
2. Compare each folder name (`YYYYMMDD_title` format) against the purpose of this PR and decide:
   - **Add to existing folder**: an existing folder covers the same goal or feature area, and this PR fits naturally as part of it
     - Examples: splitting a feature across multiple PRs, a follow-up fix, related refactoring
   - **Create new folder**: no existing folder is closely related, or `.work/tasks/` is empty
3. Confirm the argument to pass to the next step:
   - Adding to existing → use `--task-dir {folder_name}`
   - Creating new → use `--date {YYYYMMDD} --title {title}`

→ Proceed to Step 6

#### Output

- Task folder strategy (new or existing) and the arguments to use are confirmed

#### Notes

- Do not ask the user — decide autonomously based on content
- When in doubt, create a new folder (folders can be consolidated later)

---

### Step 6: Create PR folder, TODO.md, and QA.md (inside worktree)

#### Condition

- Step 5 complete

#### Process

Run one of the following depending on the choice in Step 5:

**New task folder:**

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/setup-task.py \
  ../$(basename $(pwd))-wt-PR{N} \
  --pr {N} \
  --title {title} \
  --date {YYYYMMDD} \
  --plugin-root ${CLAUDE_PLUGIN_ROOT}
```

**Add to existing task folder:**

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/setup-task.py \
  ../$(basename $(pwd))-wt-PR{N} \
  --pr {N} \
  --task-dir {existing_folder_name} \
  --title {title} \
  --plugin-root ${CLAUDE_PLUGIN_ROOT}
```

→ Proceed to Step 7

#### Output

- `../repo-wt-PR{N}/.work/tasks/{task_folder}/PR{N}/TODO.md` created
- `../repo-wt-PR{N}/.work/tasks/{task_folder}/PR{N}/QA.md` created

---

### Step 7: Fill in TODO.md with the work plan (inside worktree)

#### Condition

- Step 6 complete

#### Process

Open `TODO.md` in the worktree and replace the template placeholder rows with the actual tasks.
The following rows are mandatory and must not be removed or skipped:

| Done | Task |
|---|---|
| - | Record open questions in QA.md |
| - | Update the spec document in `.work/specs/` |
| - | (Implementation tasks: replace with PR-specific work) |
| - | Update rules / CLAUDE.md |

Also fill in the `## 次PR候補` section at the bottom of TODO.md:
- If the user mentioned follow-up work or future PRs during this session, list them here
- If nothing was mentioned, leave the placeholder row as-is (do not delete the section)

→ Proceed to Step 8

---

### Step 8: Maintain the spec document (inside worktree)

#### Condition

- Step 7 complete

#### Process

1. Check `.work/specs/` inside the worktree for a related spec
2. If found → update the relevant sections for this PR
3. If not found → create a new spec using the template at `${CLAUDE_PLUGIN_ROOT}/templates/spec.md`
4. Add a link to the spec in TODO.md's `## 参考ドキュメント` section

→ Proceed to Step 9

---

### Step 9: Record open questions in QA.md (inside worktree)

#### Condition

- Step 8 complete

#### Process

1. Append any open questions from Step 2 to `PR{N}/QA.md` inside the worktree as QA-XXX entries
2. Skip if there are no open questions

→ Proceed to Step 10

---

### Step 10: Commit created content, report to user, then start implementation

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
