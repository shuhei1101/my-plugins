[work] **Before processing this prompt, complete the steps below. No skipping. No exceptions.**

---

### Step 1: Determine whether a branch is in progress

#### Condition

- Always run this first

#### Process

Check whether a working branch is in progress in **the current Claude Code conversation session**.

→ Branch exists → proceed to Step 2
→ No branch → proceed to Step 3

#### Notes

- "In-progress branch" means a working branch that was created or explicitly mentioned within this conversation.
- Do NOT read `index.yaml` or any other files to look for in-progress branches.
- If unsure, treat it as "no branch" and proceed to Step 3.

---

### Step 2: Check QA before reading the rest of the task document

#### Condition

- A branch is in progress

#### Process

1. Use `git worktree list` to locate the in-progress branch's worktree and navigate to it
2. Read the task document at `.work/tasks/{YYMMDD}_{title}/{YYMMDD}-{日本語タイトル}.task.md` (the single `.md` file in the task folder)
3. If its `## QA` section has unresolved entries — **stop here** — ask the user to resolve them; do nothing further
4. If `## QA` is clear (or empty), read the `## 作業内容` section of the same task document
5. If the user's requested task is not already listed in `## 作業内容`, add it and commit before proceeding
6. Continue work according to the document

#### Notes

##### Prohibitions

- Continuing implementation while QA entries remain unresolved
- Running git commit while on the master branch

---

### Step 3: No branch in progress — choose the entry point

#### Condition

- No working branch is in progress

#### Process

1. Judge whether the request needs a git branch — i.e. will it produce **committable changes to
   git-tracked files**?
   - **No** → run `/work:quick-task`. This covers investigation / confirmation only ("how does this
     work?", "what is the status of X?", reading code, explaining behavior) and edits limited to
     git-ignored or otherwise untracked files (never committed). Do **not** create a branch or worktree.
   - **Yes** → run `/work:start` to create a branch, then proceed to Step 2.

#### Notes

- When unsure whether the work will produce committable tracked changes, prefer `/work:start` — a
  branch is the safe default.
- If a `work:quick-task` turns out to require committable changes to tracked files, stop and switch
  to `/work:start`.

##### Prohibitions

- Committing changes to git-tracked files without running work:start first
- Committing directly to master
- Skipping this check "just this once"
