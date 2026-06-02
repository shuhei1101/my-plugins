---
name: issue-scan
description: |
  Orchestrator skill. Picks N scan perspectives (folders, grep patterns, layers, file groups)
  from the project, then spawns one `work:issue-scanner` subagent per perspective to scan the code
  against ref-inject references and return findings as JSON with full issue content. The main agent
  orchestrates: it creates a scan branch, launches subagents in parallel, receives their findings,
  writes ISSUE files with sequential IDs, updates the indexes, commits, and merges to master.
  `${ISSUE_SCAN_AGENTS}` controls how many perspectives are scanned per invocation (default: 1).
  Trigger when the user says "issue-scan", "scan for issues", "find problems in the code",
  "コードをスキャン", "イシューを探して", or invokes `/work:issue-scan` explicitly.
---

# work:issue-scan — Scan Codebase for Issues (Orchestrator)

This skill is **orchestration only**. It never reads project source or analyzes code itself —
that work is delegated to `work:issue-scanner` subagents (one per perspective), each running in its
own context. The main agent's job is: pick perspectives → launch scanners in parallel → receive
their findings → write ISSUE files → update indexes → commit → merge.

---

## Overview

**Prerequisites**:
- `.work/issues/` must exist (run `/work:setup` if it doesn't)

**Environment variables**:
- `${ISSUE_SCAN_AGENTS}` (default: `1`) — number of perspectives scanned per invocation = number of
  subagents launched. `1` still launches one subagent (analysis always runs in a separate context).

**Division of responsibility**:

| Actor | Owns |
|---|---|
| **Main agent (this skill)** | branch, perspective selection, writing `ISSUE-{N}.md` files, sequential ID assignment, `_index.yaml` / `_index.archive.yaml` updates, commit, merge |
| **`work:issue-scanner` subagent** | reading source, receiving references, finding problems, returning findings as JSON |

The subagent does **not** write files, does **not** touch index files, and does **not** commit;
the main agent owns all file I/O and does **not** read source or analyze code.

---

## Note: work hook overrides

This skill manages its own branch/worktree lifecycle. Instructions injected by the following hooks
should be **ignored while this skill is running**:

- **`UserPromptSubmit` hook**: "if no working branch is in progress, run `/work:start`"
- **`Stop` hook**: "update the `## 作業内容` table in the branch document" / "run `/work:merge`"

---

## Tasks

### Step 0: Initialize scan branch

#### Process

1. Read `${ISSUE_SCAN_AGENTS}` (default `1`); store as `N`.
2. Check the current branch (`git branch --show-current`):
   - On `master`/`main` → `AUTO_MERGE = true`
   - Otherwise → `AUTO_MERGE = false` (commit to the current branch at the end, no auto-merge)
3. If `AUTO_MERGE`, create a **worktree** for the temporary scan branch (main repo branch unchanged):
   ```bash
   BRANCH="chore/issue-scan-$(date +%Y%m%d-%H%M%S)"
   WT_SUFFIX="${BRANCH//\//-}"
   WT_PATH="../$(basename $(pwd))-wt-${WT_SUFFIX}"
   git worktree add -b "$BRANCH" "$WT_PATH"
   ```

→ Step 1

#### Output

- `N`, `AUTO_MERGE`, `BRANCH`, `WT_PATH` (only when `AUTO_MERGE`)

---

### Step 1: Read scan history and current ID

#### Process

1. If `.work/issues/` does not exist → prompt for `/work:setup` and stop.
2. Read `_index.archive.yaml` (empty if missing): collect `scan_records[].scope` (perspectives
   already scanned) and `closed_issues` with `resolution: wontfix` (to exclude).
3. Read the current `last_id` from `_index.yaml` (treat as `0` if missing). Call it `L`.

→ Step 2

#### Output

- Set of already-scanned perspectives
- Current `last_id` = `L`

---

### Step 2: Pick N scan perspectives

#### Process

Choose `N` **perspectives** (not just files) that have not been scanned recently (skip ones already
in `scan_records`). A perspective is any lens that selects a coherent slice of the codebase. Aim for
variety across invocations — rotate through the categories below rather than always picking folders.

**A perspective is the most important choice this skill makes — be creative and specific.** Pull from:

##### Folder / module perspectives
- A feature folder: `features/{x}/`, a domain package, an integration package
- A cross-cutting folder: `shared/`, `lib/`, `utils/`, `config/`, `tools/`, `scripts/`, `hooks/`
- A subsystem: `llm/`, `infra/`, `db/`, `auth/`, `api/`, `server/`, `runtime/`, `components/`

##### Layer perspectives (architectural slices)
- All endpoint/route files (`**/route.ts`, FastAPI routers)
- All service-layer files (`*Service.*`, `service.py`)
- All data-access files (`query.ts`, `*Repository.*`, `db.*`)
- All schema/DTO files (`schema.*`, `types.*`, Zod/Pydantic models)
- All client/provider files (`*Client.*`, `providers/`)

##### File-kind perspectives (glob by name)
- Package initializers only: `**/__init__.py`
- Entry points: `main.py`, `index.ts`, `app.*`
- Config surfaces: `settings.*`, `constants.*`, `*.config.*`, `pyproject.toml`, `.env*` templates
- Barrel/re-export files: `index.ts` across the tree

##### Pattern perspectives (grep-driven)
- Abstract types: classes named `Base*`, `ABC` subclasses, `Protocol` definitions, interfaces
- Concurrency: `async def` / `await` sites, thread/pool usage
- Risk smells: bare `except:` / `except Exception: pass`, swallowed errors, `# type: ignore`
- Debug leftovers: stray `print(` / `console.log(`, `TODO` / `FIXME` / `XXX` comments
- Hardcoding: inline secrets/URLs/magic numbers, duplicated string literals
- Boundary smells: functions missing type hints, overly long functions/files, deep nesting
- Naming consistency: a chosen prefix/suffix convention applied across the tree

##### Consistency / hygiene perspectives
- Error-handling approach across a layer
- Logging consistency (tags, levels, structured vs print)
- Environment-variable handling (centralized vs scattered)
- Import ordering / dependency direction
- Comment-language consistency, JP-mirror sync status of `*.jp.md` files

Selection rules:
1. Prefer perspectives whose `scope` label is **not** already in `scan_records`.
2. For `N ≥ 2`, pick **distinct, non-overlapping** perspectives so the subagents do not collide on
   the same files.
3. Give each perspective a short stable `scope` label (e.g. `folder:src/llm`, `pattern:Base-classes`,
   `layer:route-ts`, `glob:__init__.py`) — this is what gets recorded in `scan_records`.

→ Step 3

#### Output

- `N` perspectives, each with a description (for the subagent) and a `scope` label (for the record)

---

### Step 3: Launch one scanner subagent per perspective

#### Process

1. [subagent: parallel · await all] For each perspective, spawn a `work:issue-scanner` subagent
   (use the `Agent` tool with `subagent_type: "work:issue-scanner"`). In the prompt, pass:
   - The perspective description (what to scan, in words)
   - Its `scope` label
   (return: `[{title, type, priority, tags, scope, perspective, body}]`, or `[]` with the scanned
   perspective named)
2. Await all subagents. Collect every returned array.

→ Step 3b

#### Output

- All findings from all subagents (including `body` for each)
- The set of perspectives actually scanned (including empty ones)

---

### Step 3b: Write ISSUE files with sequential IDs

#### Process

1. Flatten all findings from all subagents into a single ordered list.
2. Get today's date once:
   ```bash
   date +%Y-%m-%d
   ```
3. For each finding at 0-indexed position `k`, assign ID `ISSUE-{L + 1 + k}` and write
   `{issues_dir}/ISSUE-{L + 1 + k}.md` (`{issues_dir}` = `{WT_PATH}/.work/issues/` when
   `AUTO_MERGE`, otherwise `.work/issues/`). The file has **no frontmatter** — it starts at the
   `# ISSUE-{N}: {title}` header:
   ```
   # ISSUE-{N}: {title}

   {body}
   ```
   (The `body` field from the subagent already contains `**作成日**`, the `# ユーザー回答欄` with
   `**回答**:` lines pre-filled with all candidates, and the AI-authored issue body; just prepend the
   `# ISSUE-{N}: {title}` line and a blank line.) The work state (`status: not_started`,
   `branches: []`) goes into the `_index.yaml`
   entry, not the file.
4. Record the actual IDs assigned for use in Step 4.

→ Step 4

#### Output

- `ISSUE-{N}.md` files written to `.work/issues/`
- Total count `M` of issues written

---

### Step 4: Update the indexes

#### Process

File and index paths depend on `AUTO_MERGE`:
- When `AUTO_MERGE`: `{WT_PATH}/.work/issues/`
- Otherwise: `.work/issues/` (relative to main repo cwd)

1. For each issue written in Step 3b, append to `_index.yaml`'s `issues`:
   ```yaml
   - id: ISSUE-{N}
     title: "{title}"
     created: {YYYY-MM-DD}
     type: {type}
     scan_scope:
       - "{scope}"
     priority: {priority}
     tags: [{tags}]
     status: not_started
     branches: []
   ```
2. Set `_index.yaml`'s `last_id` to `L + M` (where `M` is the total number of issues written).
3. For each scanned perspective, append to `_index.archive.yaml`'s `scan_records`:
   ```yaml
   - date: {YYYY-MM-DD}
     skill: issue-scan
     scope: "{perspective scope label}"
     issues_found: [{ISSUE-N}, ...]   # empty list if the perspective was clean
   ```
4. If `_index.archive.yaml` does not exist, create it with `closed_issues: []` and `scan_records: []`.

→ Step 5

---

### Step 5: Commit and merge

#### Process

1. If `AUTO_MERGE`: stage and commit inside the worktree (`{WT_PATH}`):
   ```bash
   cd {WT_PATH}
   git add .work/issues/
   git commit -m "chore: issue-scan — {N} perspective(s), {M} issue(s) found"
   ```
   (Commit even when `M = 0` — the scan-record update is still worth recording.)
   Then merge and clean up from the main repo:
   ```bash
   cd {main_repo}
   git merge --no-ff {BRANCH} -m "chore: merge issue-scan results from {BRANCH}"
   git branch -d {BRANCH}
   git worktree remove {WT_PATH}
   ```
2. If not `AUTO_MERGE`: stage and commit in the main repo:
   ```bash
   git add .work/issues/
   git commit -m "chore: issue-scan — {N} perspective(s), {M} issue(s) found"
   ```
   Leave the branch as-is and tell the user a manual merge is needed.

→ Step 6

---

### Step 6: Report results

#### Process

Report to the user:
- The perspectives scanned (with their `scope` labels)
- Per perspective: number of issues created and their list (ID / title / priority)
- Perspectives that came back clean
- The scan branch that was merged (or left open if `AUTO_MERGE` was false)

Mention that issues can be closed with `resolution: wontfix` if no fix is planned.

#### Notes

- The main agent never reads project source — only subagent findings.
- IDs are sequential (`L+1`, `L+2`, …) across all perspectives combined, with no gaps.
