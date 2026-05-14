---
name: claude-creator
description: |
  Create or overhaul a CLAUDE.md (and its CLAUDE.jp.md mirror) for a project or subfolder.
  Trigger when the user says "CLAUDE.md を作って", "CLAUDE.md を書いて", "create a CLAUDE.md",
  "クロードのガイドを作りたい", "このフォルダの CLAUDE.md を作って", or asks to set up
  Claude Code instructions for a project or specific folder.
---

# claude-creator — CLAUDE.md Authoring

Creates a CLAUDE.md and its paired CLAUDE.jp.md mirror for a project or subfolder.

---

## Overview

CLAUDE.md can be placed in two locations with different behaviors:

| Placement | When loaded |
|---|---|
| Project root | Loaded at every session start |
| Subfolder | Loaded lazily when Claude reads any file in that folder or its subfolders |

**Project root CLAUDE.md**: Defines the overall project workflow, commit rules, server management,
and the folder-scoped rule table.

**Subfolder CLAUDE.md**: Describes the folder's contents and conventions.
Useful for giving Claude context about what files in this folder do and how to work with them,
without loading that context at every session start.

---

## Tasks

### Step 0: Read background materials

#### Condition

- Always — before doing anything else

#### Process

1. Read the official Claude Code documentation on CLAUDE.md:
   **https://code.claude.com/docs/en/memory**

2. Read the file-type usage reference (`references/file-types.md` in this plugin).
   Key points:

   **CLAUDE.md vs Rules vs Skills:**
   - `CLAUDE.md` (root): loaded every session — project workflow, global conventions
   - `CLAUDE.md` (subfolder): loaded when Claude accesses that folder — folder description, local conventions
   - `.claude/rules/`: loaded when Claude reads a matching file — links to related files that must stay in sync
   - `.claude/skills/`: invoked on demand — multi-step workflows and procedures

   **What goes in CLAUDE.md (not rules):**
   - General descriptions of what files in a folder do
   - Conventions that apply whenever Claude works in this folder
   - Rules that should be visible regardless of which specific file is being edited

→ Proceed to Step 1

---

### Step 1: Gather creation details

#### Condition

- Step 0 complete

#### Input

- User's description of what they want to create

#### Process

1. Ask the user for:
   - **Location** — project root (`CLAUDE.md`) or a specific subfolder (e.g., `src/CLAUDE.md`)?
   - **For root**: overall workflow steps, prohibitions, folder-scoped rule table entries
   - **For subfolder**: what files are in this folder, what are their roles, any local conventions
   - **Content overview** — what instructions or descriptions should be included?

→ Proceed to Step 2

#### Output

- Location (root or subfolder path), content overview

---

### Step 2: Validate against file-type guide

#### Condition

- Step 1 complete

#### Input

- Location and content collected in Step 1
- File-type guide (`references/file-types.md` in this plugin)

#### Process

1. Check whether the content truly belongs in CLAUDE.md:

   | If the content is… | Suggest |
   |---|---|
   | Single-folder conventions or descriptions | ✅ CLAUDE.md (subfolder) — correct choice |
   | Project-wide workflow or global conventions | ✅ CLAUDE.md (root) — correct choice |
   | Cross-path file sync ("edit X → also update Y, Z in different folders") | ⚠️ `.claude/rules/` is more appropriate |
   | A multi-step workflow with user interaction | ⚠️ `.claude/skills/` is more appropriate |
   | Mix of the above | ⚠️ Consider splitting across file types |

2. If the content fits CLAUDE.md → confirm and proceed
3. If a different file type is more appropriate → explain why and offer to redirect to `rules-creator` or `skill-creator`

→ Proceed to Step 3 if CLAUDE.md is confirmed appropriate

#### Output

- Confirmed: the content fits CLAUDE.md

#### Notes

##### Branching

- Rules fit better → explain and offer to switch to `rules-creator`
- Skill fits better → explain and offer to switch to `skill-creator`
- Mixed → suggest splitting: CLAUDE.md for the folder description part, rules/skills for the rest

---

### Step 3: Write CLAUDE.jp.md first

#### Condition

- Step 1 complete

#### Input

- Placement and content outline from Step 1

#### Process

1. Write `CLAUDE.jp.md` (or `<subfolder>/CLAUDE.jp.md`) in Japanese using the step-based structure
   (see §References for structure template)
2. Put shared tables and cross-references in `## 参考資料` at the bottom
3. Keep the file under ~200 lines — move domain-specific content to `.claude/rules/` if needed

→ Proceed to Step 4

#### Output

- `CLAUDE.jp.md` written

#### Notes

##### Prohibitions

- Do not write the body in English — CLAUDE.jp.md is the Japanese human reference
- Do not exceed ~200 lines

---

### Step 4: Translate to CLAUDE.md (English)

#### Condition

- CLAUDE.jp.md written

#### Input

- CLAUDE.jp.md content

#### Process

1. Translate line-by-line to English
2. Write `CLAUDE.md` — the file Claude Code reads as directives
3. Keep heading structure identical to CLAUDE.jp.md

→ Proceed to Step 5

#### Output

- `CLAUDE.md` written

#### Notes

##### Prohibitions

- Do not write the body in Japanese
- Keep structure identical to CLAUDE.jp.md

---

### Step 5: Final verification

#### Condition

- Both files written

#### Process

1. Check that both files exist with matching structure
2. Confirm file is under ~200 lines
3. Present result to the user for review

#### Notes

##### Checklist

- [ ] `CLAUDE.md` — English, auto-loaded by Claude Code
- [ ] `CLAUDE.jp.md` — Japanese mirror, human reference only
- [ ] Matching heading structure
- [ ] Under ~200 lines

---

## References

### Step-based structure for CLAUDE.md

```markdown
## 概要
(What this folder/project does and how AI should work here — 1-3 sentences)

## 作業内容

### ステップN: (Action name)

#### 条件
(Preconditions to enter this step. If not met, stop or branch.)

#### 入力
(Data, files, or context this step uses)

#### 処理内容
(Numbered list of concrete actions. Include commands if applicable.)
1. Do X
2. Do Y
   ```bash
   command here
   ```
→ Proceed to Step N+1 (or → Step N if <condition>)

#### 出力
(What exists as a result of completing this step)

#### 補足

##### 禁止事項
(Things that must never be done in this step)

##### 条件分岐
("If X → go to Step N", "If Y → stop and ask the user")

##### 参照ドキュメント
(Files, URLs, or §References entries used in this step)

##### チェックリスト
(Items to verify before considering this step complete)

---

## 参考資料
(Shared tables, definitions, or reference material used across multiple steps)
```

### CLAUDE.md vs `.claude/rules/` placement

| Content | Where |
|---|---|
| Applies every session, any file | `CLAUDE.md` (root) |
| Folder-specific descriptions and conventions | `CLAUDE.md` (subfolder) |
| Applies only when reading/editing a specific file | `.claude/rules/<name>.md` with `paths:` |
| Multi-step workflow procedure | `.claude/skills/<name>/SKILL.md` |

### Official docs

- CLAUDE.md structure and placement: **https://code.claude.com/docs/en/memory**
