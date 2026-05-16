[work-kit] **Before processing this prompt, complete the steps below. No skipping. No exceptions.**

---

### Step 1: Determine whether a PR is in progress

#### Condition

- Always run this first

#### Process

Check whether a PR is in progress in the current session.

→ PR exists → proceed to Step 2
→ No PR → proceed to Step 3

---

### Step 2: Check QA before reading TODO

#### Condition

- A PR is in progress

#### Process

1. Use `git worktree list` to locate the in-progress PR's worktree and navigate to it
2. Read `.work/tasks/{YYYYMMDD}_{title}/PR{N}/QA.md`
3. If unresolved QA entries exist — **stop here** — ask the user to resolve them; do nothing further
4. If QA is clear (or empty), read `.work/tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md`
5. If the user's requested task is not already listed in TODO.md, add it and commit before proceeding
6. Continue work according to the TODO

#### Notes

##### Prohibitions

- Continuing implementation while QA entries remain unresolved
- Running `git commit` while on the master branch

---

### Step 3: Run work-start before doing anything

#### Condition

- No PR is in progress

#### Process

1. Run `/work-kit:work-start` to create a PR
2. Once the PR is created, proceed to Step 2

#### Notes

##### Prohibitions

- Editing or committing files without running work-start first
- Committing directly to master
- Skipping this check "just this once"
