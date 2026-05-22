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

1. Review the **entire** session conversation and extract **every possible candidate** without omitting any.
   Cast a wide net — it is better to propose too many than to miss something valuable.

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

### Step 2: Propose artifact types

#### Condition

- Step 1 complete

#### Process

1. Based on the extracted candidates, propose **all identified artifacts** — list every candidate found, not just 2–3.
   Do not filter down. The user will decide what to keep.
   If a category yields multiple distinct candidates (e.g., two different rules), list each as a separate numbered proposal.

   ```
   今回の会話から以下のアーティファクトを作成できます:

   【案 A】スキル — {名前の候補}
   理由: {なぜスキルが適切か}
   生成物: .claude/skills/{name}/SKILL.md

   【案 B】ルール — {名前の候補}
   理由: {なぜルールが適切か}
   リンクするファイル: {編集時にセットで確認すべきファイル群}
   paths（読んだ時に発動）: {このルールを自動ロードしたいファイル/ディレクトリのパターン (例: src/**, *.ts, plugins/**)}
   生成物: .claude/rules/{name}.md

   【案 C】フック — {名前の候補}
   理由: {なぜフックが適切か}
   生成物: settings.json への hooks エントリ

   【再発防止】incidents に追記
   概要: {今回の教訓を1〜2行で}
   生成物: .claude/rules/incidents.md（インデックス）＋ .claude/references/incidents/{slug}.md（詳細）

   【用語集】glossary に以下の用語を追加してよいですか？
   - {term1}: {定義}
   - {term2}: {定義}
   生成物: .claude/rules/glossary.md

   どれを作成しますか？（複数選択可）
   ```

   > **Note**: E (incidents) is shown for insights that don't fit A–D.
   > F (glossary) is shown only when term candidates exist.

2. If nothing extractable is found:
   - Report "今回の会話から永続化できる知識・手順は見つかりませんでした" and stop.

→ After user selection, proceed to Step 3

#### Output

- Artifact type(s) selected by the user (one or more)

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
| glossary | (no creator skill) | Read `.claude/rules/glossary.md` (create if missing); append user-approved terms to the appropriate H2 category table |

If multiple types were selected, process them one at a time in the order the user listed.

→ After all selections are handled, proceed to Step 4

#### Notes

- Follow each creator skill's own steps
- After one creator skill completes, move to the next selected type
- glossary is always loaded as a rule — keep definitions to 1–2 sentences

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
| glossary | `.claude/rules/glossary.md` (always loaded) | Project-specific term definitions |

### Official docs

- Skills: **https://code.claude.com/docs/en/skills**
- Path-scoped rules: **https://code.claude.com/docs/en/memory**
- Hooks: **https://code.claude.com/docs/en/hooks**
