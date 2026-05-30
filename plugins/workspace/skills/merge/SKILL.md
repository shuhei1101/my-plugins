---
name: merge
description: |
  Merge a branch: verify TODO checklist, archive index, merge with --no-ff, remove worktree and
  branch, and confirm any remaining QA entries in the branch document.
  Trigger when the user says "マージして", "merge して", or "ブランチをマージしたい".
disable-model-invocation: true
---

# workspace:merge — Merge a Branch

Runs the full merge flow: TODO checklist verification → master compatibility check → conversation-to-claude inside the worktree (if claude-kit installed) → close related issues → index archive → `--no-ff` merge → worktree cleanup → confirm remaining QA entries in the branch document → auto-invoke pr-handoff for any next branch candidates.

> **Naming**: new branches use `{type}/{title}` (no `PR{N}/` prefix); new worktrees use
> `{repo}-wt-{type}-{title}`. Legacy branches still on `PR{N}/{type}/{title}` with worktrees at
> `{repo}-wt-PR{N}` are handled with their literal recorded names — read the actual branch / worktree
> path from `index.yaml` and `git worktree list` rather than reconstructing from `{N}`.
> `{N}` below refers to the internal numeric ID tracked in `index.yaml` (used in commit cross-references).

---

## Tasks

### Step 1: Identify the branch to merge

#### Condition

- Always — run first

#### Process

1. If the branch to merge is already identified in the current conversation session, use it and proceed to Step 2
2. Otherwise, run the following command to list active entries:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py list-active .work/tasks/index.yaml
```

   Each output line is: `id|title|type|task` — `title` is the recorded branch name (for new branches:
   `{type}/{title}`; for legacy entries it may still be `PR{N} — {title}`)
3. If multiple active entries exist, ask the user which one to merge
4. Resolve the actual branch name and worktree path:
   - **New format** (recorded title is `{type}/{title}`): branch = the title, worktree = `{repo}-wt-{type}-{title}` (slashes replaced with hyphens)
   - **Legacy format** (recorded title is `PR{N} — {title}` and the branch exists as `PR{N}/{type}/{title}`): use the literal `PR{N}/{type}/{title}` and `{repo}-wt-PR{N}`
   - When in doubt, cross-check with `git worktree list` and `git branch --list`

→ Proceed to Step 2

#### Output

- Internal ID `{N}`, branch document path, branch name, and worktree path confirmed

---

### Step 2: Verify the task checklist

#### Condition

- Step 1 complete

#### Process

1. Read the `## 作業内容` table in the branch document at `.work/tasks/{date}_{title}/{branch-hyphenated}.md`
2. Confirm all rows have `済` in the `完了` column

→ Proceed to Step 3 only if all rows are `済`

#### Notes

##### Branching

- Unfinished rows remain → do not merge; report to user and stop

---

### Step 3: Confirm compatibility with master

#### Condition

- Step 2 complete

#### Process

1. Check whether master has new commits since this branch diverged:

```bash
git log HEAD..master --oneline
```

If no output → master has not moved; skip to Step 4.

2. Check for relevant relationships between this branch's changes and master's changes. Use git commands as a starting point, then apply contextual judgment:

```bash
# Get a picture of what this branch changed
git diff master...HEAD --name-only

# Scan master's commits for what changed and where
git log HEAD..master --oneline --stat
```

   Do not rely on file-name matches alone — also consider indirect relationships:
   - Did master change a **caller or importer** of a file this branch modifies?
   - Did master change an **interface, type, schema, or config** that this branch depends on?
   - Did master introduce **naming or structural changes** that this branch's code assumes haven't happened yet?

3. Read the relevant master-side commit content and background:

```bash
git log -p HEAD..master -- {relevant file}
```

4. For each relevant change, judge priority autonomously using these dimensions:
   - **Recency**: which commit is newer?
   - **Blast radius**: is master's change central (many dependents) or local? Central changes take higher priority.
   - **Interface changes**: if master changed a function signature, type, or schema, this branch may be using the old interface → update the branch side
   - **Directional alignment**: are master and this branch heading toward the same goal, or opposite directions? Opposite directions often means one side has an error.
   - **Branch purpose**: if this branch exists specifically to correct or supersede master's change, the branch takes priority.

5. Based on the judgment, take one of the following actions autonomously (no user confirmation needed):
   - **No action needed**: changes are independent → proceed to Step 4
   - **Incorporate master**: master has a related change that this branch should reflect — merge master into the branch:

```bash
git merge master
```

   Resolve conflicts and update the branch's implementation to be compatible.
   - **Branch takes priority**: this branch is specifically correcting master, or the branch approach is clearly the newer correct one → proceed without merging
   - **Tie**: when the judgment is evenly balanced, choose the safe side — incorporate master (`git merge master`), then re-apply the branch's intent on top

→ Proceed to Step 4

#### Notes

##### Autonomous tiebreaker order (when judgment is unclear)

1. Recency — prefer the newer commit
2. Blast radius — prefer the change that more things depend on
3. Branch purpose — if the branch corrects this change, prefer the branch
4. Safe default — incorporate master, then adapt the branch

---

### Step 4: Run conversation-to-claude **inside the worktree** (if claude-kit is installed)

#### Condition

- Step 3 complete
- `WORKSPACE_MERGE_CONV2CLAUDE` is not `false`/`0`/`no`/`off` (default: enabled); if disabled → skip silently to Step 5

#### Process

1. Check whether `/claude-kit:conversation-to-claude` appears in the current session's available skill list
2. If not available → skip this step silently → proceed to Step 5
3. If available → **change to the worktree directory first**, then invoke the skill:

```bash
cd {WORKTREE_PATH}   # e.g. ../{repo}-wt-{type}-{title} (or the legacy ../{repo}-wt-PR{N})
```

   Then invoke `/claude-kit:conversation-to-claude` and wait for it to complete.

4. After completion, ensure that any `.claude/` files generated (rules / references / glossary) are
   committed to the branch. If they were not already committed by the skill, commit them now inside the worktree:

```bash
git -C {WORKTREE_PATH} add .claude/
git -C {WORKTREE_PATH} commit -m "docs: conversation-to-claude artifacts #{N}"
```

5. Return to the main repository directory:

```bash
cd -
```

→ Proceed to Step 5

#### Notes

- This step captures session knowledge before the branch is deleted
- Do not skip even if the conversation seems short — let the skill decide what to persist

##### Why run inside the worktree

Running `conversation-to-claude` from the main repo (master) cwd writes `.claude/` files directly to master.
Those changes are then committed straight to master, separate from the branch's `--no-ff` merge.
The result is that "branch work" and "session knowledge" become scattered across separate commits.
Running inside the worktree includes them in the branch so the merge commit captures everything together.

##### Prohibitions

- Do not run `conversation-to-claude` from the master cwd (causes direct master commits)

---

### Step 5: Close related issues (inside the worktree)

#### Condition

- Step 4 complete

#### Process

1. Read the `## 関連イシュー` section of the branch document at `.work/tasks/{date}_{title}/{branch-hyphenated}.md` in the worktree
2. **If the section is absent, empty, or only contains the template placeholder row** (`| ISSUE-{N} | ... |`) → skip the rest of this step and proceed to Step 6
3. For each row in the table, run the close command **inside the worktree**:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/issue-tool.py" close \
  --issues-dir {WORKTREE_PATH}/.work/issues \
  --issue-id ISSUE-{NNN} \
  --resolution {resolved|wontfix} \
  --linked-pr {N}
```

   The script:
   - Moves `.work/issues/ISSUE-{NNN}.md` → `.work/issues/closed/ISSUE-{NNN}.md`
   - Removes the entry from `_index.yaml` (gitignored — no commit needed)
   - Appends a `closed_issues` entry (with `linked_pr`) to `_index.archive.yaml`
4. If `.work/issues/` does not exist on the project (issue management not adopted), the script prints a skip message — treat as a no-op
5. Commit the changes inside the worktree:

```bash
git -C {WORKTREE_PATH} add .work/issues/
git -C {WORKTREE_PATH} commit -m "chore: close related issues for #{N}"
```

→ Proceed to Step 6

#### Notes

- The issue file moves are git-tracked renames; `_index.yaml` stays gitignored
- This commit will be included in the `--no-ff` merge in Step 8
- If no issue rows were processed, do not create an empty commit

##### Why before mark-completed / archive

Running this step **before** `set-completed` / `archive` keeps the issue-close commit on the PR branch (where it semantically belongs) rather than mixing it with index management.

---

### Step 6: Mark the branch as completed in index.yaml

#### Condition

- Step 5 complete

#### Process

1. Run the following command to mark the entry as `completed: true` in the main repository's `index.yaml`:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py" set-completed \
  .work/tasks/index.yaml --id {N}
```

→ Proceed to Step 7

#### Notes

- Run from the **main repository** directory (not the worktree) — `index.yaml` is gitignored and exists only in the main repo
- No commit is needed for `index.yaml` itself — it remains gitignored

---

### Step 7: Archive completed index entries

#### Condition

- Step 6 complete

#### Process

1. Run the following command to move completed entries to the **worktree's** `index.archive.yaml`:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py" archive \
  .work/tasks/index.yaml \
  {WORKTREE_PATH}/.work/tasks/index.archive.yaml
```

The command prints the number of entries moved. If it prints `0`, skip the rest of this step.

2. If entries were moved, commit `index.archive.yaml` inside the worktree:

```bash
git -C {WORKTREE_PATH} add .work/tasks/index.archive.yaml
git -C {WORKTREE_PATH} commit -m "chore: archive #{N} to index.archive.yaml"
```

→ Proceed to Step 8

#### Notes

- `index.yaml` remains gitignored — no commit needed for it
- `index.archive.yaml` is git-tracked — commit it to the **branch** (not directly to the parent branch); it will be included in the --no-ff merge in Step 8
- The archive command reads from the main repo's `index.yaml` and writes to the worktree's `index.archive.yaml`

---

### Step 8: Execute the merge

#### Condition

- Step 7 complete

> ⚠️ **Pre-merge check required**
> If `index.archive.yaml` was not committed in the worktree in Step 7, the archive changes will be missing from the merge commit.
> **Confirm that the `git commit` inside the worktree in Step 7 has completed before running the merge command.**
> (Skip this check only if Step 7 reported 0 entries moved — no commit was needed.)

#### Notes

##### Prohibitions

> Only merge if this skill was invoked in the user's **most recent message**. If the skill context is still present from a previous turn (not from the current message), do NOT merge — the previous invocation's permission does not carry over.

#### Process

1. Confirm the current branch is the parent branch this branch was branched from (e.g., `master` if branched from `master`, `develop` if branched from `develop`)
2. Merge with `--no-ff`:

```bash
git merge --no-ff -m "{type}: {title} #{N}" {BRANCH_NAME}
```

   Where `{BRANCH_NAME}` is the actual branch name (new format: `{type}/{title}`; legacy: `PR{N}/{type}/{title}`).

→ Proceed to Step 9

---

### Step 9: Remove the worktree and branch

#### Process

1. Remove the worktree and branch:

```bash
git worktree remove {WORKTREE_PATH}
git branch -d {BRANCH_NAME}
```

→ Proceed to Step 10

#### Notes

##### Prohibitions

- Never run `Remove-Item -Recurse` or `rm -rf` at the worktree root

---

### Step 10: Confirm remaining QA entries

#### Process

1. Review the `## QA` section of the branch document at `.work/tasks/{date}_{title}/{branch-hyphenated}.md` and confirm any remaining unresolved entries with the user
2. Commit if there are changes:

```bash
git add .work/
git commit -m "docs: post-merge update for #{N}"
```

→ Proceed to Step 11

---

### Step 11: Report merge completion

#### Process

1. Report the merge as complete to the user
   - Include the merged branch name, internal ID, and task folder

→ Proceed to Step 12

---

### Step 12: Delegate next branch candidates to pr-handoff

#### Condition

- `WORKSPACE_MERGE_AUTO_HANDOFF` is not `false`/`0`/`no`/`off` (default: enabled); if disabled → skip this step and proceed to Step 13

#### Process

1. Read the merged branch document and inspect its `## 次ブランチ候補` section
2. **If next branch candidates exist**: invoke `/workspace:pr-handoff` (no user confirmation needed). Delegate all classification and reservation logic to that skill
3. **If next branch candidates are empty**: skip pr-handoff

→ Proceed to Step 13

---

### Step 13: Present next branch candidates in 3 categories

#### Process

Invoke `/workspace:pr-show` passing the merged branch document path as the data source.

#### Notes

Full logic (reading `## 次ブランチ候補` table, classifying each candidate, branch lookup by title) is defined in the `pr-show` skill.
