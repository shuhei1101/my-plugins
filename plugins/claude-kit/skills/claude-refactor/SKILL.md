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
folder restructuring, over-coupling / duplicate detection, file-type migration,
and JP/EN mirror integrity checks.

---

## Overview

Claude configuration tends to grow organically and become bloated.
This skill diagnoses the following and presents a reorganization plan:

1. **rules** — folder structure cleanup, consolidation/separation detection, file-type migration
2. **skills** — similar skill identification
3. **CLAUDE.md** — bloat detection and extraction to `.claude/references/`
4. **hooks** — identify content in rules/CLAUDE.md that should become hooks
5. **JP/EN mirrors** — detect missing mirror files across all scopes

Always targets all scopes.

---

## Tasks

### Step 1: Collect target files

#### Condition

- Always — run first

#### Process

1. Read all of the following reference files (this plugin's `references/`):
   - `common.md` — file type decision criteria and JP/EN mirror rules
   - `rules.md` — two rule types, use-case-oriented design, consolidation/separation, folder structure
   - `skills.md` — when to use skills, step structure
   - `hooks.md` — hook events, when to use hooks, loop prevention
   - `claude-md.md` — CLAUDE.md thinning principles, extraction destinations

2. Collect all of the following:

| Scope | Collection target |
|---|---|
| rules | Glob `.claude/rules/**/*.md`; read the first 30 lines (`paths:` and summary) of each |
| rules JP | Glob `.claude/rules-jp/**/*.md`; verify pairing with corresponding English rules |
| skills | Glob `.claude/skills/**/SKILL.md`; read `name` / `description` frontmatter and overview |
| skills JP | Check existence of `.claude/skills/**/SKILL.jp.md` |
| CLAUDE.md | List all `CLAUDE.md` files in project root and subfolders; check line counts |
| CLAUDE.md JP | Check existence of `CLAUDE.jp.md` alongside each `CLAUDE.md` |
| hooks | Read the hooks section of `.claude/settings.json` / `.claude/settings.local.json` / `hooks/hooks.json` |

→ Proceed to Step 2

#### Output

- List of collected files with summary

---

### Step 2: Analyze rules

#### Condition

- Step 1 complete

#### Process

Analyze each rule using the criteria from `references/common.md` (already read in Step 1):
rule types, use-case-oriented `paths:` design, consolidation/separation criteria, and file type appropriateness.

##### 2-A: Folder structure cleanup

1. If many flat `.md` files exist directly under `.claude/rules/`, propose organizing into subfolders
2. Determine folders using the following criteria:

   **Required folders**

   | Folder | Role | What goes here |
   |---|---|---|
   | `core/` | Project-wide foundational rules | Coding conventions, workflow, environment setup, general dev process |
   | `feature/` | Feature-specific domain knowledge | Rules per feature, specs, design decisions (1 feature = 1 file) |

   **Optional folders (codebase-dependent)**

   | Folder | When to add |
   |---|---|
   | `ui/` | Frontend exists: `components/`, `pages/`, `views/`, etc. |
   | `api/` | Many backend API rules / `routes/` or `handlers/` directories |
   | `infra/` | Many Docker / CI/CD / deployment rules |

3. Inform the user that `_overview.md` will be generated in each folder (template in Step 9)

##### 2-B: Consolidation and separation detection

Detect both over-consolidation (tight coupling) and insufficient consolidation (duplication):

**Consolidation candidates (duplicate detection)**:
- Identify rules sharing the same `paths:` pattern or same domain
- Mark rules with heavily overlapping content as "consolidation candidates"

**Separation candidates (tight coupling detection)**:
- Identify rules whose `paths:` covers multiple unrelated domains in a single file
  - Example: `src/models/` and `src/payments/` are in the same rule
  - Editing models would load the payments rule too, wasting context unnecessarily
- Mark as "separation candidates" and propose splitting by domain into separate files

**Decision criteria**:
- `paths:` patterns span unrelated directories → separate
- `paths:` patterns duplicate coverage of the same domain → consolidate

##### 2-C: File type appropriateness check

Check each rule against §References / File type decision criteria

→ Proceed to Step 3

#### Output

- Proposed folder structure
- Consolidation and separation candidates
- File type migration candidates

---

### Step 3: Analyze skills

#### Condition

- Step 2 complete

#### Process

##### 3-A: Similar skill identification

1. Identify pairs of skills whose `description` trigger conditions are similar
2. Do not prescribe consolidation — present as "similar skills exist" for the user to decide
3. Explain the degree of similarity and the differences (trigger conditions, step structure)

##### 3-B: File type appropriateness check

Check each skill against §References / File type decision criteria:

- **Should become a rule**: primarily a file sync link rather than a workflow
- **Should move to CLAUDE.md**: can be expressed in 1–2 simple lines
- **Appropriate as skill**: has multiple steps, user confirmation points, and branching

→ Proceed to Step 4

#### Output

- Similar skill pairs (with difference explanations)
- File type migration candidates

---

### Step 4: Analyze CLAUDE.md

#### Condition

- Step 3 complete

#### Process

CLAUDE.md is loaded on every session — keep it as thin as possible.

##### 4-A: Bloat detection

1. Mark CLAUDE.md files over 200 lines as "bloated"
2. Even below 200 lines, propose extraction if detailed explanations, workflows, or reference material are present

##### 4-B: Extraction destination proposals

For each section, propose the following extraction destinations in priority order:

| Content nature | Proposed destination |
|---|---|
| Cross-path link needed only when specific files are edited | `.claude/rules/` — path-matched, loads only when needed |
| Multi-step workflow or procedure | `.claude/skills/` — on-demand invocation |
| Content relevant only to a specific directory | `CLAUDE.md` in that subfolder |
| Reference material or detailed explanation needed only sometimes | `.claude/references/{topic}.md` — CLAUDE.md lists only the file path |
| Spec or doc already existing in the project | List only the file path in CLAUDE.md; do not duplicate content |

**About `.claude/references/`**:
A place for content that belongs in CLAUDE.md conceptually but does not need to be loaded every session
(detailed specs, supplementary explanations, reference material).
Write only the file path in CLAUDE.md — Claude reads the file when it actually needs it.

→ Proceed to Step 5

#### Output

- List of bloated CLAUDE.md files with line counts
- Per-section extraction proposals (with destination)

---

### Step 5: Analyze hooks

#### Condition

- Step 4 complete

#### Process

##### 5-A: Hook migration candidates

Scan rules / CLAUDE.md content and mark items with the following properties as "hook migration candidates":

| Property | Hook event candidate |
|---|---|
| "Check every time a prompt is submitted", "verify on every request" | `UserPromptSubmit` |
| "Do X every time Claude stops", "confirm after work is complete" | `Stop` |
| "Confirm before running a tool" | `PreToolUse` |
| "Notify after editing a file" | `PostToolUse` |

##### 5-B: Existing hooks redundancy check

1. If multiple hooks are registered for the same event, propose consolidation
2. If unused hook definitions exist, propose deletion

→ Proceed to Step 6

#### Output

- Hook migration candidates (current location → target hook event)
- Existing hooks redundancy report

---

### Step 6: Check JP/EN mirrors

#### Condition

- Step 5 complete

#### Process

Using the collection from Step 1, report missing mirror files:

| English file | Required JP mirror |
|---|---|
| `.claude/rules/{name}.md` | `.claude/rules-jp/{name}.md` |
| `.claude/skills/{name}/SKILL.md` | `.claude/skills/{name}/SKILL.jp.md` |
| `CLAUDE.md` (including subfolders) | `CLAUDE.jp.md` in the same folder |

List any missing JP mirrors as "needs creation".

→ Proceed to Step 7

#### Output

- List of files missing their JP mirror

---

### Step 7: Compile proposals and present to user

#### Condition

- Step 6 complete

#### Process

1. Organize proposals by category:

   **rules: Folder structure changes**
   | File (current) | Destination | Reason |
   |---|---|---|

   **rules: Consolidation candidates**
   | Target file | Merge into | Reason |
   |---|---|---|

   **rules: Separation candidates**
   | Target file | Split plan | Reason (context savings) |
   |---|---|---|

   **File type migration proposals**
   | Target (current) | Destination type | Reason |
   |---|---|---|

   **CLAUDE.md extraction proposals**
   | Target section | Destination | Reason |
   |---|---|---|

   **Hook migration candidates**
   | Target (current) | Hook event | Reason |
   |---|---|---|

   **Similar skills**
   | Skill A | Skill B | Similarities | Differences |
   |---|---|---|---|

   **Missing JP mirrors**
   | English file | JP mirror to create |
   |---|---|

2. Report "no issues found" for categories with zero proposals
3. Ask the user: "run all", "select individually", or "cancel"

→ Wait for user confirmation

---

### Step 8: Confirm user selection

#### Condition

- Step 7 proposals presented to user

#### Process

1. If user selects "run all": execute all proposals
2. If user selects individually: execute only selected proposals
3. Reflect any modifications the user makes to individual proposals

→ Proceed to Step 9

---

### Step 9: Execute

#### Condition

- User confirmation obtained in Step 8

#### Process

**Always invoke the corresponding creator skill for each category before doing any file work.**
Creator skills contain the creation criteria, templates, and mirror sync procedures — do not write files directly.

| Category | Invoke first | Then |
|---|---|---|
| rule creation / conversion / consolidation / separation | `/claude-kit:rule-creator` | Follow skill instructions to create, move, merge, or split |
| rule folder restructure | (no skill needed) | Move with `git mv`; generate `_overview.md` in each folder |
| skill creation / conversion | `/claude-kit:skill-creator` | Follow skill instructions to create or convert |
| CLAUDE.md creation / post-extraction update | `/claude-kit:claude-creator` | Follow skill instructions to create or update |
| hook creation | `/claude-kit:hook-creator` | Follow skill instructions to create hook; remove source content from rules/CLAUDE.md |
| JP mirror creation | Corresponding creator skill (above) | Each creator skill includes JP mirror creation steps |

**`_overview.md` template** (used when restructuring rules folders):

```markdown
# {folder-name} — {one-line category description}

## About this folder

{1–3 sentences on the policy for rules in this category}

## File list

| File | Content |
|---|---|
| `{file}.md` | {one-line description} |
```

→ Proceed to Step 10

#### Notes

##### Prohibitions

- Use `git mv` not `cp` (to preserve git history)
- Never write files directly without invoking the creator skill first
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

### Reference files

Use the files read in Step 1 as the criteria during analysis:

| File | Contents |
|---|---|
| `references/common.md` | File type decision criteria and JP/EN mirror rules |
| `references/rules.md` | Two rule types, use-case-oriented design, consolidation/separation, folder structure |
| `references/skills.md` | When to use skills, step structure |
| `references/hooks.md` | Hook events, when to use hooks, loop prevention |
| `references/claude-md.md` | CLAUDE.md thinning principles, extraction destinations |
