---
name: jp-mirror-sync
description: |
  Accept one or more Japanese mirror (.jp.md) files and create or update the corresponding English
  counterparts (.md). Treats the JP mirror as the source of truth and spawns one
  utils:jp-mirror-translator subagent per file, running all subagents in parallel.
  Trigger when the user says "JP ミラーを同期して", "英語版を更新して", "jp-mirror-sync して",
  "translate JP mirror", or passes one or more .jp.md file paths.
---

# utils:jp-mirror-sync — JP Mirror → English Sync

Accept one or more `.jp.md` file paths and spawn one `utils:jp-mirror-translator` subagent per
file. All subagents run in parallel.

---

## Tasks

### Step 1: Parse the file list

#### Input

File paths from skill args or the user's message

#### Process

1. Extract `.jp.md` file paths from the skill args or the user's message
   - Accept space-separated, quoted, or newline-separated paths
2. Validate that each path ends in `.jp.md`
3. If no paths are found, ask the user to provide them

→ Proceed to Step 2

#### Output

- List of `.jp.md` file paths to process

---

### Step 2: Launch subagents in parallel

#### Condition

Step 1 complete and at least one file path exists

#### Process

1. [subagent: parallel · await all] For each file path in the list, spawn one
   `utils:jp-mirror-translator` subagent. Pass the absolute file path as the prompt.
   (return: completion report string from each subagent)

→ Proceed to Step 3

#### Notes

- Issue **all Agent calls in a single response message** so they run concurrently
- Each subagent prompt contains only one absolute path (no conversation history needed)

---

### Step 3: Report results

#### Process

1. Collect all subagent completion reports and present them in a summary table:

| No | File | Action | Result |
|----|------|--------|--------|
| 1 | `foo.jp.md` | created / updated | `foo.md` |
