---
name: conversation-to-claude
description: |
  Analyze the current session's conversation history and propose the best artifact type
  (skill, rule, hook, or CLAUDE.md) for persisting the knowledge or workflow discovered.
  Trigger when the user says "会話をキャプチャして", "今の作業を保存して", "この手順を残したい",
  "会話からスキル作って", "会話からルール作って",
  or invoked explicitly as `/claude-kit:conversation-to-claude`.
  Replaces the former `conversation-to-skill` and `conversation-to-rule` skills.
---

# conversation-to-claude — Generate Artifacts from Conversation History

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

   **E. Lessons learned / recurrence prevention** (→ `incidents` rule)
   - Commands or operations that were tried and failed, where the cause and fix are now known
   - Wrong assumptions that turned out to be incorrect
   - "I don't want to make this mistake again"

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
   今回の会話から以下のアーティファクトを作成できます:

   【案 A】スキル — {名前の候補}
   理由: {なぜスキルが適切か}
   生成物: .claude/skills/{name}/SKILL.md

   【案 B】ルール — {名前の候補}
   理由: {なぜルールが適切か}
   適用パス: {このルールを適用するファイル/ディレクトリのパターン (例: src/**, *.ts, plugins/**)}
   生成物: .claude/rules/{name}.md

   【案 C】フック — {名前の候補}
   理由: {なぜフックが適切か}
   生成物: settings.json への hooks エントリ

   【再発防止】incidents に追記
   概要: {今回の教訓を1〜2行で}
   生成物: .claude/rules/incidents.md（インデックス）＋ .claude/references/incidents/{slug}.md（詳細）

   どれを作成しますか？（複数選択可）
   ```

   > **Note**: Proposals A–D take priority. E (incidents) is only for insights that don't fit A–D.

2. If nothing extractable is found:
   - Report "今回の会話から永続化できる知識・手順は見つかりませんでした" and stop.

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
| incidents | Failures, wrong assumptions, or misconceptions worth preventing from recurring |

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
| incidents | (no creator skill) | Append a one-line summary to `.claude/rules/incidents.md` (index); write full details to `.claude/references/incidents/{slug}.md` (+ `.jp.md`) |

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
| incidents | `.claude/rules/incidents.md` (index — always loaded)<br>`.claude/references/incidents/{slug}.md` (detail en)<br>`.claude/references/incidents/{slug}.jp.md` (detail jp) | Preventing recurrence of failures and wrong assumptions |

### Official docs

- Skills: **https://code.claude.com/docs/en/skills**
- Path-scoped rules: **https://code.claude.com/docs/en/memory**
- Hooks: **https://code.claude.com/docs/en/hooks**
