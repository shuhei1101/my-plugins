---
name: conversation-capture
description: |
  Analyze the current session's conversation history and propose the best artifact type
  (skill, rule, hook, or CLAUDE.md) for persisting the knowledge or workflow discovered.
  Trigger when the user says "会話をキャプチャして", "今の作業を保存して", "この手順を残したい",
  "会話からスキル作って", "会話からルール作って",
  or invoked explicitly as `/claude-kit:conversation-capture`.
  Replaces the former `conversation-to-skill` and `conversation-to-rule` skills.
---

# conversation-capture — Generate Artifacts from Conversation History

Analyzes the session's conversation history, proposes the best Claude Code artifact type
(skill / rule / hook / CLAUDE.md), lets the user choose, and delegates to the
appropriate creator skill to implement it.

---

## Overview

After completing an implementation, investigation, or configuration task, you often want
to capture what was learned: a repeatable workflow, a file dependency, a hook trigger,
or a project convention. This skill figures out the best form for that knowledge and
generates it through the right creator skill.

---

## Tasks

### Step 1: Analyze the conversation history

#### Condition

- Always — run first

#### Process

1. Review the entire session conversation and extract:

   **A. Repeatable workflow candidates** (→ skill)
   - 3+ step procedures involving user interaction or branching
   - Patterns worth reusing in other projects

   **B. File dependency / path structure knowledge** (→ rule)
   - "Whenever I edit file X, I also need to edit file Y"
   - "Config lives here", "routing is here" — path role discoveries

   **C. Event-triggered automation** (→ hook)
   - Actions to run automatically before/after specific tool use or at session start
   - "I want to check this every time before running that command"

   **D. Project-wide conventions and guidelines** (→ CLAUDE.md)
   - Prohibitions, naming rules, design principles that apply to all files
   - "This belongs in CLAUDE.md"

→ Proceed to Step 2

#### Output

- Internal list of candidates per category

---

### Step 2: Propose artifact types

#### Condition

- Step 1 complete

#### Process

1. Based on the extracted candidates, propose **multiple artifact types (usually 2–3)**:

   ```
   From today's conversation, the following artifacts can be created:

   [Option A] Skill — {name candidate}
   Reason: {why a skill fits}
   Output: .claude/skills/{name}/SKILL.md

   [Option B] Rule — {name candidate}
   Reason: {why a rule fits}
   Output: .claude/rules/{name}.md

   [Option C] Hook — {name candidate}
   Reason: {why a hook fits}
   Output: hooks entry in settings.json

   Which would you like to create? (multiple selections allowed)
   ```

2. If nothing extractable is found:
   - Report "No reusable knowledge or workflows were found in this session" and stop.

→ After user selection, proceed to Step 3

#### Output

- Artifact type(s) selected by the user (one or more)

#### Reference: artifact selection criteria

| Type | Best fit |
|---|---|
| Skill | 3+ step repeatable workflow with user interaction or branching |
| Rule | File dependency discovery, path role knowledge |
| Hook | Automatic reaction to tool events (pre/post tool use, session start) |
| CLAUDE.md | Project-wide conventions, prohibitions, design principles |

---

### Step 3: Implement selected artifacts

#### Condition

- User selected artifact type(s) in Step 2

#### Process

For each selected type, launch the corresponding creator skill and delegate:

| Selected type | Creator skill | Context to pass |
|---|---|---|
| Skill | `claude-kit:skill-creator` | Skill name candidate, trigger conditions, extracted workflow |
| Rule | `claude-kit:rule-creator` | Domain name, file list, dependency description |
| Hook | `claude-kit:hook-creator` | Hook name, target event, description of what to run |
| CLAUDE.md | `claude-kit:claude-creator` | Guideline content to add or create |

If multiple types were selected, process them one at a time in the order the user listed.

→ After all selections are handled, proceed to Step 4

#### Notes

- Follow each creator skill's own steps
- After one creator skill completes, move to the next selected type

---

### Step 4: Report completion

#### Condition

- Step 3 complete

#### Process

1. List all created and updated files
2. Ask the user whether to commit
3. If the user agrees, commit the changes

---

## References

### Artifact type summary

| Type | Output | Primary use case |
|---|---|---|
| Skill | `.claude/skills/<name>/SKILL.md` | Automating complex repeatable workflows |
| Rule | `.claude/rules/<name>.md` | Persisting file dependencies and path structure |
| Hook | `settings.json` hooks | Automatic pre/post-tool checks and notifications |
| CLAUDE.md | Append to `CLAUDE.md` | Documenting project conventions and guidelines |

### Official docs

- Skills: **https://code.claude.com/docs/en/skills**
- Path-scoped rules: **https://code.claude.com/docs/en/memory**
- Hooks: **https://code.claude.com/docs/en/hooks**
