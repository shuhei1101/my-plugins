---
name: issue-scan
description: |
  Pick one source file at random from the project and Read it; compare it against the references
  that the matching `*-kit` plugin's auto-injection hook returns, and record any rule violations
  or improvements as issues in `.work/issues/`.
  Excludes already-scanned files via `_index.archive.yaml`.
  Trigger when the user says "issue-scan", "scan for issues", "find problems in the code",
  "コードをスキャン", "イシューを探して", or invokes `/work:issue-scan` explicitly.
---

# work:issue-scan — Scan Codebase for Issues

Picks one project file at random per invocation and Reads it. The `*-kit` plugins'
`PreToolUse(Read)` hooks auto-inject the applicable references. The skill then compares
the file against those references and records discovered problems via `/work:issue-save`.

---

## Overview

**Prerequisites**:
- `.work/issues/` must exist (run `/work:setup` if it doesn't)
- At least one `*-kit` plugin with a `PreToolUse(Read)` reference auto-injection hook
  (dev-kit, etc.) must be installed

**Approach**:
- The `*-kit` `PreToolUse(Read)` hooks resolve and inject the relevant references based on file type
- This skill therefore only needs to pick one target file and Read it
- The hook reads `_injection_rules.yaml` to decide which references apply; the skill does not
  re-implement pattern matching or YAML parsing
- The hook's session+file-hash token ensures each file is injected once per session

---

## Tasks

### Step 1: Read scan history

#### Condition

- Always — run first

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

### Step 2: Pick one target file at random

#### Condition

- Always — run after Step 1

#### Process

1. Enumerate the project's source files
   - Use `find` or glob: `**/*.py`, `**/*.ts`, `**/*.tsx`, `**/*.html`, `**/*.js`, etc.
   - Exclude common non-source directories: `.work/`, `.git/`, `node_modules/`, `.venv/`,
     `venv/`, `__pycache__/`, `dist/`, `build/`, `.next/`, `.turbo/`
2. Remove files already present in `_index.archive.yaml`'s `scan_records[].scope`
3. Pick one remaining file at random
4. If zero candidates remain: ask the user "All files have been scanned. Re-scan anyway?" —
   if yes, drop the exclusion and pick again; if no, stop

→ Proceed to Step 3

#### Output

- Chosen file path (e.g. `src/myapp/features/chat/service.py`)

---

### Step 3: Read the file and related files, then receive references

#### Condition

- Always — run after Step 2

#### Process

1. Read the file chosen in Step 2 (the primary scan target)
2. If a `*-kit` `PreToolUse(Read)` hook matches, its `decision: block` response will inject the
   applicable reference bodies into the conversation as `reason`
   - The injection contains the required / optional reference bodies for this file
3. **Also Read related files to build context**:
   - Sibling files in the same folder (e.g. for `features/chat/service.py`, also `types.py`, `route.py`, `query.py`)
   - Files the primary target depends on / files that call into the primary target (follow imports)
   - The whole related layer when the issue might span a layer (e.g. read the rest of the LLM folder)
   - Keep the related-file set as small as needed for sound judgement — do not over-expand
   - Related files are not the scan target, so do NOT record them in `scan_records.scope`
4. If no injection occurred, treat the file as "no applicable `*-kit` reference" and skip to Step 6
   (still write the scan record)

→ Injection present → Step 4 / No injection → Step 6

#### Output

- The primary file's content
- Related files' content (context only)
- Injected reference bodies (may be absent)

---

### Step 4: Compare the file against references to find issues

#### Condition

- Only if Step 3 produced injected references

#### Process

1. Compare the primary file (and related files from Step 3 where useful) against each injected
   reference, looking for:
   - Convention violations (naming, types, comments, style)
   - Architectural violations (dependency direction, layer boundaries)
   - Improvement opportunities (DRY violations, dead code, outdated patterns — anything the references call out)
2. Related files are used as judgement material; the issues themselves are raised against the
   primary target file (mention related-file problems inline, or defer them to a later scan)
3. Drop findings that match an already-`wontfix` closed issue
4. Group findings into independently actionable units

→ Proceed to Step 5

#### Output

- List of discovered problems (title / type / priority / location / suggested fix)

---

### Step 5: Save issues

#### Condition

- Only if Step 4 found one or more problems

#### Process

1. For each discovered problem, invoke `/work:issue-save`:
   - Pass title / type / priority / tags / scope (= chosen file path) / problem description / suggested fix
   - Collect the ISSUE IDs returned by issue-save

→ Proceed to Step 6

#### Output

- List of created issue IDs

---

### Step 6: Update the scan record

#### Condition

- Always — even if no issues were found, the scan record must still be written

#### Process

1. Append the following to `_index.archive.yaml`'s `scan_records`:
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

### Step 7: Report results

#### Condition

- Always — run last

#### Process

1. Report to the user:
   - The scanned file path
   - Whether references were injected (if not, no matching `*-kit` exists for this file)
   - Number of issues created and their list (ID / title / priority)
   - If zero issues, state that the file looks clean
2. Mention that issues can be closed with `resolution: wontfix` if no fix is planned

#### Notes

- Do NOT run `git commit` in this skill — the user reviews before committing
- Each file's injection slightly enlarges the context, but the `*-kit` session+file-hash token
  prevents re-injection on the same file within one session
