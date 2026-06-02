---
name: quick-task
description: |
  Handle a lightweight task that does NOT need a git branch. Two cases qualify: (1) investigation /
  confirmation only — "how does this work?", "what is the status of X?", "look into Y", reading code,
  explaining behavior; (2) changes limited to git-ignored or otherwise untracked files (which are
  never committed). Invoked by the work UserPromptSubmit hook when the request needs no committable
  change to git-tracked files, or explicitly via /work:quick-task. Does NOT create a branch,
  worktree, index entry, QA gate, or merge. If the work turns out to require committable changes to
  tracked files, stop and switch to /work:start.
---

# work:quick-task — Lightweight Task (No Branch)

For work that does not warrant a git branch: pure investigation/confirmation, and edits limited to
git-ignored or untracked files. This skill skips the whole branch lifecycle (no worktree, no
`index.yaml` entry, no QA gate, no merge) so simple requests stay simple.

> This is the lightweight counterpart to `work:start`. `work:start` is for implementation that will
> be **committed to tracked files**; `work:quick-task` is for everything that will not.

---

## Tasks

### Step 1: Confirm this is a quick task

#### Condition

- Always — run first

#### Process

1. Confirm the request fits one of these (no git branch needed):
   - **Investigation / confirmation only** — answering a question, reading code, explaining how
     something works, checking status. No file changes.
   - **Untracked-only changes** — the only files to edit are git-ignored or otherwise untracked
     (verify with `git check-ignore -v <path>` / `git status` when unsure). These are never
     committed, so no branch is needed.
2. **If the work will require committable changes to git-tracked files** → stop and run `/work:start`
   instead (this skill is the wrong entry point).

→ Proceed to Step 2

#### Notes

- When unsure whether tracked files will need committing, prefer `/work:start` — a branch is the safe default.

---

### Step 2: Do the work

#### Condition

- Step 1 confirmed this is a quick task

#### Process

1. Perform the investigation or the untracked-file edit directly on the current checkout.
   - No worktree, no new branch.
2. Report findings / what was done to the user in the response.

→ Proceed to Step 3

#### Notes

##### Prohibitions

- Do not create a worktree or a git branch
- Do not add an entry to `.work/tasks/index.yaml`
- Do not commit changes to git-tracked files (if such a change becomes necessary, switch to `/work:start`)

---

### Step 3: Optionally record a task document

#### Condition

- The investigation/result is substantial enough to be worth keeping, **or** the user asks for a record

#### Process

1. Write a lightweight task document at
   `.work/tasks/{YYMMDD}_{title}/{YYMMDD}-{日本語タイトル}.task.md` capturing the request and the
   findings. The `task-document` reference template is auto-injected when you write a `*.task.md`
   file — author from it, filling only the sections that apply (a quick task typically needs just
   `# title`, `## 概要`, and a short findings section).
2. Leave the document **uncommitted** — it is a working record. The user commits it later if they
   want it kept, or it is absorbed into a future branch. `work:quick-task` never commits.

→ Done.

#### Notes

- Skip this step entirely for trivial questions — do not create a document for every quick answer.
- Recording is opt-in: keep `quick-task` lightweight.
