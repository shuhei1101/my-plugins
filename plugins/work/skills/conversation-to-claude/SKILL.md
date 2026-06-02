---
name: work:conversation-to-claude
description: |
  Analyze the current session's conversation history and automatically create all
  appropriate artifacts (skill, rule, hook, CLAUDE.md, incidents, glossary) for
  persisting the knowledge or workflow discovered. No user confirmation required.
  Trigger when the user says "会話をキャプチャして", "今の作業を保存して", "この手順を残したい",
  "会話からスキル作って", "会話からルール作って",
  or invoked explicitly as `/work:conversation-to-claude`.
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

**Quality over quantity.** The value of this skill is in capturing knowledge that is
**not already discoverable** — not in producing a large pile of entries. Every glossary
term and incident must survive the deduplication check in Step 2 (it must add information
that CLAUDE.md, the rules, the folder structure, and existing entries do not already
provide). When in doubt, do **not** register it.

---

## Tasks

### Step 1: Analyze the conversation history

#### Condition

- Always — run first

#### Process

1. Review the **entire** session conversation and extract candidates per category below.
   Cast a wide net for skill / rule / hook / CLAUDE.md candidates (better too many than to
   miss something reusable). For **incidents** and **glossary**, apply the stricter inclusion
   bars defined in E and F — these two are quality-gated, not quantity-driven.

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

   What to put in a rule: links to related files, "when editing X also check Y". Keep it short.
   What NOT to put: detailed docs, step-by-step workflows.

   - "Whenever I edit file X, I also need to edit file Y"
   - "Config lives here", "routing is here" — path role discoveries
   - Any "always check together" or "must stay in sync" pattern discovered during the session

   ---

   **C. Event-triggered automation** (→ hook)

   Use when: you want something to happen automatically at a specific event — no user prompt needed.

   Available events: `PreToolUse` / `PostToolUse` / `Stop` / `SubagentStop` / `SessionStart` / `SessionEnd` / `UserPromptSubmit` / `PreCompact` / `Notification`

   Not a hook: if the user should consciously trigger it — use a skill instead.

   - Actions to run automatically before/after specific tool use or at session start
   - Validations or notifications that should fire on every relevant event

   ---

   **D. Project-wide conventions and guidelines** (→ CLAUDE.md)

   Use when: conventions, prohibitions, or structural knowledge that every session should know — regardless of which files are open. CLAUDE.md loads always; rules load only on file read.

   Good CLAUDE.md content: prohibitions, naming conventions, folder/directory structure, design principles, onboarding info.

   Not CLAUDE.md: file-specific sync rules (use rule), procedures (use skill), event automation (use hook).

   ---

   **E. Lessons learned / recurrence prevention** (→ `incidents`)

   An incident captures a **concrete process mistake that actually happened this session** (an error
   of operation or judgment — NOT a code defect/bug) so it does not recur. Record an entry **only if
   ALL of these hold**:

   - A real failure occurred this session: a command/operation failed and the correct approach
     is now known; a file was accidentally deleted or overwritten; a task planned in the original
     TODO was silently dropped by AI and the user had to re-request it; AI acted on a wrong
     assumption and the user corrected it.
   - The lesson is **generalizable** to future sessions (not specific to this one branch's code).
   - The prevention is **not already captured** elsewhere (see the dedup check in Step 2).

   Do **NOT** record (these are the failure modes the old version suffered from):
   - **The code bug itself / its fix** — the single most common mis-registration. A bug a bug-fix
     branch resolved is done once fixed; it is a code defect, not a session process mistake, and
     logging these explodes the entry count. "Which bug, fixed how" belongs in the task document /
     commit message.
   - **"That's already a rule / CLAUDE.md convention."** If the correct behavior is (or should be)
     enforced by an existing rule, CLAUDE.md, or hook, it is not an incident. If a rule *should*
     exist, create the rule (category B/D) instead of logging an incident.
   - The PR/branch work content itself (what feature was implemented, what code was changed).
   - Tasks the user newly added as scope expansion.
   - General best-practices already documented anywhere in the project or in well-known tooling docs.
   - A one-off slip with no generalizable prevention.

   ---

   **F. Project-specific terminology** (→ `glossary`)

   A glossary term defines a project-specific noun/abbreviation/concept a reader would otherwise
   misunderstand. Because the glossary is **always loaded**, every entry costs context on every
   session — so the bar is high. Register a term **only if ALL of these hold**:

   - It is **project-specific**: a coined term, an internal abbreviation, or a word used with a
     non-obvious project-specific meaning.
   - Its meaning is **not obvious from its own name**, and a reader would genuinely misunderstand
     or fail to understand it without the definition.
   - It **recurs** — it is (or will be) referenced repeatedly, not mentioned once in passing.
   - The meaning is **not already discoverable** (see the dedup check in Step 2).

   Do **NOT** register (these are the failure modes the old version suffered from):
   - **"That's already in CLAUDE.md / a rule / a skill description."** Those files are the source
     of truth; duplicating them in the glossary is pure bloat. Point to / rely on the source instead.
   - **"You can tell that just from the folder/file structure."** If opening the repo or reading a
     file name makes the meaning self-evident (e.g. "the `skills/` folder holds skills"), skip it.
   - General or industry-standard terms that are not project-specific (git, PR, commit, hook, lint).
   - One-off mentions with no reuse value.
   - A restatement of something already obvious from reading the relevant file.

→ Proceed to Step 2

#### Output

- A list of candidates per category. Skill/rule/hook/CLAUDE.md: inclusive. incidents/glossary:
  only entries that pass the E/F bars above.

---

### Step 2: Deduplicate against existing artifacts (source-of-truth check)

#### Condition

- Step 1 complete

#### Process

This step is the **proliferation guard**. Its purpose is to prevent the low-value entries the
old version produced. Run it for **every** candidate, and especially aggressively for incidents
and glossary.

1. For each candidate, scan the project for existing artifacts that already cover it:

   | Candidate type | Where to look (search by term / topic) |
   |---|---|
   | Skill | `.claude/skills/`, `plugins/*/skills/` — SKILL.md filenames and descriptions |
   | Rule | `.claude/rules/` — filenames and heading lines |
   | Hook | `~/.claude/settings.json`, `.claude/settings.json`, `plugins/*/hooks/` |
   | CLAUDE.md content | `CLAUDE.md`, `plugins/*/CLAUDE.md` — relevant sections |
   | incidents | `.claude/rules/incidents.md` + `.claude/references/incidents/` — same topic? |
   | glossary | `.claude/rules/glossary.md` — same or adjacent term? |

2. **Mandatory dedup check for every incident and glossary candidate.** Before keeping it,
   actively search:
   - **glossary** → grep `CLAUDE.md`, every `plugins/*/CLAUDE.md`, `.claude/rules/`, and skill
     descriptions for the term and its concept. If the meaning is already stated there, or is
     self-evident from the folder/file structure → **discard**.
   - **incidents** → check whether an existing rule, CLAUDE.md convention, hook, or incident
     already enforces or records the lesson. If so → **discard** (or, if a rule *should* exist
     but doesn't, convert it to a rule candidate instead).

3. Apply the decision per candidate:
   - **Merge into existing**: an existing artifact covers the same domain → extend it, do NOT create a new file.
   - **Discard**: one-time, temporary, already covered, or self-evident → skip it.
   - **Create new**: no existing artifact covers it AND it clears the category's inclusion bar.

4. Record the decision (create new / merge into `{path}` / discard) for Step 3.

→ Proceed to Step 3

#### Output

- For each surviving candidate: decision (new / merge) and target path. Discarded candidates dropped.

---

### Step 3: Implement all artifacts

#### Condition

- Step 2 complete

#### Process

1. If nothing survived Step 2:
   - Report "今回の会話から永続化すべき知識・手順は見つかりませんでした" and stop.

2. **incidents / glossary** — handle directly (no creator-skill delegation):
   - **incidents**: Append a one-line summary to `.claude/rules/incidents.md` (index); write full
     details to `.claude/references/incidents/{slug}.md` (+ `.jp.md` mirror).
   - **glossary**: Read `.claude/rules/glossary.md` (create if missing); append terms to the
     appropriate H2 category table. Keep each definition to 1–2 sentences.

3. **Skill / Rule / Hook / CLAUDE.md** — spawn one subagent per category that has surviving
   candidates. Launch all applicable subagents **in a single message** (parallel) using the
   Agent tool with `isolation: "worktree"`. Wait for all to complete before Step 4.

   Each subagent delegates to the matching **claude-kit creator skill** (invoked by its slash
   command so it resolves regardless of install location):

   | Category | Creator skill (invoke) | What to implement |
   |---|---|---|
   | Skill | `/claude-kit:skill-creator` | All skill candidates |
   | Rule | `/claude-kit:rule-creator` | All rule candidates |
   | Hook | `/claude-kit:hook-creator` | All hook candidates |
   | CLAUDE.md | `/claude-kit:claude-creator` | All CLAUDE.md additions |

   **Subagent prompt template** (fill in `{…}` per category before sending):

   ```
   You are a subagent responsible for creating [{Category}] artifacts.

   ## Steps
   1. Invoke the creator skill: {creator skill slash command}
   2. Follow its steps to implement all targets below.
      Skip any confirmation prompts — implement automatically.

   ## Targets
   {For each candidate in this category:}
   ### {artifact name or description}
   - Trigger / Domain / Event: {extracted trigger, domain, or event}
   - Context: {workflow steps / file list / hook behavior / guideline text}
   - Step 2 decision: {new | merge into {path}}

   ## Notes
   - If multiple targets exist, implement them one at a time in listed order
   - Follow the Step 2 decision (new / merge) for each target
   ```

   > If claude-kit is not installed in this project, the subagent cannot invoke the creator skill.
   > In that case the subagent creates the artifact directly following the project's existing
   > conventions (the claude-kit ref-inject hook, if present, auto-injects the authoring guide on
   > Write/Edit of the target file).

→ Proceed to Step 4

#### Notes

- Skip any confirmation prompts inside creator skills
- glossary is always loaded — keep definitions to 1–2 sentences

---

### Step 4: Verify output

#### Condition

- Step 3 complete

#### Process

1. For each artifact, verify:
   - The expected files were created or updated at the correct paths
   - Contents match the intended artifact (spot-check headings and key fields)
   - No unintended files were created outside the expected directories
   - **Re-check incidents/glossary against the Step 2 dedup bar** — delete any entry that, on
     review, merely duplicates CLAUDE.md / a rule / the folder structure.
2. If any issue is found, fix it directly (do not re-spawn the subagent).

→ Proceed to Step 5

---

### Step 5: Commit and report

#### Condition

- Step 4 complete

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

### Inclusion bar quick reference

- **glossary**: project-specific + meaning non-obvious + recurring + not already in CLAUDE.md / rules / skill descriptions / folder structure.
- **incidents**: a real mistake happened this session + lesson is generalizable + not already enforced by a rule / CLAUDE.md / hook / existing incident.
- When in doubt for either: **discard**.

The full authoring guides also live as work references and are auto-injected when you edit the
target files: `references/conversation/用語集.md` (on `.claude/rules/glossary.md`) and
`references/conversation/インシデント.md` (on `.claude/rules/incidents.md` / `.claude/references/incidents/**`).

### Official docs

- Skills: **https://code.claude.com/docs/en/skills**
- Path-scoped rules: **https://code.claude.com/docs/en/memory**
- Hooks: **https://code.claude.com/docs/en/hooks**
