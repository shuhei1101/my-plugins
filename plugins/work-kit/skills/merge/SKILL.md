---
name: merge
description: |
  Merge a PR: verify task checklist, merge with --no-ff, remove worktree and branch,
  update index.yaml to completed, and sync qa docs.
  Manual invocation only — use /work-kit:merge.
  Trigger when the user says "マージして", "merge して", or "PR をマージしたい".
disable-model-invocation: true
allowed-tools: Bash Read Write
---

# work-kit:merge — Merge a PR

Runs the full merge flow: checklist verification → `--no-ff` merge → worktree cleanup
→ index.yaml update → qa doc sync.

---

## Tasks

### Step 1: Identify the PR to merge

#### Condition

- Always — run first

#### Process

1. Read `docs/tasks/index.yaml` and list in-progress PRs (`completed: false`)
2. If multiple exist, ask the user which one to merge
3. Confirm the branch name: `PR{N}/{type}/{description}`

→ Proceed to Step 2

#### Output

- Target PR number and branch name confirmed

---

### Step 2: Verify the task checklist

#### Condition

- Step 1 complete

#### Process

1. Read `## 作業内容` in `docs/tasks/{task_folder}/PR{N}.md`
2. Confirm no unchecked items (`- [ ]`) remain

→ Proceed to Step 3 only if all items are `- [x]`

#### Output

- All tasks confirmed complete

#### Notes

##### Branching

- Unchecked tasks remain → do not merge; inform the user and stop

---

### Step 3: Execute the merge

#### Condition

- All tasks complete

#### Process

1. Confirm the current branch is master/main
2. Merge with `--no-ff`:

```bash
git merge --no-ff -m "{type}({scope}): {description} #PR{N}" PR{N}/{type}/{description}
```

→ Proceed to Step 4

#### Output

- Merge commit created

---

### Step 4: Remove the worktree and branch

#### Condition

- Merge complete

#### Process

1. Remove the worktree:

```bash
git worktree remove ../$(basename $(pwd))-wt-PR{N}
git branch -d PR{N}/{type}/{description}
```

→ Proceed to Step 5

#### Output

- Worktree and branch deleted

#### Notes

##### Prohibitions

- Never run `Remove-Item -Recurse` or `rm -rf` at the worktree root — it follows junctions
  and destroys files in the main repository

---

### Step 5: Update documents

#### Condition

- Worktree removed

#### Process

1. Set `completed: true` for the PR in `docs/tasks/index.yaml`
2. Review `docs/tasks/qa.md` and move resolved items to `docs/tasks/qa_history.md`
3. Commit if there are changes:

```bash
git add docs/tasks/
git commit -m "docs: post-merge update for PR{N}"
```

→ Proceed to Step 6

#### Output

- `index.yaml` updated to `completed: true`
- `qa.md` and `qa_history.md` synced

---

### Step 6: Report completion

#### Process

1. Report merge complete to the user
2. Show next in-progress PRs if any

#### Notes

##### Checklist

- [ ] Merge commit exists
- [ ] Worktree and branch deleted
- [ ] `index.yaml` set to `completed: true`
- [ ] `qa.md` reviewed and updated
