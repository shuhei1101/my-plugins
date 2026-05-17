---
name: merge
description: |
  Merge a PR: verify TODO checklist, archive index, merge with --no-ff, remove worktree and branch,
  and sync QA.md. Trigger when the user says "マージして", "merge して", or "PR をマージしたい".
  Never invoke automatically — only when the user explicitly requests a merge.
disable-model-invocation: true
---

# work-kit:merge — Merge a PR

Runs the full merge flow: TODO checklist verification → index archive → `--no-ff` merge
→ worktree cleanup → QA doc sync.

---

## Tasks

### Step 1: Identify the PR to merge

#### Condition

- Always — run first

#### Process

1. Run the following command to list active PRs:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py list-active .work/tasks/index.yaml
```

   Each output line is: `id|title|type|task`
2. If multiple active PRs exist, ask the user which one to merge
3. Confirm the branch name: `PR{N}/{type}/{title}`

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

### Step 3: Archive completed index entries

#### Process

1. If `${CLAUDE_PLUGIN_ROOT}/scripts/trim-index.py` does not exist, skip this step
2. Run trim to move completed entries from `index.yaml` to `index.archive.yaml`:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/trim-index.py .work/tasks/index.yaml
```

3. If output is "Nothing to archive", skip the commit below
4. If `index.archive.yaml` was created or updated, commit it:

```bash
git add .work/tasks/index.archive.yaml
git commit -m "chore: archive completed PR entries"
```

→ Proceed to Step 4

#### Notes

- `index.yaml` remains gitignored — no commit needed for it
- `index.archive.yaml` is git-tracked — commit it directly to master as part of this merge flow

---

### Step 4: Execute the merge

#### Process

1. Confirm the current branch is master/main
2. Merge with `--no-ff`:

```bash
git merge --no-ff -m "{type}: {title} #PR{N}" PR{N}/{type}/{title}
```

→ Proceed to Step 5

---

### Step 5: Remove the worktree and branch

#### Process

1. Remove the worktree and branch:

```bash
git worktree remove ../$(basename $(pwd))-wt-PR{N}
git branch -d PR{N}/{type}/{title}
```

→ Proceed to Step 6

#### Notes

##### Prohibitions

- Never run `Remove-Item -Recurse` or `rm -rf` at the worktree root

---

### Step 6: Update QA.md

#### Process

1. Review `.work/tasks/{date}_{title}/PR{N}/QA.md` and confirm any remaining unresolved entries with the user
2. Commit if there are changes:

```bash
git add .work/
git commit -m "docs: post-merge update for PR{N}"
```

→ Proceed to Step 7

---

### Step 7: Report completion

#### Process

1. Report merge complete to the user
2. List any remaining in-progress PRs under `.work/tasks/`

#### Notes

##### Checklist

- [ ] Merge commit exists
- [ ] Worktree and branch deleted
- [ ] QA.md reviewed and updated
- [ ] index.archive.yaml committed (if trim-index.py is present and had entries)
