# Claude Code File Type Usage Guide

This document defines when to use `CLAUDE.md`, `.claude/rules/`, `.claude/skills/`, hooks, and references.
Shared reference for all creator skills and `claude-refactor`.
Japanese mirror: `references/file-types.jp.md`

---

## Summary: when to use what

| File type | When read | What to write |
|---|---|---|
| `CLAUDE.md` (root) | Every session start — always | Project-wide conventions and workflow. **Keep as thin as possible** |
| `CLAUDE.md` (subfolder) | When Claude accesses that folder | Folder description and local conventions (co-location preferred) |
| `.claude/rules/<name>.md` | When a file matching `paths:` is read | Cross-path links and missed-update prevention. Single-folder also fine (auditability preferred) |
| `.claude/skills/<name>/SKILL.md` | When invoked | Multi-step workflows and procedures |
| `.claude/hooks/` + `settings.json` | On specific event (automatic) | Auto-checks, notifications, prompt injection |
| `.claude/references/<name>.md` | On-demand, when Claude needs it | Detailed explanations and reference material not needed every session |

---

## CLAUDE.md

### When it loads

| Placement | When loaded |
|---|---|
| Project root | At every session start — always loaded |
| Subfolder | Lazily, when Claude reads any file in that folder or its subfolders |

A subfolder CLAUDE.md is not loaded at session start.
It loads the moment Claude accesses a file in that directory.

### Purpose

- Describing the contents and conventions of a folder
- General rules that apply whenever Claude works in this folder

### Important: keep it thin

The root CLAUDE.md is **loaded on every session** — the more content it has, the more context it consumes.
Keep it thin using these principles:

| Content nature | Action |
|---|---|
| Needed only when specific files are edited | Move to `.claude/rules/` |
| Multi-step workflow or procedure | Move to `.claude/skills/` |
| Relevant only to a specific folder | Move to that subfolder's `CLAUDE.md` |
| Detailed explanation or reference (read occasionally) | Move to `.claude/references/`; write only the path in CLAUDE.md |
| Spec or doc already in the project | Write only the path; do not duplicate content |

### Not a good fit

- Multi-step workflows or procedures → `.claude/skills/` is more appropriate
- Detailed explanations not needed every session → extract to `.claude/references/`

---

## `.claude/rules/` (Path-scoped rules)

### When it loads

Loads when Claude **reads** a file matching the `paths:` pattern.

- ✅ Reading a file → loads
- ✅ Editing a file (Claude reads before editing) → loads
- ❌ Shell-only commands (`mv`, `rm`, etc.) without reading → does not load
- ❌ Working without accessing a matching file → does not load

### Two types of rules

Rules serve two distinct purposes:

#### ① Link rule (file-coupling type)

Bundles related files so that editing one forces the author to check the others.

- List all related files in `paths:`
- Example: abstract class + interface + child class + parent class in one rule
- Example: config file + spec doc + test cases + implementation code bundled together
- **Effect**: When any one file is edited, Claude has full context of the entire relationship

#### ② Context rule (trigger-load type)

Automatically loads relevant knowledge, specs, or guidelines when working in a specific area.

- Set `paths:` to the files that, when touched, should trigger loading this rule
- Example: touching `config/` → config spec rule is loaded
- Example: touching `src/` → coding convention rule is loaded

### Use-case-driven `paths:` design

**Start from "when should this be read?"**

1. **Identify the use case** — in what kind of work is this rule useful?
2. **Identify the trigger file/folder** — what file is always touched during that work?
3. **Set that file in `paths:`** — the rule loads every time it is touched

**Example — context rule for a config spec**:
- Use case: when editing a config file, load the corresponding spec
- Trigger: editing something in `config/`
- Set `config/**` in `paths:` → spec rule loads every time a config file is touched

**Example — always-on rule**:
- Use case: a rule that must be followed during any work (e.g. coding conventions)
- Trigger: touching any source code
- Set a broad pattern like `src/**` or `**/*.ts` in `paths:`

### Consolidation and separation

- **Consolidate**: rules covering the same domain with duplicated content → merge into one
- **Separate**: one rule covering unrelated domains → split by domain
  - A `paths:` spanning unrelated directories causes unnecessary context load on every touch
  - Principle: 1 domain = 1 rule file

### Single-folder content: `.claude/rules/` vs subfolder `CLAUDE.md`

| Priority | Choice |
|---|---|
| **See all active rules in one place** (auditability) | `.claude/rules/<name>.md` |
| **Keep rules co-located with the code** (proximity) | Subfolder `CLAUDE.md` |

Cross-path linking ("if X changes, also update Y in a different folder") always belongs in `.claude/rules/`.

---

## `.claude/skills/`

### When it loads

- When explicitly invoked as `/skill-name`
- When the `description` frontmatter condition is matched (auto-trigger)

Do not use `disable-model-invocation: true` by default.
**Exception**: use it for skills that must only be run by a human (merge, deploy, destructive operations).

### Purpose

Define multi-step workflows and procedures.

### When to use

- 3 or more steps, user confirmation points, branching → skill
- PR creation flow, documentation authoring, information gathering routines

### Not a good fit

- Simple rules that fit in 1–2 lines → `CLAUDE.md` or `.claude/rules/`
- File sync reminders → `.claude/rules/`

---

## `.claude/hooks/` (Prompt-injection hooks)

### When it fires

Automatically injects a prompt into Claude's context when a registered event fires in `settings.json`.

### Hook events and purposes

| Event | When it fires | Purpose |
|---|---|---|
| `UserPromptSubmit` | Every time the user submits a prompt | Rules or checklists to verify on every request |
| `Stop` | Every time Claude stops responding | Post-work checks, forced follow-up |
| `PreToolUse` | Before a tool is executed | Block or confirm dangerous operations |
| `PostToolUse` | After a tool is executed | Post-edit notifications or validation |
| `SessionStart` | At session start | Initial context injection |

### When to migrate rules/CLAUDE.md content to hooks

If content in rules / CLAUDE.md has any of these properties, a hook may be more effective:

- "Check every time a prompt is submitted", "verify on every request" → `UserPromptSubmit`
- "Do X every time Claude stops", "confirm after work is complete" → `Stop`
- "Confirm before running a tool" → `PreToolUse`
- "Notify after editing a file" → `PostToolUse`

### Not a good fit

- Content that only needs to be confirmed once — hooks fire every time
- Long-form prompts — the `Stop` hook's `reason` is shown directly to the user; keep it brief

---

## `.claude/references/`

### When it loads

No auto-load. Claude reads it on-demand when needed.

### Purpose

A place for content that belongs in CLAUDE.md conceptually but does not need to be loaded every session
(detailed specs, supplementary explanations, reference material).
Write only the file path in CLAUDE.md — Claude reads the file when it actually needs it.

### When to use

- Detailed specs and design documents
- Usage guides and tutorials
- Shared reference knowledge for creator skills (this file itself is an example)

---

## JP/EN mirror rules

Every file requires a corresponding JP mirror:

| English file (read by Claude) | JP mirror (human reference only) |
|---|---|
| `.claude/rules/<name>.md` | `.claude/rules-jp/<name>.md` |
| `.claude/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.jp.md` |
| `CLAUDE.md` (any folder) | `CLAUDE.jp.md` in the same folder |
| `.claude/references/<name>.md` | `.claude/references/<name>.jp.md` |

**Update procedure**: update the JP mirror first, then apply the same change to the English version.
