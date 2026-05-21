---
name: conversation-to-skill
description: |
  Analyze the current session's conversation history and generate a reusable skill
  from the work performed during the session.
  Trigger when the user says "会話からスキル作って", "今の作業をスキル化して",
  or invoked explicitly as `/claude-kit:conversation-to-skill`.
---

# conversation-to-skill — Generate a Skill from Conversation History

Reviews the current session's work, extracts repeatable workflow steps, and records
them as a skill under `.claude/skills/` using `skill-creator`.

---

## Overview

After completing a complex procedure, you often want to reuse it: "I'd like to do
the same thing in another project" or "automate this workflow."
This skill analyzes the conversation history, extracts the workflow steps, and
collaborates with the user to turn them into a reusable skill.

The process is conversational — the user confirms scope and naming before any files
are written, keeping the output accurate.

---

## Tasks

### Step 1: Analyze the conversation history

#### Condition

- Always — run first

#### Process

1. Review the entire conversation and extract:
   - The main work performed (what was done)
   - The step order (how it was done)
   - Tools, commands, and files referenced
   - Decision points and branching ("in this case did X, otherwise did Y")
   - Repeatable patterns worth capturing

2. Assess whether the workflow is a good fit for a skill:
   - 3+ steps with user interaction or branching → good fit for a skill
   - 1–2 simple operations → CLAUDE.md or `.claude/rules/` may be simpler

→ Proceed to Step 2

#### Output

- Summary of the extracted workflow

---

### Step 2: Confirm the scope with the user

#### Condition

- Step 1 complete

#### Process

Ask the user the following questions in order (conversational style):

**Question 1: Scope**
```
Which part of today's work do you want to turn into a skill?

Options:
A. {extracted work A} (e.g. DB schema change → migration → test update)
B. {extracted work B}
C. Wrap the entire conversation into one skill
```

**Question 2: Name and trigger**
```
What should the skill be named, and when should it auto-trigger?

Example:
- Name: db-migration
- Trigger: when the user says "DBを変えたい" or "マイグレーション作って"
```

**Question 3: Prerequisites**
```
Does this skill require anything to be in place before it runs?

Example: "docker must be running", "must be on a feature branch"
If none, just say "none".
```

Incorporate the user's answers to finalize the skill specification.

→ Proceed to Step 3

#### Output

- Skill name, trigger conditions, target workflow, prerequisites

---

### Step 3: Convert the workflow into a step structure

#### Condition

- Step 2 complete

#### Process

1. Convert the finalized workflow into the skill step structure:
   - Organize each action as "Condition → Process → Output"
   - Express decision points as "Branching" within the relevant step
   - Include specific commands and file paths where applicable

2. Present the structure to the user for approval:
   ```
   Here is the proposed skill structure. Reply "OK" to proceed, or point out any corrections.

   Skill name: {name}
   Trigger: {description}

   Step 1: {title}
     → {process summary}

   Step 2: {title}
     → {process summary}
   ...
   ```

→ Proceed to Step 4 after user approval

#### Output

- Approved skill step structure

---

### Step 4: Launch `skill-creator` to write the skill

#### Condition

- User approved the structure in Step 3

#### Process

1. Invoke the `claude-kit:skill-creator` skill
2. Pass the finalized skill specification:
   - Skill name
   - Trigger conditions (for the `description` frontmatter)
   - Step structure (condition / process / output for each step)
3. Follow skill-creator's steps to create:
   - `.claude/skills/<name>/SKILL.jp.md` (JP mirror — write first)
   - `.claude/skills/<name>/SKILL.md` (English — Claude reads this)

→ Proceed to Step 5

#### Notes

##### References

- Follow the `claude-kit:skill-creator` skill procedure

---

### Step 5: Report results and propose a commit

#### Condition

- Step 4 complete

#### Process

1. List all created files
2. Ask the user whether to commit
3. If the user agrees, commit the changes

#### Output

- List of created files
- Commit confirmation for the user

---

## References

### When to use a skill vs. other file types

| Content | Best location |
|---|---|
| 3+ step workflow with user interaction or branching | ✅ `.claude/skills/` |
| Repeatable routine that needs confirmation points | ✅ `.claude/skills/` |
| 1–2 simple rules or conventions | ⚠️ CLAUDE.md or `.claude/rules/` |
| File dependency relationships | ⚠️ `.claude/rules/` (use `conversation-to-rule`) |

### Official docs

- Skills: **https://code.claude.com/docs/en/skills**
