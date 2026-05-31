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

> **Naming**: branches use `{type}/{title}` by default. If `WORK_BRANCH_AUTHOR` is set, the author
> segment is inserted: `{type}/{author}/{title}` (e.g. `feat/nishikawa/test-update`).
> The worktree mirrors the full branch name with slashes replaced by hyphens: `{repo}-wt-{branch-hyphenated}`.
> The branch document filename is `{YYMMDD}-{日本語タイトル}.branch.md` — the Japanese title collected in Step 2
> (e.g. `260531-ブランチ文書ファイル名変更.branch.md`). The `.branch.md` extension marks it as the branch
> document (the task folder may also hold user files). The git branch name is recorded inside the document header.
> The branch index (`index.yaml`) is keyed by the branch name; there is no numeric ID or `last_id`.

---

## Tasks

### Step 1: Decide the branch name

#### Condition

- Always — run first

#### Process

1. Determine the branch suffix from the requested work:
   - **Type**: `feat` / `fix` / `refactor` / `docs` / `chore` / `test`
   - **Title**: short kebab-case label that describes the work
2. Check `WORK_BRANCH_AUTHOR` to build the full branch name:

   ```bash
   author="${WORK_BRANCH_AUTHOR:-}"
   ```

   - If `$author` is non-empty: branch name is `{type}/${author}/{title}` (e.g. `feat/nishikawa/test-update`)
   - If `$author` is empty or unset: branch name is `{type}/{title}` (e.g. `feat/test-update`)

→ Proceed to Step 2

#### Output

- Branch name decided (with or without author segment)

---

### Step 2: Collect request details

#### Condition

- Step 1 complete

#### Process

1. Determine the following:
   - **日本語タイトル**: descriptive Japanese title for this branch work — used in the document H1 and as the file name (e.g. `ブランチ文書ファイル名変更`)
   - **TODO list**: what will be done on this branch (becomes the checklist)
   - **Note**: does a related note exist in `.work/notes/`? Or does one need to be created?
   - **Open questions**: anything that needs to be confirmed or decided before starting implementation.
     Check from these angles:
     - **Maintainability / extensibility**: Is this approach manageable long-term? Is there a simpler alternative?
     - **Scope / cost**: Is the implementation over-engineered for the requirement?
     - **Performance**: Are there concerns about processing load, speed, or token consumption?
     - **Library / tool selection**: When multiple options exist, which one to use?
     - **Alternative implementation**: Is there a better approach than what the user described?
     - **Breaking changes**: Does this affect existing behavior or interfaces?

→ Proceed to Step 3

#### Output

- 日本語タイトル `{日本語タイトル}`, TODO list, note info, and open questions confirmed

---

### Step 3: Add entry to index.yaml (main repository)

#### Condition

- Step 2 complete

#### Process

1. Run the following command to add the new branch entry:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py add .work/tasks/index.yaml \
  --branch "{full-branch-name}" \
  --title "{日本語タイトル}" \
  --type {type} \
  --summary "{summary}" \
  --task "{YYMMDD}_{title}"
```

→ Proceed to Step 4

#### Output

- `.work/tasks/index.yaml` updated with the new branch entry (main repository)

#### Notes

- `index.yaml` is excluded by `.work/tasks/.gitignore` — no commit to master is needed
- Use a 6-digit `YYMMDD` (e.g. `260530`), not the 8-digit `YYYYMMDD` form
- `--branch` records the git branch name; `--title` records the Japanese document title

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

2. **If enabled**: invoke `/work:worktree-create` with the full branch name (including author if set):

   > `/work:worktree-create {full-branch-name}`
   >
   > e.g. `/work:worktree-create feat/nishikawa/test-update` or `/work:worktree-create feat/test-update`

3. **If disabled**: skip worktree creation and notify the user:

   > ⚠️ `WORK_USE_WORKTREE` が無効のため、ワークツリーの作成をスキップします。  
   > `.work/` フォルダ管理のみで作業を続けます。  
   > ワークツリーを使用したい場合は `settings.json` の `env` から `WORK_USE_WORKTREE` を外すか `true` に設定してください。

→ Proceed to Step 5

#### Output

- (worktree enabled) Worktree created at `../{repo}-wt-{branch-hyphenated}`, branch exists
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
3. Decide the branch-document path inside the worktree `{wt}`
   (`{wt}` = `../$(basename $(pwd))-wt-{branch-hyphenated}`, slashes in the full branch name → hyphens):
   - New folder: `{wt}/.work/tasks/{YYMMDD}_{title}/{YYMMDD}-{日本語タイトル}.branch.md`
   - Existing folder: `{wt}/.work/tasks/{existing_folder_name}/{YYMMDD}-{日本語タイトル}.branch.md`

→ Proceed to Step 6

#### Output

- Task folder strategy (new or existing) and the full branch-document path are confirmed

#### Notes

- Do not ask the user — decide autonomously based on content
- When in doubt, create a new folder (folders can be consolidated later)
- New folders must use the 6-digit `YYMMDD` prefix and a **Japanese title** (e.g. `260530_タスクフォルダ命名統一`)

---

### Step 6: Create and fill in the branch document (inside worktree)

#### Condition

- Step 5 complete

#### Process

1. `Write` the branch document at the path decided in Step 5
   (`{YYMMDD}-{日本語タイトル}.branch.md`).
2. The **template is auto-injected** by the ref-inject hook the moment you write a `.branch.md`
   file under `.work/tasks/` (your first write is blocked once and the full template +
   section fill-in guide from `references/work-dir/タスクドキュメント.md` appears). Author the
   document from that injected template — there is **no script** and no template file to copy.
3. Fill in the real plan as you write:
   - H1 = `{日本語タイトル}`; `> ブランチ:` = the full git branch name.
   - `## 概要` (incl. `### 実施条件` — `即時実施可` or `「{other branch}」が完了してから`,
     mirroring the triggering branch's `## 次ブランチ候補` row).
   - `## 作業内容` — keep the mandatory rows (record QA / update note); add the implementation tasks.
   - `## 変更内容` / `## テスト` — leave placeholder rows; fill in during implementation.
   - `## QA` — open questions from Step 2 (Step 7 appends them).
   - `## 参考ドキュメント` — leave empty; the note path is added in the final commit (Step 9).
   - `## 関連イシュー` — issues this branch resolves; **delete the heading + table if none**.
   - `## 関連ブランチ` / `## 次ブランチ候補` — fill from this session, or leave placeholders.

The injected `タスクドキュメント.md` reference is the single source of truth for the section
structure and rules — follow it.

→ Proceed to Step 7

#### Output

- `{wt}/.work/tasks/{task_folder}/{YYMMDD}-{日本語タイトル}.branch.md` created and filled with the plan

---

### Step 7: Record open questions in the `## QA` section (inside worktree)

#### Condition

- Step 6 complete

#### Process

1. Append any open questions from Step 2 to the `## QA` section of the branch document as QA-XXX entries
2. Skip if there are no open questions

→ Proceed to Step 8

---

### Step 8: First commit — create branch document, then start implementation

#### Process

1. Commit **only the branch document** inside the worktree (branch: `{branch}`)
   - Do **not** include notes at this stage — notes are committed in the final Step 9
2. Report what was created: branch name, worktree path, branch document path
3. Start implementation:
   - **If QA entries exist** → ask the user for confirmation before starting
   - **If no QA entries** → proceed with implementation immediately

#### Notes

##### Prohibitions

- Never commit to anywhere other than the created worktree (`{branch}` branch)
- Never include notes or final updates in this first commit

##### Commit granularity

- Commit in meaningful units that are easy for the user to understand
- Do not split commits too finely
- Do not mix planning documents (branch document) and implementation code in the same commit

##### Commit ordering

This commit is always the **first** commit of the branch.
Implementation commits follow in the middle.
The final commit (Step 9) closes the branch with notes and branch document updates.

##### Commit message language

Read the following env vars before composing every commit message:

```bash
lang="${WORK_COMMIT_LANG:-JP}"
use_type_raw="${WORK_COMMIT_TYPE:-true}"; case "${use_type_raw,,}" in false|0|no|off) use_type=false;; *) use_type=true;; esac
```

- **`WORK_COMMIT_LANG`** (default `JP`): `JP` → Japanese; `EN` → English. Both subject and body follow this setting. Metadata lines like `Co-Authored-By:` may remain in English regardless.
- **`WORK_COMMIT_TYPE`** (default `true`): truthy → include `feat:` / `fix:` / `chore:` etc. prefix; falsy → omit the type prefix entirely.

| `WORK_COMMIT_LANG` | `WORK_COMMIT_TYPE` | Example commit message |
|---|---|---|
| `JP` (default) | `true` (default) | `chore: feat/commit-message-options のブランチドキュメントを作成` |
| `EN` | `true` | `chore: create branch document for feat/commit-message-options` |
| `JP` | `false` | `feat/commit-message-options のブランチドキュメントを作成` |
| `EN` | `false` | `create branch document for feat/commit-message-options` |

---

### Step 9: Final commit — update notes and branch document

#### Condition

- All implementation work is complete

#### Process

1. Check `.work/notes/` inside the worktree for a related note
2. If found → update it to reflect the current state (a note is a **current spec sheet** — overwrite stale text, don't append history)
3. If not found → create a new note following `ノート記述内容ルール.md` (auto-injected when you edit a file under `.work/notes/`): present state only, no YAML frontmatter, fixed template ending in a `## 変更履歴` table
   - The note H1 title must be written **entirely in Japanese** (e.g. `# 機能名 — 一行説明`)
   - Technical identifiers (plugin names, command names, file paths) may remain in their original form
4. Add a link to the note in the branch document's `## 参考ドキュメント` section
5. Update (or create) `.work/notes/_index.md`:
   - Add the new note to the appropriate category, or update the entry if the note already existed
   - If `_index.md` does not exist, create it with all current notes grouped by category
6. Commit the updated notes + branch document together as the **final commit** of the branch

#### Notes

- This is always the **last** commit of the branch
- Commit notes and branch document together — do not split them
