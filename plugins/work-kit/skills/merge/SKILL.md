---
name: merge
description: |
  Merge a PR: verify TODO checklist, archive index, merge with --no-ff, remove worktree and branch,
  and sync QA.md. Trigger when the user says "マージして", "merge して", or "PR をマージしたい".
  Never invoke automatically — only when the user explicitly requests a merge.
disable-model-invocation: true
---

# work-kit:merge — Merge a PR

Runs the full merge flow: TODO checklist verification → conversation-to-claude (if claude-kit installed) → index archive → `--no-ff` merge → worktree cleanup → QA doc sync.

---

## Tasks

### Step 1: Identify the PR to merge

#### Condition

- Always — run first

#### Process

1. If the PR to merge is already identified in the current conversation session, use that PR and proceed to Step 2
2. Otherwise, run the following command to list active PRs:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py list-active .work/tasks/index.yaml
```

   Each output line is: `id|title|type|task`
3. If multiple active PRs exist, ask the user which one to merge
4. Confirm the branch name: `PR{N}/{type}/{title}`

→ Proceed to Step 2

#### Output

- PR number, TODO.md path, and branch name confirmed

---

### Step 2: Verify the TODO checklist

#### Condition

- Step 1 complete

#### Process

1. Read `## 作業内容` table in `.work/tasks/{date}_{title}/PR{N}/TODO.md`
2. Confirm all rows have `済` in the Done column

→ Proceed to Step 3 only if all rows are `済`

#### Notes

##### Branching

- Unfinished rows remain → do not merge; report to user and stop

---

### Step 3: Run conversation-to-claude (if claude-kit is installed)

#### Condition

- Step 2 complete

#### Process

1. Check whether `/claude-kit:conversation-to-claude` appears in the current session's available skill list
2. If available → invoke `/claude-kit:conversation-to-claude` and wait for it to complete
3. If not available → skip this step silently

→ Proceed to Step 4

#### Notes

- This step captures session knowledge before the branch is deleted
- Do not skip even if the conversation seems short — let the skill decide what to persist

---

### Step 4: Mark the PR as completed in index.yaml

#### Condition

- Step 3 complete

#### Process

1. Run the following command to mark the PR as `completed: true` in the main repository's `index.yaml`:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py" set-completed \
  .work/tasks/index.yaml --id {N}
```

→ Proceed to Step 5

#### Notes

- Run from the **main repository** directory (not the worktree) — `index.yaml` is gitignored and exists only in the main repo
- No commit is needed for `index.yaml` itself — it remains gitignored

---

### Step 5: Archive completed index entries

#### Condition

- Step 4 complete

#### Process

1. Run the following command to move completed entries to the **worktree's** `index.archive.yaml`:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py" archive \
  .work/tasks/index.yaml \
  ../$(basename $(pwd))-wt-PR{N}/.work/tasks/index.archive.yaml
```

The command prints the number of entries moved. If it prints `0`, skip the rest of this step.

2. If entries were moved, commit `index.archive.yaml` inside the worktree:

```bash
git -C ../$(basename $(pwd))-wt-PR{N} add .work/tasks/index.archive.yaml
git -C ../$(basename $(pwd))-wt-PR{N} commit -m "chore: archive PR{N} to index.archive.yaml #PR{N}"
```

→ Proceed to Step 6

#### Notes

- `index.yaml` remains gitignored — no commit needed for it
- `index.archive.yaml` is git-tracked — commit it to the **PR branch** (not directly to the parent branch); it will be included in the --no-ff merge in Step 6
- The archive command reads from the main repo's `index.yaml` and writes to the worktree's `index.archive.yaml`

---

### Step 6: Execute the merge

#### Condition

- Step 5 complete

> ⚠️ **Pre-merge check required**
> If `index.archive.yaml` was not committed in the worktree in Step 5, the archive changes will be missing from the merge commit.
> **Confirm that the `git commit` inside the worktree in Step 5 has completed before running the merge command.**
> (Skip this check only if Step 5 reported 0 entries moved — no commit was needed.)

#### Process

1. Confirm the current branch is the parent branch the PR was branched from (e.g., `master` if branched from `master`, `develop` if branched from `develop`)
2. Merge with `--no-ff`:

```bash
git merge --no-ff -m "{type}: {title} #PR{N}" PR{N}/{type}/{title}
```

→ Proceed to Step 7

---

### Step 7: Remove the worktree and branch

#### Process

1. Remove the worktree and branch:

```bash
git worktree remove ../$(basename $(pwd))-wt-PR{N}
git branch -d PR{N}/{type}/{title}
```

→ Proceed to Step 8

#### Notes

##### Prohibitions

- Never run `Remove-Item -Recurse` or `rm -rf` at the worktree root

---

### Step 8: Update QA.md

#### Process

1. Review `.work/tasks/{date}_{title}/PR{N}/QA.md` and confirm any remaining unresolved entries with the user
2. Commit if there are changes:

```bash
git add .work/
git commit -m "docs: post-merge update for PR{N}"
```

→ Proceed to Step 9

---

### Step 9: Report completion

#### Process

1. Report merge complete to the user
2. Read the merged PR's `TODO.md` and present the contents of the `## 次PR候補` section as recommended next PRs
3. List any remaining in-progress PRs under `.work/tasks/`

#### Notes

##### Checklist

- [ ] Merge commit exists
- [ ] Worktree and branch deleted
- [ ] QA.md reviewed and updated
- [ ] index.archive.yaml committed to the PR branch and included in the merge (if completed entries existed)
