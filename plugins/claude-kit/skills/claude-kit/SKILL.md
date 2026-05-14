---
name: claude-kit
description: |
  Gateway for creating and editing Claude Code instruction files.
  Trigger when the user wants to: create or edit CLAUDE.md, create a new rule (.claude/rules/), create a new skill (.claude/skills/), ask about Claude Code authoring conventions, or set up Claude Code for a new project.
  Trigger phrases: "ルールを作る", "スキルを作る", "CLAUDE.md を作る", "create a rule", "create a skill", "new CLAUDE.md", "add a rule for", "how do I write a skill".
---

# claude-kit — Claude Code Instruction Authoring Toolkit

Gateway for creating and editing Claude Code instruction files.
Dispatches to `rules-creator` or `skill-creator` based on what the user needs.

---

## Overview

Three file types to know:

| File | Auto-loaded? | Scope |
|---|---|---|
| `CLAUDE.md` | Yes | Every session in this project |
| `.claude/rules/<name>.md` | Yes (path match or always) | Scoped to matching paths, or always-on if no `paths:` |
| `.claude/skills/<name>/SKILL.md` | Only when invoked | On-demand via `/skill-name` or auto-trigger from `description` |

---

## Tasks

### Step 1: Identify what the user needs

#### Condition

- `/claude-kit:claude-kit` was invoked or the user asked about creating a Claude Code file

#### Input

- User's request

#### Process

1. Identify which file type the user wants to create or edit:

   | User wants | Route to |
   |---|---|
   | Create a new rule for a domain or folder | `/claude-kit:rules-creator` |
   | Create a new skill | `/claude-kit:skill-creator` |
   | Create or edit `CLAUDE.md` | Apply conventions in this skill directly |
   | Edit an existing rule or skill | Apply conventions in this skill directly |
   | Ask how Claude Code works | Check official docs: **https://code.claude.com/docs/** |

2. If routing to a sub-skill, invoke it and hand off.
3. If editing directly, continue to Step 2.

#### Output

- Clear routing decision

---

### Step 2: Apply authoring conventions

#### Condition

- Editing CLAUDE.md, an existing rule, or an existing skill directly (not using a sub-skill)

#### Input

- Target file and requested changes

#### Process

1. Write or edit the English authoritative file
2. Write or edit the paired Japanese mirror
3. Commit both files together

#### Output

- English file and JP mirror both updated

#### Notes

##### Prohibitions

- Never write the body of CLAUDE.md / SKILL.md / `.claude/rules/*.md` in Japanese — Claude reads these directly as directives
- Never update one side (EN or JP) without updating the other
- Never place a `.jp.md` mirror inside `.claude/rules/` — use `.claude/rules-jp/` instead (the rules directory is scanned recursively; a JP file there would be auto-loaded)

##### References

Mirror placement:

| Auto-loaded (English) | Human mirror (Japanese) |
|---|---|
| `CLAUDE.md` | `CLAUDE.jp.md` (same directory) |
| `SKILL.md` | `SKILL.jp.md` (same directory) |
| `.claude/rules/<name>.md` | `.claude/rules-jp/<name>.md` (parallel directory) |

---

### Step 3: Verify and commit

#### Condition

- After creating or editing any instruction file

#### Process

1. Confirm EN file and JP mirror are both updated
2. Commit both in the same commit

#### Output

- Both files committed together

#### Notes

##### Checklist

- [ ] English authoritative file written / updated
- [ ] Japanese mirror written / updated to match
- [ ] Both committed in the same commit

---

## References

### CLAUDE.md vs `.claude/rules/` placement

| Instruction type | Where |
|---|---|
| Applies every session, regardless of which file is being edited | `CLAUDE.md` |
| Project meta-workflow (worktree, commit, server management) | `CLAUDE.md` |
| Applies only while editing a specific folder or file type | `.claude/rules/<name>.md` with `paths:` |
| "Which specs govern this folder" reference list | `.claude/rules/<name>.md` with `paths:` |

Keep `CLAUDE.md` under ~200 lines. Move domain-specific content to path-scoped rules.

### Official docs

| Topic | URL |
|---|---|
| Skills | https://code.claude.com/docs/en/skills |
| Path-scoped rules / memory | https://code.claude.com/docs/en/memory |
| Plugins | https://code.claude.com/docs/en/plugins |
| Hooks | https://code.claude.com/docs/en/hooks |
