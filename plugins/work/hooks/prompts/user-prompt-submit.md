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

1. Judge whether the request **mainly edits source code**.
   - **No** (investigation / confirmation / research / reading code / explaining behavior — "how does
     this work?", "what is the status of X?", "look into Y") → run `/work:quick-task`. It creates a
     branch + a lightweight task document recording the findings.
   - **Yes** (source-code implementation) → run `/work:start` to create a branch, then proceed to Step 2.

#### Notes

- Both entry points create a branch and a task document; the difference is the nature of the work
  (investigation vs source-code implementation) and how light the lifecycle is.
- If a `work:quick-task` turns into source-code implementation, continue under the `work:start`
  lifecycle on the same branch.

##### Prohibitions

- Editing or committing without running `work:start` or `work:quick-task` first
- Committing directly to master
- Skipping this check "just this once"
