---
name: merge
description: |
  Merge a PR: verify TODO checklist, merge with --no-ff, remove worktree and branch,
  and sync QA.md. Trigger when the user says "マージして", "merge して", or "PR をマージしたい".
  Never invoke automatically — only when the user explicitly requests a merge.
disable-model-invocation: true
---

# work-kit:merge — Merge a PR

Runs the full merge flow: TODO checklist verification → `--no-ff` merge
→ worktree cleanup → QA doc sync.

---

## Tasks

### Step 1: Identify the PR to merge

#### Condition

- Always — run first

#### Process

1. Run the following command to list active PRs:

```bash
python plugins/work-kit/scripts/index-tool.py list-active .work/tasks/index.yaml
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

1. Read `## TODO` in `.work/tasks/{date}_{title}/PR{N}/TODO.md`
2. Confirm no unchecked items (`- [ ]`) remain

→ Proceed to Step 3 only if all items are `- [x]`

#### Notes

##### Branching

- Unchecked tasks remain → do not merge; report to user and stop

---

### Step 3: Execute the merge

#### Process

1. Confirm the current branch is master/main
2. Merge with `--no-ff`:

```bash
git merge --no-ff -m "{type}: {title} #PR{N}" PR{N}/{type}/{title}
```

→ Proceed to Step 4

---

### Step 4: Remove the worktree and branch

#### Process

1. Remove the worktree and branch:

```bash
git worktree remove ../$(basename $(pwd))-wt-PR{N}
git branch -d PR{N}/{type}/{title}
```

→ Proceed to Step 5

#### Notes

##### Prohibitions

- Never run `Remove-Item -Recurse` or `rm -rf` at the worktree root

---

### Step 5: Update QA.md

#### Process

1. Review `.work/tasks/{date}_{title}/PR{N}/QA.md` and confirm any remaining unresolved entries with the user
2. Commit if there are changes:

```bash
git add .work/
git commit -m "docs: post-merge update for PR{N}"
```

→ Proceed to Step 6

---

### Step 6: Check archive threshold

#### Process

1. If `plugins/work-kit/scripts/index-tool.py` does not exist, skip this step
2. Check whether `.work/` is gitignored:

```bash
git check-ignore -q .work/
```

   - Exit 0 (gitignored) → skip this step
3. Get the completed PR count:

```bash
python plugins/work-kit/scripts/index-tool.py completed-count .work/tasks/index.yaml
```

4. If count < 100 → skip this step
5. If count ≥ 100 → run `/work-kit:archive` to archive the completed entries

→ Proceed to Step 7

#### Notes

- `index.yaml` remains gitignored; only `index.archive.yaml` is committed (via archive branch)
- The archive branch created by `/work-kit:archive` can be merged separately after this PR

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
- [ ] index.yaml archived (if trim-index.py is present)
