---
name: conversation-to-claude
description: |
  Analyze the current session's conversation history and automatically create all
  appropriate artifacts (skill, rule, hook, CLAUDE.md, incidents, glossary) for
  persisting the knowledge or workflow discovered. No user confirmation required.
  Trigger when the user says "会話をキャプチャして", "今の作業を保存して", "この手順を残したい",
  "会話からスキル作って", "会話からルール作って",
  or invoked explicitly as `/claude-kit:conversation-to-claude`.
  Replaces the former `conversation-to-skill` and `conversation-to-rule` skills.
---

# conversation-to-claude — Generate Artifacts from Conversation History

Analyzes the session's conversation history, identifies all appropriate Claude Code
artifact types (skill / rule / hook / CLAUDE.md / incidents / glossary), and
implements them all automatically without asking for confirmation.

---

## Overview

After completing an implementation, investigation, or configuration task, you often want
to capture what was learned: a repeatable workflow, a file dependency, a hook trigger,
or a project convention. This skill figures out the best form for that knowledge and
generates all identified artifacts automatically.

---

## Tasks

### Step 1: Analyze the conversation history

#### Condition

- Always — run first

#### Process

1. Review the **entire** session conversation and extract **every possible candidate** without omitting any.
   Cast a wide net — it is better to create too many than to miss something valuable.

   **A. Repeatable workflow candidates** (→ skill)

   Use when: a multi-step workflow (3+ steps) involving user decisions, branching, or interaction. The value is reusability — someone would run this same procedure again.

   - 3+ step procedures involving user interaction or branching
   - Patterns worth reusing in other projects
   - Multi-step investigative or setup flows the user might repeat

   Not a skill: a single action, a one-time fix, or information that belongs in a rule or CLAUDE.md.

   ---

   **B. File dependency / path structure knowledge** (→ rule)

   Use when: you discovered that two or more files must stay in sync. A rule loads automatically when Claude *reads* a file matching `paths:`, surfacing the linked files every time.

   How `paths:` works:
   - Triggers when Claude **reads** a matching file — NOT on shell commands (mv, rm, cp)
   - Set `paths:` to files Claude will actually *open* when working in this domain
   - Example: `paths: ["src/models/**/*.py"]` loads when opening any model file

   What to put in a rule: links to related files, "when editing X also check Y". Keep it short — rules are injected on every matching read.
   What NOT to put: detailed docs, step-by-step workflows.

   - "Whenever I edit file X, I also need to edit file Y"
   - "Config lives here", "routing is here" — path role discoveries
   - Any "always check together" or "must stay in sync" pattern discovered during the session

   ---

   **C. Event-triggered automation** (→ hook)

   Use when: you want something to happen automatically at a specific event — no user prompt needed.

   Available events: `PreToolUse` (before tool call, can block) / `PostToolUse` / `Stop` (response done) / `SubagentStop` / `SessionStart` / `SessionEnd` / `UserPromptSubmit` / `PreCompact` / `Notification`

   Hook types: prompt injection (injects text into Claude's context) or shell command (runs a script).

   Not a hook: if the user should consciously trigger it — use a skill instead.

   - Actions to run automatically before/after specific tool use or at session start
   - "I want to check this every time before running that command"
   - Validations or notifications that should fire on every relevant event

   ---

   **D. Project-wide conventions and guidelines** (→ CLAUDE.md)

   Use when: conventions, prohibitions, or structural knowledge that every session should know — regardless of which files are open. CLAUDE.md loads always; rules load only on file read.

   Good CLAUDE.md content: prohibitions, naming conventions, folder/directory structure ("specs go in `.work/specs/`"), design principles, onboarding info.

   Not CLAUDE.md: file-specific sync rules (use rule), procedures (use skill), event automation (use hook).

   - Prohibitions, naming rules, design principles that apply to all files
   - Folder / directory structure discoveries: "specs live here", "generated files go there", "this folder is the canonical place for X"
   - Anything a new contributor would need to know to avoid mistakes or find the right place to put things

   ---

   **E. Lessons learned / recurrence prevention** (→ `incidents` rule)
   - Commands or operations that were tried and failed, where the cause and fix are now known
   - Wrong assumptions that turned out to be incorrect
   - "I don't want to make this mistake again"

   **F. Project-specific terminology** (→ `glossary` rule)
   - Project-specific nouns, abbreviations, or concepts the user mentioned in conversation
   - Terms not yet in `glossary.md`, or whose meaning was ambiguous
   - Words a reader would misunderstand without a definition

→ Proceed to Step 2

#### Output

- Exhaustive internal list of candidates per category — err on the side of including more

---

### Step 2: Check existing artifacts

#### Condition

- Step 1 complete

#### Process

1. For each candidate identified in Step 1, scan the project for existing artifacts that overlap or could absorb the new content:

   | Candidate type | Where to look |
   |---|---|
   | Skill | `.claude/skills/`, `plugins/*/skills/` — scan SKILL.md filenames and descriptions |
   | Rule | `.claude/rules/` — scan filenames and heading lines |
   | Hook | `~/.claude/settings.json`, `.claude/settings.json` — check existing hook entries |
   | CLAUDE.md content | `CLAUDE.md`, `plugins/*/CLAUDE.md` — check relevant sections |
   | incidents | `.claude/rules/incidents.md` — check for existing entries on the same topic |
   | glossary | `.claude/rules/glossary.md` — check for existing term entries |

2. For each candidate, decide:
   - **Merge into existing**: existing artifact covers the same domain → extend it
   - **Create new**: no closely related artifact exists

3. Record the decision (create new / edit existing at `{path}`) for use in Step 3.

→ Proceed to Step 3

#### Output

- For each candidate: decision (new / edit existing) and target path (if editing)

---

### Step 3: Implement all artifacts

#### Condition

- Step 2 complete

#### Process

1. If nothing extractable is found:
   - Report "今回の会話から永続化できる知識・手順は見つかりませんでした" and stop.

2. Otherwise, implement **all identified artifacts** automatically without asking for confirmation.
   If a category yields multiple distinct candidates (e.g., two different rules), implement each one.

   For each artifact type, delegate to the corresponding creator skill:

   | Type | Creator skill | Context to pass |
   |---|---|---|
   | Skill | `claude-kit:skill-creator` | Skill name candidate, trigger conditions, extracted workflow |
   | Rule | `claude-kit:rule-creator` | Domain name, file list, dependency description |
   | Hook | `claude-kit:hook-creator` | Hook name, target event, description of what to run |
   | CLAUDE.md | `claude-kit:claude-creator` | Guideline content to add or create |
   | incidents | (no creator skill) | Append a one-line summary to `.claude/rules/incidents.md` (index); write full details to `.claude/references/incidents/{slug}.md` (+ `.jp.md`) |
   | glossary | (no creator skill) | Read `.claude/rules/glossary.md` (create if missing); append terms to the appropriate H2 category table |

   Process multiple artifacts one at a time in order A → B → C → D → E → F.

→ Proceed to Step 4

#### Notes

- Follow each creator skill's own steps — but skip any confirmation prompts within them
- glossary is always loaded as a rule — keep definitions to 1–2 sentences

---

### Step 4: Commit and report

#### Condition

- Step 3 complete

#### Process

1. Commit all created and updated files with a descriptive message
2. List all created and updated files to the user

---

## References

### Artifact type summary

| Type | Output | Primary use case |
|---|---|---|
| Skill | `.claude/skills/<name>/SKILL.md` | Automating complex repeatable workflows |
| Rule | `.claude/rules/<name>.md` | Persisting file dependencies and path structure |
| Hook | `settings.json` hooks | Automatic pre/post-tool checks and notifications |
| CLAUDE.md | Append to `CLAUDE.md` | Documenting project conventions and guidelines |
| incidents | `.claude/rules/incidents.md` (index — always loaded)<br>`.claude/references/incidents/{slug}.md` (detail en)<br>`.claude/references/incidents/{slug}.jp.md` (detail jp) | Preventing recurrence of failures and wrong assumptions |
| glossary | `.claude/rules/glossary.md` (always loaded) | Project-specific term definitions |

### Official docs

- Skills: **https://code.claude.com/docs/en/skills**
- Path-scoped rules: **https://code.claude.com/docs/en/memory**
- Hooks: **https://code.claude.com/docs/en/hooks**
