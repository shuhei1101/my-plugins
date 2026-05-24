---
name: pr-handoff
description: |
  Generate a handoff brief for the next session and output it inside the conversation.
  Trigger when the user says "引き継ぎ書を作って", "次のPRの指示書を作って", "ハンドオフして",
  "handoff して", "pr-handoff して", or calls `/work-kit:pr-handoff` explicitly.
---

# work-kit:pr-handoff — Generate Handoff Brief

Analyzes the current session's work and outputs a handoff brief as a code block
so the user can paste it into the next fresh-context session.

---

## Overview

After finishing a PR, any remaining work exists — but the next session's Claude
has zero context about what was done. This skill generates a brief that covers
"what happened" and "what to do next", output as a markdown code block
for easy copy-paste into the next session.

---

## Tasks

### Step 1: Confirm the target PR

#### Condition

- Always — run first

#### Process

1. If the user has already specified the next PR number and title, use those values
2. Otherwise:
   - Read `index.yaml` and list entries with `completed: false`
   - Ask the user: "Which PR should I hand off to?"

3. If a TODO.md exists for the target PR, read it to understand the work:
   ```
   .work/tasks/{task_folder}/PR{N}/TODO.md
   ```

→ Proceed to Step 2

#### Output

- Target PR number, title, and TODO content (if any) confirmed

---

### Step 2: Summarize current session work

#### Condition

- Step 1 complete

#### Process

1. Review the current conversation and summarize the main work done in this session:
   - PR number and title worked on
   - Key changes made (what changed and how)
   - Important design decisions or conclusions

2. If a TODO.md exists for the current PR, read it to check which rows are marked done:
   ```
   .work/tasks/{task_folder}/PR{N}/TODO.md
   ```

→ Proceed to Step 3

#### Output

- Summary of current session work is ready

---

### Step 3: Output handoff brief as a code block

#### Condition

- Step 2 complete

#### Process

1. Compose a markdown handoff brief using the structure below
2. Output it inside the conversation as a code block (` ```markdown `) — do not write to a file

**Handoff brief structure:**

```
# Handoff Brief — PR{N}: {Title}

## Background

In this session, the following work was done on {repository name}:

### Completed work
- {PR number}: {Title} — {Summary of main changes}

### Key decisions
- {Design decisions or context worth carrying forward, if any}

---

## What to do next

**PR{N}: {Title}**

### Request

{TODO.md task list or description of the work}

### Suggested steps

1. Run `/work-kit:work-start` to start work on PR{N}
2. {Specific implementation steps, if any}

### Reference files

- `.work/tasks/{task_folder}/PR{N}/TODO.md`: task checklist
- {Other relevant files}

---

## Notes

- {Any repo-specific constraints or rules worth flagging}
- Read `CLAUDE.md` first — it contains project-wide rules
```

→ Done

#### Output

- Handoff brief output as a code block in the conversation

#### Notes

##### Output format

- Do not write to a file — output inline in the conversation only
- Code block format lets the user copy it with Claude Code's copy command
- The user opens a new session and pastes the copied content as the first message

##### Output quality

- Make "what to do next" concrete and actionable
- Include the "why" (background context) to improve handoff quality
- Go beyond the TODO.md — include key constraints and context surfaced during this session
