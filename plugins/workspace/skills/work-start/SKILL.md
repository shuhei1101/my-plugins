---
name: work-start
description: |
  Start a new PR: determine PR number, collect details, add index.yaml entry in main repo,
  create worktree, then create the single per-PR task document INSIDE the worktree.
  Trigger when the user says "新しい PR を作って", "新しい作業を始めたい", "work-start して",
  "start new work", or "create a new PR".
---

# workspace:work-start — Start a New PR

Creates the worktree first, then creates the single per-PR task document inside it.
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
   - **Note**: does a related note exist in `.work/notes/`? Or does one need to be created?
   - **Open questions**: anything unclear or undecided

→ Proceed to Step 3

#### Output

- Title, type, TODO list, note info, and open questions confirmed

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
  --task "{YYMMDD}_{title}"
```

→ Proceed to Step 4

#### Output

- `.work/tasks/index.yaml` updated with the new PR entry and `last_id` (main repository)

#### Notes

- `index.yaml` is excluded by `.work/tasks/.gitignore` — no commit to master is needed
- Use a 6-digit `YYMMDD` (e.g. `260530`), not the 8-digit `YYYYMMDD` form

---

### Step 4: Create the worktree and branch (if enabled)

#### Condition

- Step 3 complete

#### Process

1. Check whether worktree usage is enabled. It is **enabled by default**; disabled only when the
   `WORKSPACE_USE_WORKTREE` env var is set to a falsy value (`false` / `0` / `no` / `off`):

   ```bash
   v="${WORKSPACE_USE_WORKTREE:-true}"; case "${v,,}" in false|0|no|off) echo disabled;; *) echo enabled;; esac
   ```

2. **If enabled**: invoke `/workspace:work-add` with the PR number and branch:

   > `/workspace:work-add PR{N} {type}/{title}`

3. **If disabled**: skip worktree creation and notify the user:

   > ⚠️ `WORKSPACE_USE_WORKTREE` が無効のため、ワークツリーの作成をスキップします。  
   > `.work/` フォルダ管理のみで作業を続けます。  
   > ワークツリーを使用したい場合は `settings.json` の `env` から `WORKSPACE_USE_WORKTREE` を外すか `true` に設定してください。

→ Proceed to Step 5

#### Output

- (worktree enabled) Worktree created at `../repo-wt-PR{N}`, branch `PR{N}/{type}/{title}` exists
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
2. Compare each folder name (`YYMMDD_title` format) against the purpose of this PR and decide:
   - **Add to existing folder**: an existing folder covers the same goal or feature area, and this PR fits naturally as part of it
     - Examples: splitting a feature across multiple PRs, a follow-up fix, related refactoring
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
- Legacy folders may still use the 8-digit `YYYYMMDD` prefix — leave them as-is; only new folders use `YYMMDD`

---

### Step 6: Create the PR document (inside worktree)

#### Condition

- Step 5 complete

#### Process

Run one of the following depending on the choice in Step 5. The `--branch` argument is the full branch
name (`PR{N}/{type}/{title}`); the script converts slashes to hyphens to form the file name
(e.g. `PR168/refactor/refactor-task-doc-structure` → `PR168-refactor-refactor-task-doc-structure.md`):

**New task folder:**

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/setup-task.py \
  ../$(basename $(pwd))-wt-PR{N} \
  --pr {N} \
  --branch PR{N}/{type}/{title} \
  --title {title} \
  --date {YYMMDD} \
  --plugin-root ${CLAUDE_PLUGIN_ROOT}
```

**Add to existing task folder:**

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/setup-task.py \
  ../$(basename $(pwd))-wt-PR{N} \
  --pr {N} \
  --branch PR{N}/{type}/{title} \
  --task-dir {existing_folder_name} \
  --title {title} \
  --plugin-root ${CLAUDE_PLUGIN_ROOT}
```

→ Proceed to Step 7

#### Output

- `../repo-wt-PR{N}/.work/tasks/{task_folder}/PR{N}-{type}-{title}.md` created

---

### Step 7: Fill in the PR document with the work plan (inside worktree)

#### Condition

- Step 6 complete

#### Process

Open the created `PR{N}-{type}-{title}.md` in the worktree and replace the template placeholder content with
the actual plan. The document holds every section for this PR — TODO, variations, QA, and references — all
in one file.

**`## 概要`** — write the goal / background, plus the `### 実施条件` sub-section:

- `### 実施条件`: when this PR can be started. `即時実施可`, or `「{other PR name}」が完了してから`.
  Mirrors the `実施条件` column from the triggering PR's `## 次PR候補` row.

**`## 作業内容`** — task checklist. The following rows are mandatory and must not be removed or skipped:

| 完了 | 作業内容 | 対象ファイル |
|---|---|---|
| - | Record open questions in `## QA` (this same document) | - |
| - | Update the note document in `.work/notes/` | - |
| - | (Implementation tasks: replace with PR-specific work) | - |
| - | Update rules / CLAUDE.md | - |

**`## 変更内容`** — the implementation files this PR adds or modifies (excluding tests). Fill in once
implementation starts — every file that lands in a commit goes here:

| ファイル名 | 新規/編集 | 内容 | 補足 |

**`## テスト`** — test files added or modified alongside the implementation. Leave the placeholder row if
this PR has no test changes; otherwise list each test file.

**`## QA`** — record open questions from Step 2 as QA-XXX entries here (Step 9 below appends them).

**`## 参考ドキュメント`** — links to related notes / specs (the note from Step 8 is appended here).

**`## 関連イシュー`** — list `.work/issues/ISSUE-{N}` entries this PR resolves
(table format: `| ID | 概要 | resolution |`). `resolution` is `resolved` or `wontfix`.
**If there are no related issues**: delete the `## 関連イシュー` heading and table entirely.

**`## 関連PR`** — list PRs directly related to this one (predecessors, split siblings, follow-ups)
(table format: `| PR番号 | 概要 |`). Leave the placeholder row if there are none.

**`## 次PR候補`** — list follow-up PRs mentioned during this session
(columns: title / summary / 実施条件):
- `即時実施可` (or `-`) when the candidate has no dependency
- `「{other candidate title}」が完了したら` when the candidate depends on another candidate in the same table

→ Proceed to Step 8

---

### Step 8: Maintain the note document (inside worktree)

#### Condition

- Step 7 complete

#### Process

1. Check `.work/notes/` inside the worktree for a related note
2. If found → update the relevant sections for this PR
3. If not found → create a new note using the template at `${CLAUDE_PLUGIN_ROOT}/templates/note.md`
4. Add a link to the note in the PR document's `## 参考ドキュメント` section

→ Proceed to Step 9

---

### Step 9: Record open questions in the `## QA` section (inside worktree)

#### Condition

- Step 8 complete

#### Process

1. Append any open questions from Step 2 to the `## QA` section of the PR document as QA-XXX entries
2. Skip if there are no open questions

→ Proceed to Step 10

---

### Step 10: Commit created content, report to user, then start implementation

#### Process

1. Commit all created files inside the worktree (branch: `PR{N}/{type}/{title}`)
2. Report what was created: branch name, worktree path, PR document path, note path
3. Start implementation:
   - **If QA entries exist** → ask the user for confirmation before starting
   - **If no QA entries** → proceed with implementation immediately

#### Notes

##### Prohibitions

- Never commit to anywhere other than the created worktree (`PR{N}/{type}/{title}` branch)

##### Commit granularity

- Commit in meaningful units that are easy for the user to understand
- Do not split commits too finely
- Do not mix planning documents (PR document, notes, etc.) and implementation code in the same commit

##### Commit message language

- All commit messages produced by this skill MUST be written in **Japanese**
- Both subject and body are in Japanese (metadata lines like `Co-Authored-By:` may remain in English)
- Conventional commit prefixes (`feat:` `fix:` `chore:` etc.) may stay in English
- Example: `chore: PR{N} のタスクドキュメントを作成 #PR{N}`
