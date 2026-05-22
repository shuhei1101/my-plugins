---
name: claude-refactor
description: |
  Audit and organize Claude configuration (rules / skills / CLAUDE.md / hooks).
  Trigger when the user says "ルールを整理して", "設定が肥大化してきた",
  "スキルに重複がある気がする", "CLAUDE.md が長くなってきた",
  ".claude/ をきれいにしたい", or calls `/claude-kit:claude-refactor` explicitly.
---

# claude-refactor — Audit and Reorganize Claude Configuration

Audits rules / skills / CLAUDE.md / hooks under `.claude/` and proposes
folder restructuring, deduplication, consolidation, and file-type migration.

---

## Overview

Claude configuration tends to grow organically and become bloated.
This skill diagnoses the following and presents a reorganization plan to the user:

1. **rules** — folder structure cleanup, duplicate/consolidation detection, migration to CLAUDE.md or hooks
2. **skills** — duplicate/consolidation/split detection
3. **CLAUDE.md** — bloat detection and extraction to rules/skills
4. **hooks** — identify content in rules/CLAUDE.md that should become hooks

The user selects which scopes to process.
All scopes can be run at once, or individual scopes can be targeted.

---

## Tasks

### Step 1: Confirm the scope

#### Condition

- Always — run first

#### Process

1. Ask the user which scopes to organize:
   - All scopes (rules + skills + CLAUDE.md + hooks)
   - rules only
   - skills only
   - CLAUDE.md only
   - Any combination

2. If the user does not specify, propose "all scopes"

→ Proceed to Step 2

#### Output

- List of scopes to reorganize

---

### Step 2: Collect target files

#### Condition

- Step 1 complete

#### Process

Collect files for each selected scope:

| Scope | Collection target |
|---|---|
| rules | Glob `.claude/rules/**/*.md` and read the first 30 lines of each file |
| skills | Glob `.claude/skills/**/SKILL.md` and read `name` / `description` frontmatter and overview |
| CLAUDE.md | List all `CLAUDE.md` files in project root and subfolders; check line counts |
| hooks | Read the hooks section of `.claude/settings.json` / `.claude/settings.local.json` / `hooks/hooks.json` |

→ Proceed to Step 3

#### Output

- List of collected files with summary

---

### Step 3: Analyze rules (when rules scope is selected)

#### Condition

- Step 2 complete and rules scope is selected

#### Process

Analyze each rule from the following perspectives:

##### 3-A: Folder structure cleanup

1. If many flat `.md` files exist directly under `.claude/rules/`, propose organizing into subfolders
2. Determine folder candidates using §References / Folder structure criteria

##### 3-B: Duplicate and consolidation detection

1. Identify rules that share the same `paths:` pattern or same domain
2. Mark rules with heavily overlapping content as "consolidation candidates"
3. Mark rules covering the same domain with different content as "merge consideration"

##### 3-C: File type appropriateness check

Check each rule against §References / File type decision criteria:

- **Should move to CLAUDE.md**: 1–2 line instruction needed on every session
- **Should become a hook**: "run automatically when X happens", "check every time Claude stops"
- **Should become a skill**: contains a multi-step workflow
- **Appropriate as rule**: cross-path file sync link spanning multiple different folders

→ Proceed to Step 4 (or next scope)

#### Output

- Proposed folder structure
- Consolidation candidates
- File type migration candidates

---

### Step 4: Analyze skills (when skills scope is selected)

#### Condition

- Step 2 complete and skills scope is selected

#### Process

Analyze each skill from the following perspectives:

##### 4-A: Duplicate and consolidation detection

1. Identify skills whose `description` trigger conditions are similar
2. Mark skills with similar step structures as "consolidation candidates"
3. When proposing consolidation, also suggest which skill to use as the base

##### 4-B: Split consideration

1. Mark skills over 200 lines as "split consideration"
2. Propose splitting when a single skill covers multiple unrelated use cases

##### 4-C: File type appropriateness check

Check each skill against §References / File type decision criteria:

- **Should become a rule**: primarily a file sync link rather than a workflow
- **Should move to CLAUDE.md**: can be expressed in 1–2 simple lines
- **Appropriate as skill**: has multiple steps, user confirmation points, and branching

→ Proceed to Step 5 (or next scope)

#### Output

- Consolidation candidates (including which skill to use as base)
- Split candidates
- File type migration candidates

---

### Step 5: Analyze CLAUDE.md (when CLAUDE.md scope is selected)

#### Condition

- Step 2 complete and CLAUDE.md scope is selected

#### Process

Analyze each CLAUDE.md from the following perspectives:

##### 5-A: Bloat detection

1. Mark CLAUDE.md files over 200 lines as "bloated"
2. For bloated files, propose where to extract content (rules / skills / subfolder CLAUDE.md)

##### 5-B: Content appropriateness check

Check each section against §References / File type decision criteria:

- **Should move to rules**: cross-path link that only needs to load when specific files are edited
- **Should become a skill**: multi-step workflow or procedure
- **Should move to subfolder CLAUDE.md**: content relevant only to a specific directory
- **Should remain in root CLAUDE.md**: workflow or constraints needed project-wide at all times

→ Proceed to Step 6 (or next scope)

#### Output

- List of bloated CLAUDE.md files with line counts
- Per-section migration proposals

---

### Step 6: Analyze hooks (when hooks scope is selected)

#### Condition

- Step 2 complete and hooks scope is selected

#### Process

##### 6-A: Discover hook migration candidates

Scan rules / CLAUDE.md content and mark items with the following properties as "hook migration candidates":

| Property | Hook event candidate |
|---|---|
| "Check every time a prompt is submitted", "verify on every request" | `UserPromptSubmit` |
| "Do X every time Claude stops", "confirm after work is complete" | `Stop` |
| "Confirm before running a tool" | `PreToolUse` |
| "Notify after editing a file" | `PostToolUse` |

##### 6-B: Redundancy check for existing hooks

1. If multiple hooks are registered for the same event, propose consolidation
2. If unused hook definitions exist, propose deletion

→ Proceed to Step 7

#### Output

- Hook migration candidates (current location → target hook event)
- Existing hooks redundancy report

---

### Step 7: Compile proposals and present to user

#### Condition

- All selected scopes have been analyzed

#### Process

1. Organize proposals by category:

   **Folder structure changes** (rules only)
   | File (current) | Destination | Reason |
   |---|---|---|
   | ... | ... | ... |

   **Consolidation / deprecation proposals**
   | Target | Type | Proposal | Reason |
   |---|---|---|---|
   | ... | rule/skill | Merge into: `{name}` | ... |

   **File type migration proposals**
   | Target (current) | Destination type | Reason |
   |---|---|---|
   | ... | rule/skill/CLAUDE.md/hook | ... |

   **Split proposals** (skills only)
   | Target skill | Split plan | Reason |
   |---|---|---|
   | ... | `{name-a}` + `{name-b}` | ... |

2. Report "no issues found" for scopes with zero proposals
3. Ask the user: "run all", "select individually", or "cancel"

→ Wait for user confirmation

#### Output

- Full proposal list
- User's execution instructions

---

### Step 8: Confirm user selection

#### Condition

- Step 7 proposals presented to user

#### Process

1. If user selects "run all": execute all proposals
2. If user selects individually: execute only selected proposals
3. If user modifies any proposal: reflect the modifications

→ Proceed to Step 9

---

### Step 9: Execute

#### Condition

- User confirmation obtained in Step 8

#### Process

Execute confirmed work:

| Work type | How to execute |
|---|---|
| rules folder restructure | Move files with `git mv`; generate `_overview.md` in each folder |
| rules consolidation | Merge content into base file; `git rm` the old file |
| skills consolidation | Merge content into base skill; `git rm` the old folder |
| skills split | Create new skill folders; split content accordingly |
| CLAUDE.md extraction | Move sections to new rules/skill file; remove from CLAUDE.md |
| hooks migration | Call `hook-creator` to create the hook; remove content from source rules/CLAUDE.md |
| File type conversion | Call the appropriate creator skill to create the new artifact |

→ Proceed to Step 10

#### Notes

##### Prohibitions

- Use `git mv` not `cp` (to preserve git history)
- Always update references in other skills/rules that mention renamed/moved files

---

### Step 10: Report results

#### Condition

- Step 9 complete

#### Process

1. Report the list of changed files
2. Report generated and deleted files
3. Prompt the user to confirm and commit

---

## References

### Folder structure criteria

#### Required folders

| Folder | Role | What goes here |
|---|---|---|
| `core/` | Project-wide foundational rules | Coding conventions, workflow, environment setup, general dev process |
| `feature/` | Feature-specific domain knowledge | Implementation rules per feature, specs, design decisions (1 feature = 1 file) |

#### Optional folder criteria

| Folder | When to add |
|---|---|
| `ui/` | Frontend exists: `components/`, `pages/`, `views/`, etc. |
| `api/` | Many backend API rules / `routes/` or `handlers/` directories exist |
| `infra/` | Many Docker / CI/CD / deployment rules |

---

### File type decision criteria

| Content nature | Best file type | Reason |
|---|---|---|
| Cross-path file sync link spanning multiple different folders | **rule** | Path-matched auto-load only when target files are edited |
| Single-folder file listing or local conventions | rule or subfolder CLAUDE.md | rule for visibility, CLAUDE.md for co-location |
| Short workflow or constraints needed project-wide at all times | **CLAUDE.md (root)** | Always loaded at session start |
| Multi-step workflow with user confirmation and branching | **skill** | On-demand invocation; does not pollute context |
| Repeated auto-check or notification triggered by events | **hook** | Auto-fires on event; injects into Claude's context |
| 1–2 line simple instruction or caution | CLAUDE.md or rule | Not complex enough to warrant a skill |

---

### Skills analysis criteria

| Condition | Proposal |
|---|---|
| `description` trigger heavily overlaps with another skill | Consolidation candidate — confirm which skill encompasses the other |
| 2 or fewer steps with no branching | Migration candidate to rule or CLAUDE.md |
| Over 200 lines and covers multiple unrelated use cases | Split candidate — one skill per use case |
| Already called as Step N of another skill | Clarify delegate relationship; remove or restrict standalone `description` |

---

### `_overview.md` template (for rules folders)

```markdown
# {folder-name} — {one-line category description}

## About this folder

{1–3 sentences on the policy for rules in this category}

## File list

| File | Content |
|---|---|
| `{file}.md` | {one-line description} |
```
