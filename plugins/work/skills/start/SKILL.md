---
name: start
description: |
  Start a new branch: decide the branch name, collect details, add the index.yaml entry in the main
  repo, create a worktree, then create the single per-branch task document INSIDE the worktree.
  Trigger when the user says "新しいブランチを切って", "新しい作業を始めたい", "work-start して",
  "start new work", or "create a new branch".
---

# work:start — Start a New Branch

Creates the worktree first, then creates the single per-branch task document inside it.
This prevents task documents from being created in the main repository.

> **Naming**: branches use `{type}/{title}` (no `PR{N}/` prefix). The worktree mirrors the branch as
> `{repo}-wt-{type}-{title}` (slashes → hyphens). The branch document filename is `{YYMMDD}-{branch-hyphenated}.md`
> (e.g. `refactor/foo-bar` created on 260531 → `260531-refactor-foo-bar.md`).
> An internal numeric ID is still tracked in `index.yaml` for archive metadata, but it does not appear in branch names, worktree paths, or branch document filenames.

---

## Tasks

### Step 1: Decide the branch name

#### Condition

- Always — run first

#### Process

1. Determine the branch suffix from the requested work:
   - **Type**: `feat` / `fix` / `refactor` / `docs` / `chore` / `test`
   - **Title**: short kebab-case label that describes the work
2. The full branch name is `{type}/{title}` (for example `refactor/rename-pr-to-branch`).
3. Reserve an internal ID for `index.yaml` bookkeeping (used in the archive — it does not appear in the branch name itself):

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py next-id .work/tasks/index.yaml
```

→ Proceed to Step 2

#### Output

- Branch name `{type}/{title}` decided
- Internal ID `{N}` reserved

---

### Step 2: Collect request details

#### Condition

- Step 1 complete

#### Process

1. Determine the following:
   - **TODO list**: what will be done on this branch (becomes the checklist)
   - **Note**: does a related note exist in `.work/notes/`? Or does one need to be created?
   - **Open questions**: anything unclear or undecided

→ Proceed to Step 3

#### Output

- TODO list, note info, and open questions confirmed

---

### Step 3: Add entry to index.yaml (main repository)

#### Condition

- Step 2 complete

#### Process

1. Run the following command to add the new branch entry:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py add .work/tasks/index.yaml \
  --id {N} \
  --title "{type}/{title}" \
  --type {type} \
  --summary "{summary}" \
  --task "{YYMMDD}_{title}"
```

→ Proceed to Step 4

#### Output

- `.work/tasks/index.yaml` updated with the new branch entry and `last_id` (main repository)

#### Notes

- `index.yaml` is excluded by `.work/tasks/.gitignore` — no commit to master is needed
- Use a 6-digit `YYMMDD` (e.g. `260530`), not the 8-digit `YYYYMMDD` form
- `--id {N}` is the internal numeric ID reserved in Step 1; it is recorded in the YAML row but
  not embedded in the branch / worktree / filename
- `--title` records the branch name as the row title (no `PR{N}` prefix)

---

### Step 4: Create the worktree and branch (if enabled)

#### Condition

- Step 3 complete

#### Process

1. Check whether worktree usage is enabled. It is **enabled by default**; disabled only when the
   `WORK_USE_WORKTREE` env var is set to a falsy value (`false` / `0` / `no` / `off`):

   ```bash
   v="${WORK_USE_WORKTREE:-true}"; case "${v,,}" in false|0|no|off) echo disabled;; *) echo enabled;; esac
   ```

2. **If enabled**: invoke `/work:worktree-create` with the branch name:

   > `/work:worktree-create {type}/{title}`

3. **If disabled**: skip worktree creation and notify the user:

   > ⚠️ `WORK_USE_WORKTREE` が無効のため、ワークツリーの作成をスキップします。  
   > `.work/` フォルダ管理のみで作業を続けます。  
   > ワークツリーを使用したい場合は `settings.json` の `env` から `WORK_USE_WORKTREE` を外すか `true` に設定してください。

→ Proceed to Step 5

#### Output

- (worktree enabled) Worktree created at `../{repo}-wt-{type}-{title}`, branch `{type}/{title}` exists
- (worktree disabled) No worktree; proceed with `.work/` folder management only

#### Notes

##### Prohibitions

- Never commit directly to master/main

---

### Step 5: Determine the task folder (autonomous judgment)

#### Condition

- Step 4 complete

#### Process

1. Read all folder names under `.work/tasks/` in the worktree
2. Compare each folder name (`YYMMDD_title` format) against the purpose of this branch and decide:
   - **Add to existing folder**: an existing folder covers the same goal or feature area, and this branch fits naturally as part of it
     - Examples: splitting a feature across multiple branches, a follow-up fix, related refactoring
   - **Create new folder**: no existing folder is closely related, or `.work/tasks/` is empty
3. Confirm the argument to pass to the next step:
   - Adding to existing → use `--task-dir {folder_name}`
   - Creating new → use `--date {YYMMDD} --title {title}`

→ Proceed to Step 6

#### Output

- Task folder strategy (new or existing) and the arguments to use are confirmed

#### Notes

- Do not ask the user — decide autonomously based on content
- When in doubt, create a new folder (folders can be consolidated later)
- New folders must use the 6-digit `YYMMDD` prefix and a **Japanese title** (e.g. `260530_タスクフォルダ命名統一`)

---

### Step 6: Create the branch document (inside worktree)

#### Condition

- Step 5 complete

#### Process

Run one of the following depending on the choice in Step 5. The `--branch` argument is the branch
name (`{type}/{title}`); the script prepends the date and converts slashes to hyphens to form the file name
(e.g. `refactor/rename-pr-to-branch` on 260531 → `260531-refactor-rename-pr-to-branch.md`):

**New task folder:**

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/setup-task.py \
  ../$(basename $(pwd))-wt-{type}-{title} \
  --id {N} \
  --branch {type}/{title} \
  --title {title} \
  --date {YYMMDD} \
  --plugin-root ${CLAUDE_PLUGIN_ROOT}
```

**Add to existing task folder:**

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/setup-task.py \
  ../$(basename $(pwd))-wt-{type}-{title} \
  --id {N} \
  --branch {type}/{title} \
  --task-dir {existing_folder_name} \
  --title {title} \
  --plugin-root ${CLAUDE_PLUGIN_ROOT}
```

→ Proceed to Step 7

#### Output

- `../{repo}-wt-{type}-{title}/.work/tasks/{task_folder}/{YYMMDD}-{type}-{title}.md` created

---

### Step 7: Fill in the branch document with the work plan (inside worktree)

#### Condition

- Step 6 complete

#### Process

Open the created `{YYMMDD}-{type}-{title}.md` in the worktree and replace the template placeholder content
with the actual plan. The document holds every section for this branch — TODO, variations, QA, and
references — all in one file.

**`## 概要`** — write the goal / background, plus the `### 実施条件` sub-section:

- `### 実施条件`: when this branch can be started. `即時実施可`, or `「{other branch name}」が完了してから`.
  Mirrors the `実施条件` column from the triggering branch's `## 次ブランチ候補` row.

**`## 作業内容`** — task checklist. The following rows are mandatory and must not be removed or skipped:

| # | 完了 | 作業内容 |
|---|---|---|
| 1 | - | Record open questions in `## QA` (this same document) |
| 2 | - | Update the note document in `.work/notes/` |
| 3 | - | (Implementation tasks: replace with branch-specific work) |
| 4 | - | Update rules / CLAUDE.md |

**`## 変更内容`** — the implementation files this branch adds or modifies (excluding tests). Fill in
once implementation starts — every file that lands in a commit goes here:

| # | ファイル名 | 新規/編集 | 内容 | 補足 |

**`## テスト`** — test files added or modified alongside the implementation. Leave the placeholder row if
this branch has no test changes; otherwise list each test file.

**`## QA`** — record open questions from Step 2 as QA-XXX entries here (Step 9 below appends them).

**`## 参考ドキュメント`** — links to related notes / specs (the note from Step 8 is appended here).

**`## 関連イシュー`** — list `.work/issues/ISSUE-{N}` entries this branch resolves
(table format: `| # | ID | 概要 | resolution |`). `resolution` is `resolved` or `wontfix`.
**If there are no related issues**: delete the `## 関連イシュー` heading and table entirely.

**`## 関連ブランチ`** — list branches directly related to this one (predecessors, split siblings,
follow-ups) (table format: `| # | ブランチ | 概要 |`). Leave the placeholder row if there are none.

**`## 次ブランチ候補`** — list follow-up branches mentioned during this session
(columns: `#` / title / summary / 実施条件):
- `即時実施可` (or `-`) when the candidate has no dependency
- `「{other candidate title}」が完了したら` when the candidate depends on another candidate in the same table

→ Proceed to Step 8

---

### Step 8: Maintain the note document (inside worktree)

#### Condition

- Step 7 complete

#### Process

1. Check `.work/notes/` inside the worktree for a related note
2. If found → update the relevant sections for this branch
3. If not found → create a new note using the template at `${CLAUDE_PLUGIN_ROOT}/templates/note.md`
   - The note H1 title must be written **entirely in Japanese** (e.g. `# 機能名 — 一行説明`)
   - Technical identifiers (plugin names, command names, file paths) may remain in their original form
4. Add a link to the note in the branch document's `## 参考ドキュメント` section
5. Update (or create) `.work/notes/_index.md`:
   - Add the new note to the appropriate category, or update the entry if the note already existed
   - If `_index.md` does not exist, create it with all current notes grouped by category

→ Proceed to Step 9

---

### Step 9: Record open questions in the `## QA` section (inside worktree)

#### Condition

- Step 8 complete

#### Process

1. Append any open questions from Step 2 to the `## QA` section of the branch document as QA-XXX entries
2. Skip if there are no open questions

→ Proceed to Step 10

---

### Step 10: Commit created content, report to user, then start implementation

#### Process

1. Commit all created files inside the worktree (branch: `{type}/{title}`)
2. Report what was created: branch name, worktree path, branch document path, note path
3. Start implementation:
   - **If QA entries exist** → ask the user for confirmation before starting
   - **If no QA entries** → proceed with implementation immediately

#### Notes

##### Prohibitions

- Never commit to anywhere other than the created worktree (`{type}/{title}` branch)

##### Commit granularity

- Commit in meaningful units that are easy for the user to understand
- Do not split commits too finely
- Do not mix planning documents (branch document, notes, etc.) and implementation code in the same commit

##### Commit message language

- All commit messages produced by this skill MUST be written in **Japanese**
- Both subject and body are in Japanese (metadata lines like `Co-Authored-By:` may remain in English)
- Conventional commit prefixes (`feat:` `fix:` `chore:` etc.) may stay in English
- Example: `chore: {type}/{title} のブランチドキュメントを作成`
