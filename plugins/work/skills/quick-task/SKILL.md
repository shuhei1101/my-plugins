---
name: work:quick-task
description: |
  Handle a lightweight task — work that does NOT mainly edit source code: investigation,
  confirmation, research, reading code, explaining behavior ("how does this work?", "what is the
  status of X?", "look into Y"). Invoked by the work UserPromptSubmit hook when a request is not
  primarily source-code implementation, or explicitly via /work:quick-task. Creates a branch and a
  lightweight task document that records the findings, and commits it (branching and saving are
  expected — not restricted). Lighter than work:start: the document and lifecycle stay minimal (no
  implementation/QA gate, no mandatory note, no merge ceremony). If the work turns into source-code
  implementation, switch to /work:start.
---

# work:quick-task — Lightweight Task (Investigation)

For work that is **not mainly source-code editing** — investigation, confirmation, research,
explaining how something works. Creates a branch and a lightweight task document recording the
findings, then commits it. Saving on a branch is the norm; there is no restriction against
branching or committing.

> Counterpart to `work:start`. `work:start` is for **source-code implementation**; `work:quick-task`
> is for **investigation / non-implementation** work. Both create a branch + task document — but
> quick-task keeps the document and lifecycle light.

---

## Tasks

### Step 1: Confirm this is a lightweight task

#### Condition

- Always — run first

#### Process

1. Confirm the request is **not mainly source-code editing** — it is investigation, confirmation,
   research, reading code, or explaining behavior.
2. **If the request is mainly source-code implementation** → run `/work:start` instead.

→ Proceed to Step 2

#### Notes

- The deciding factor is whether the work mainly edits source code, **not** whether files change at
  all. A quick task may still touch files (e.g. write its own task document).

---

### Step 2: Create a branch + lightweight task document

#### Condition

- Step 1 confirmed this is a lightweight task

#### Process

1. Decide a branch name `{type}/{title}` — investigation work is usually `docs/` or `chore/`. Insert
   the author segment when `${WORK_BRANCH_AUTHOR}` is set (`{type}/{author}/{title}`).
2. Add the index entry in the main repository:

   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py add .work/tasks/index.yaml \
     --branch "{full-branch-name}" \
     --title "{日本語タイトル}" \
     --type {type} \
     --summary "{summary}" \
     --task "{YYMMDD}_{title}"
   ```

3. Create the branch (and worktree, unless `${WORK_USE_WORKTREE}` is falsy): invoke
   `/work:worktree-create {full-branch-name}`.
4. Inside the branch, author a **lightweight** task document at
   `.work/tasks/{YYMMDD}_{title}/{YYMMDD}-{日本語タイトル}.task.md`. The `task-document` template is
   auto-injected when you write a `*.task.md` file — fill only what a quick task needs: the H1 title,
   `> ブランチ:`, `## 概要`, and a findings section. The implementation/test sections may be left as
   placeholders or removed.

→ Proceed to Step 3

#### Notes

- Use a 6-digit `YYMMDD`. `index.yaml` is git-ignored — no master commit is needed for it.

---

### Step 3: Investigate, record, and save

#### Condition

- Step 2 complete

#### Process

1. Perform the investigation on the branch and record the findings in the task document's `## 概要`
   / findings section.
2. Commit the task document on the branch.
3. quick-task keeps the lifecycle light: there is **no** "resolve QA before implementing" gate, **no**
   mandatory `.work/notes/` update, and **no** merge requirement. Suggest `/work:merge` only if the
   user wants the branch merged.

→ Done.

#### Notes

- If source-code implementation becomes necessary mid-task, continue on this branch following the
  `work:start` lifecycle (or run `/work:start`).
