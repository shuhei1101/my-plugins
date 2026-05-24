---
name: merge
description: |
  Merge a PR: verify TODO checklist, archive index, merge with --no-ff, remove worktree and branch,
  and sync QA.md. Trigger when the user says "マージして", "merge して", or "PR をマージしたい".
  Never invoke automatically — only when the user explicitly requests a merge.
  ABSOLUTE RULE: Never execute git merge on your own initiative. Even if the user
  previously approved a merge in this session, you MUST receive a new explicit
  merge instruction for each PR. Past permission does not carry over.
disable-model-invocation: true
---

# work-kit:merge — Merge a PR

Runs the full merge flow: TODO checklist verification → master compatibility check → conversation-to-claude (if claude-kit installed) → index archive → `--no-ff` merge → worktree cleanup → QA doc sync.

---

## Critical Prohibition

> 🚫 **NEVER execute `git merge` without an explicit instruction from the user in the current message.**
>
> - Do NOT merge because a previous step completed successfully
> - Do NOT merge because the user approved a merge earlier in this session
> - Do NOT merge as part of "finishing up" or cleanup
> - Do NOT merge to "help" the user — wait to be asked
>
> **If the user did not say "マージして", "merge して", or an equivalent in their most recent message, STOP and ask before proceeding to Step 6.**
>
> Past permission does not carry over. Each merge requires a fresh, explicit instruction.

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

### Step 3: Confirm compatibility with master

#### Condition

- Step 2 complete

#### Process

1. Check whether master has new commits since this PR branch diverged:

```bash
git log HEAD..master --oneline
```

If no output → master has not moved; skip to Step 4.

2. Identify files that were changed both in master and in this PR branch:

```bash
# Files changed in this PR (compared to master)
git diff master...HEAD --name-only

# For each overlapping file, check master's commits on it
git log HEAD..master --oneline -- {file}
```

3. For each overlapping file, read the commit context from master:

```bash
git log -p HEAD..master -- {file}
```

4. Judge priority for each overlapping change — consider both:
   - **Recency**: which commit is newer?
   - **Background**: what was the purpose of master's change? Does it supersede or conflict with this PR?

5. Based on the judgment, take one of the following actions:
   - **No action needed**: changes are independent (different lines/sections, no logical conflict) → proceed to Step 4
   - **Incorporate master**: master has a related, newer change that should be reflected in this PR → merge master into the PR branch and adapt as needed:

```bash
git merge master
```

   Resolve any conflicts and update the PR's implementation to be compatible.
   - **Manual resolution required**: both sides have valid but contradictory intentions → report to user and stop; do not proceed until the user decides

→ Proceed to Step 4

#### Notes

##### Judgment guidelines

| Situation | Action |
|---|---|
| Master changed unrelated files only | No action — proceed |
| Master changed the same file but different sections | Merge master to stay current |
| Master changed the same logic this PR corrects | PR takes priority — proceed without merging |
| Master and PR changes are logically contradictory | Stop and ask the user |

##### When to stop and ask the user

Stop when the overlap involves core logic where the correct direction is unclear, or when merging master produces conflicts that cannot be resolved without user input.

---

### Step 4: Run conversation-to-claude (if claude-kit is installed)

#### Condition

- Step 3 complete

#### Process

1. Check whether `/claude-kit:conversation-to-claude` appears in the current session's available skill list
2. If available → invoke `/claude-kit:conversation-to-claude` and wait for it to complete
3. If not available → skip this step silently

→ Proceed to Step 5

#### Notes

- This step captures session knowledge before the branch is deleted
- Do not skip even if the conversation seems short — let the skill decide what to persist

---

### Step 5: Mark the PR as completed in index.yaml

#### Condition

- Step 4 complete

#### Process

1. Run the following command to mark the PR as `completed: true` in the main repository's `index.yaml`:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/index-tool.py" set-completed \
  .work/tasks/index.yaml --id {N}
```

→ Proceed to Step 6

#### Notes

- Run from the **main repository** directory (not the worktree) — `index.yaml` is gitignored and exists only in the main repo
- No commit is needed for `index.yaml` itself — it remains gitignored

---

### Step 6: Archive completed index entries

#### Condition

- Step 5 complete

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

→ Proceed to Step 7

#### Notes

- `index.yaml` remains gitignored — no commit needed for it
- `index.archive.yaml` is git-tracked — commit it to the **PR branch** (not directly to the parent branch); it will be included in the --no-ff merge in Step 7
- The archive command reads from the main repo's `index.yaml` and writes to the worktree's `index.archive.yaml`

---

### Step 7: Execute the merge

#### Condition

- Step 6 complete

> ⚠️ **Pre-merge check required**
> If `index.archive.yaml` was not committed in the worktree in Step 6, the archive changes will be missing from the merge commit.
> **Confirm that the `git commit` inside the worktree in Step 6 has completed before running the merge command.**
> (Skip this check only if Step 6 reported 0 entries moved — no commit was needed.)

#### Notes

##### Prohibitions

> 🚫 **ABSOLUTE PROHIBITION — read before executing**
>
> - NEVER run `git merge` unless the user explicitly said "マージして" or equivalent **in the message that triggered this skill invocation**.
> - Even if all previous steps completed without issue, you MUST stop here and confirm with the user before merging.
> - A user approval given earlier in the same session does NOT authorize this merge. Request confirmation again.
> - If in doubt, ask: "Step 1–6 が完了しました。マージを実行してよいですか？"

#### Process

1. Confirm the current branch is the parent branch the PR was branched from (e.g., `master` if branched from `master`, `develop` if branched from `develop`)
2. Merge with `--no-ff`:

```bash
git merge --no-ff -m "{type}: {title} #PR{N}" PR{N}/{type}/{title}
```

→ Proceed to Step 8

---

### Step 8: Remove the worktree and branch

#### Process

1. Remove the worktree and branch:

```bash
git worktree remove ../$(basename $(pwd))-wt-PR{N}
git branch -d PR{N}/{type}/{title}
```

→ Proceed to Step 9

#### Notes

##### Prohibitions

- Never run `Remove-Item -Recurse` or `rm -rf` at the worktree root

---

### Step 9: Update QA.md

#### Process

1. Review `.work/tasks/{date}_{title}/PR{N}/QA.md` and confirm any remaining unresolved entries with the user
2. Commit if there are changes:

```bash
git add .work/
git commit -m "docs: post-merge update for PR{N}"
```

→ Proceed to Step 10

---

### Step 10: Report completion

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
