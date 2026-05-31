---
name: issue-scan
description: |
  Orchestrator skill. Picks N scan perspectives (folders, grep patterns, layers, file groups)
  from the project, then spawns one `work:issue-scanner` subagent per perspective to scan the code
  against ref-inject references and write findings as issues in `.work/issues/`. The main agent
  only orchestrates: it creates a scan branch, allocates ID blocks, launches subagents, then
  aggregates their metadata, updates the indexes, commits, and merges to master.
  ISSUE_SCAN_AGENTS controls how many perspectives are scanned per invocation (default: 1).
  Trigger when the user says "issue-scan", "scan for issues", "find problems in the code",
  "コードをスキャン", "イシューを探して", or invokes `/work:issue-scan` explicitly.
---

# work:issue-scan — Scan Codebase for Issues (Orchestrator)

This skill is **orchestration only**. It never reads project source or analyzes code itself —
that work is delegated to `work:issue-scanner` subagents (one per perspective), each running in its
own context. The main agent's job is: pick perspectives → allocate ID blocks → launch scanners in
parallel → aggregate their returned metadata → update indexes → commit → merge.

Keeping analysis out of the main context is the whole point: issue bodies live in files written by
the subagents and never enter the orchestrator's context.

---

## Overview

**Prerequisites**:
- `.work/issues/` must exist (run `/work:setup` if it doesn't)

**Environment variables**:
- `ISSUE_SCAN_AGENTS` (default: `1`) — number of perspectives scanned per invocation = number of
  subagents launched. `1` still launches one subagent (analysis always runs in a separate context).

**Division of responsibility**:

| Actor | Owns |
|---|---|
| **Main agent (this skill)** | branch, perspective selection, ID-block allocation, `_index.yaml` / `_index.archive.yaml` updates, commit, merge |
| **`work:issue-scanner` subagent** | reading source, receiving references, finding problems, writing `ISSUE-{N}.md` files |

The subagent does **not** touch the index files and does **not** commit; the main agent does **not**
read source or analyze code.

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

1. Read `ISSUE_SCAN_AGENTS` (default `1`); store as `N`.
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

1. Allocate a non-overlapping ID block to each perspective. With `SLOT = 30`, perspective `i`
   (0-indexed) gets start ID `START_i = L + 1 + i * SLOT`. Each subagent uses `ISSUE-{START_i}`,
   `ISSUE-{START_i + 1}`, … for its findings — blocks never overlap, so parallel writes never collide.
2. [subagent: parallel · await all] For each perspective, spawn a `work:issue-scanner` subagent
   (use the `Agent` tool with `subagent_type: "work:issue-scanner"`). In the prompt, pass:
   - The perspective description (what to scan, in words)
   - Its `scope` label
   - Its start ID `START_i`
   - Issue file output path: `{WT_PATH}/.work/issues/` when `AUTO_MERGE`,
     or `.work/issues/` (relative to main repo cwd) otherwise
   (return: the compact metadata array `[{id, title, type, priority, tags, scope, perspective}]`,
   or `[]` with the scanned perspective named)
3. Await all subagents. Collect every returned metadata array.

→ Step 4

#### Output

- Combined metadata for all created issues (bodies are already on disk — not in context)
- The set of perspectives actually scanned (including empty ones)

---

### Step 4: Update the indexes

#### Process

The index file paths depend on `AUTO_MERGE`:
- When `AUTO_MERGE`: `{WT_PATH}/.work/issues/_index.yaml` / `_index.archive.yaml`
- Otherwise: `.work/issues/_index.yaml` / `_index.archive.yaml` (main repo)

1. For each returned issue metadata, append to `_index.yaml`'s `issues`:
   ```yaml
   - id: ISSUE-{N}
     title: "{title}"
     created: {YYYY-MM-DD}
     type: {type}
     scan_scope:
       - "{scope}"
     priority: {priority}
     tags: [{tags}]
   ```
2. Set `_index.yaml`'s `last_id` to `L + N * SLOT` (the whole reserved range is consumed; IDs may be
   non-contiguous across parallel scans — this is expected and harmless).
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

- The main agent never reads project source or issue bodies — only subagent metadata.
- IDs are intentionally non-contiguous under parallel scanning (each subagent owns a reserved block).
