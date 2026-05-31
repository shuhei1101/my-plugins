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

### Step 2: Check QA before reading the rest of the branch document

#### Condition

- A branch is in progress

#### Process

1. Use `git worktree list` to locate the in-progress branch's worktree and navigate to it
2. Read the branch document at `.work/tasks/{YYMMDD}_{title}/{YYMMDD}-{日本語タイトル}.md` (the single `.md` file in the task folder)
3. If its `## QA` section has unresolved entries — **stop here** — ask the user to resolve them; do nothing further
4. If `## QA` is clear (or empty), read the `## 作業内容` section of the same branch document
5. If the user's requested task is not already listed in `## 作業内容`, add it and commit before proceeding
6. Continue work according to the document

#### Notes

##### Prohibitions

- Continuing implementation while QA entries remain unresolved
- Running git commit while on the master branch

---

### Step 3: Run work:start before doing anything

#### Condition

- No working branch is in progress

#### Process

1. Run `/work:start` to create a branch
2. Once the branch is created, proceed to Step 2

#### Notes

##### Prohibitions

- Editing or committing files without running work:start first
- Committing directly to master
- Skipping this check "just this once"
