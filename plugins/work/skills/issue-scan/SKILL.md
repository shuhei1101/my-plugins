---
name: issue-scan
description: |
  Pick source files at random from the project and Read them; compare them against the references
  that ref-inject hooks auto-inject, and record any rule violations or improvements as issues
  in `.work/issues/`. Automatically creates a scan branch, commits results, and merges to master.
  Excludes already-scanned files via `_index.archive.yaml`.
  ISSUE_SCAN_AGENTS controls how many files are scanned per invocation (default: 1).
  Trigger when the user says "issue-scan", "scan for issues", "find problems in the code",
  "コードをスキャン", "イシューを探して", or invokes `/work:issue-scan` explicitly.
---

# work:issue-scan — Scan Codebase for Issues

Picks source files at random per invocation and Reads them. ref-inject hooks
auto-inject the applicable references. The skill then compares the files against those
references and records discovered problems via `/work:issue-save`.
Creates a temporary scan branch, commits all findings, and merges to master automatically.

---

## Overview

**Prerequisites**:
- `.work/issues/` must exist (run `/work:setup` if it doesn't)

**Environment variables**:
- `ISSUE_SCAN_AGENTS` (default: `1`) — number of files to scan per invocation.
  `1` = single scan in the main agent (no subagents). `2+` = parallel subagents, one file each.

**Approach**:
- ref-inject hooks resolve and inject the relevant references based on file type
- This skill picks target file(s), reads them (triggering reference injection), and compares against injected references
- The hook's session+file-hash token ensures each file is injected once per session
- Each invocation creates a temporary `chore/issue-scan-*` branch, commits findings, and merges to master with `--no-ff`

---

## Tasks

### Step 0: Initialize scan branch

#### Condition

- Always — run first

#### Process

1. Read `ISSUE_SCAN_AGENTS` env var (default `1`); store as `N`
2. Verify the current branch is `master` (or `main`):
   ```bash
   git branch --show-current
   ```
   - If not on master/main → skip auto-branch/merge (Steps 7); commit directly to the current branch at the end
3. Create a temporary scan branch and switch to it:
   ```bash
   BRANCH="chore/issue-scan-$(date +%Y%m%d-%H%M%S)"
   git checkout -b "$BRANCH"
   ```

→ Proceed to Step 1

#### Output

- `BRANCH` name (e.g. `chore/issue-scan-20260531-143022`)
- `N` = number of parallel scan agents
- `AUTO_MERGE` = true if started from master/main, false otherwise

---

### Step 1: Read scan history

#### Condition

- Always — run after Step 0

#### Process

1. Check whether `.work/issues/` exists
   - If not → prompt for `/work:setup` and stop
2. Read `_index.archive.yaml` (treat as empty if missing)
   - Collect all `scan_records` entries (files already scanned)
   - Collect `closed_issues` whose `resolution: wontfix` (to exclude from results)

→ Proceed to Step 2

#### Output

- Set of already-scanned file paths
- Set of wontfix issue IDs

---

### Step 2: Pick N target files at random

#### Condition

- Always — run after Step 1

#### Process

1. Enumerate the project's source files
   - Use `find` or glob: `**/*.py`, `**/*.ts`, `**/*.tsx`, `**/*.html`, `**/*.js`, etc.
   - Exclude common non-source directories: `.work/`, `.git/`, `node_modules/`, `.venv/`,
     `venv/`, `__pycache__/`, `dist/`, `build/`, `.next/`, `.turbo/`
2. Remove files already present in `_index.archive.yaml`'s `scan_records[].scope`
3. Pick `N` remaining files at random (or all remaining if fewer than `N` are left)
4. If zero candidates remain: ask the user "All files have been scanned. Re-scan anyway?" —
   if yes, drop the exclusion and pick again; if no, stop (still merge the empty scan branch)

→ Proceed to Step 3

#### Output

- List of chosen file paths (1 to N paths)

---

### Step 3: Read files and receive references

#### Condition

- Always — run after Step 2

#### Process

**If N = 1 (single-agent mode):**

1. Read the chosen file (the primary scan target)
2. If a ref-inject `PreToolUse(Read)` hook matches, its `decision: block` response will inject the
   applicable reference bodies into the conversation as `reason`
3. **Also Read related files to build context**:
   - Sibling files in the same folder (e.g. for `features/chat/service.py`, also `types.py`, `route.py`, `query.py`)
   - Files the primary target depends on / files that call into the primary target (follow imports)
   - The whole related layer when the issue might span a layer (e.g. read the rest of the LLM folder)
   - Keep the related-file set as small as needed for sound judgement — do not over-expand
   - Related files are not the scan target; do NOT record them in `scan_records.scope`
4. If no injection occurred, treat the file as "no applicable ref-inject reference" and skip to Step 6
   (still write the scan record)

→ N=1 with injection → Step 4 / N=1 without injection → Step 6

**If N ≥ 2 (parallel subagent mode):**

1. [subagent: parallel · await all] For each chosen file path, spawn a subagent that reads the file, receives any injected references, also reads sibling/related files for context, and compares the primary file against the references
   (return: `[{title, type, priority, tags, scope, problem, suggested_fix, horizontal_notes}]` — empty list if no issues found)
2. Flatten all returned issue lists into a single findings list

→ N≥2 → Step 5

#### Output

- N=1: primary file content + related files + injected references (may be absent)
- N≥2: combined findings list from all subagents

---

### Step 4: Compare the file against references to find issues

#### Condition

- Only if Step 3 (N=1 path) produced injected references

#### Process

1. Compare the primary file (and related files from Step 3 where useful) against each injected
   reference, looking for:
   - Convention violations (naming, types, comments, style)
   - Architectural violations (dependency direction, layer boundaries)
   - Improvement opportunities (DRY violations, dead code, outdated patterns — anything the references call out)
   - Maintainability issues (duplicated logic, dual-source management, uncentralized configuration, shared boilerplate not extracted to a utility)
   - Cross-cutting problems (issues likely to exist in similar form across other files — note these for horizontal expansion)
2. Related files are used as judgement material; the issues themselves are raised against the
   primary target file (mention related-file problems inline, or defer them to a later scan)
3. Drop findings that match an already-`wontfix` closed issue
4. Group findings into independently actionable units
5. For each finding, note whether the same pattern likely appears elsewhere in the codebase
   (horizontal expansion candidate)

→ Proceed to Step 5

#### Output

- List of discovered problems (title / type / priority / location / suggested fix / horizontal notes)

---

### Step 5: Save issues

#### Condition

- Only if Step 4 (or Step 3 N≥2 path) found one or more problems

#### Process

1. For each discovered problem, invoke `/work:issue-save`:
   - Pass title / type / priority / tags / scope (= chosen file path) / problem description / suggested fix / horizontal expansion notes
   - Collect the ISSUE IDs returned by issue-save

→ Proceed to Step 6

#### Output

- List of created issue IDs

---

### Step 6: Update the scan record

#### Condition

- Always — even if no issues were found, the scan record must still be written for every scanned file

#### Process

1. For each scanned file, append to `_index.archive.yaml`'s `scan_records`:
   ```yaml
   scan_records:
     - date: {YYYY-MM-DD}
       skill: issue-scan
       scope: "{chosen file path}"
       issues_found: [{ISSUE-N}, ...]   # empty list if zero found
   ```
2. If `_index.archive.yaml` does not exist yet, create it with `closed_issues: []` and `scan_records: []`

→ Proceed to Step 7

---

### Step 7: Commit and merge to master

#### Condition

- Always — run after Step 6

#### Process

1. Stage all new and updated files under `.work/issues/`:
   ```bash
   git add .work/issues/
   ```
2. If there are staged changes, commit on the scan branch:
   ```bash
   git commit -m "chore: issue-scan — {N} file(s) scanned, {M} issue(s) found"
   ```
   - If nothing to stage (no issues found and archive record was the only change), still commit the archive update
3. If `AUTO_MERGE` is true (started from master/main):
   ```bash
   git checkout master
   git merge --no-ff {BRANCH} -m "chore: merge issue-scan results from {BRANCH}"
   git branch -d {BRANCH}
   ```
4. If `AUTO_MERGE` is false (started from a feature branch): leave the scan branch as-is and notify the user that manual merge is needed

→ Proceed to Step 8

---

### Step 8: Report results

#### Condition

- Always — run last

#### Process

1. Report to the user:
   - The scanned file path(s)
   - Whether references were injected for each file (if not, no ref-inject hook applies to that file)
   - Number of issues created and their list (ID / title / priority)
   - If zero issues, state that the file(s) look clean
   - The scan branch that was merged (or left open if AUTO_MERGE was false)
2. Mention that issues can be closed with `resolution: wontfix` if no fix is planned
