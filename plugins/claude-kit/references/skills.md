# Skills Authoring Guide

How to design, create, and evaluate `.claude/skills/<name>/SKILL.md` files.
A skill is an on-demand workflow — invoked explicitly (`/skill-name`) or auto-triggered via its
`description` frontmatter. This guide is self-contained: when it is injected (because you are
editing a `SKILL.md`), follow it to author the file directly. Read `common.md` alongside it for
file-type decisions, JP/EN mirror rules, and the provenance-stamping step.
Japanese mirror: `references/skills.jp.md`

---

## When skills load

- When explicitly invoked as `/skill-name`
- When the `description` frontmatter condition is matched (auto-trigger)

Do not use `disable-model-invocation: true` by default.
**Exception**: use it for skills that must only be run by a human (merge, deploy, destructive operations).
Skills with that flag do not need a "no autonomous invocation" prohibition — the flag already enforces it.

---

## Step 1 — Confirm a skill is the right type

Before writing, validate the choice against the content:

| If the content is… | Verdict |
|---|---|
| Multi-step workflow with user interaction or branching | ✅ Skill — correct |
| Repeated routine that needs user confirmation points | ✅ Skill — correct |
| 3+ distinct steps | ✅ Skill — correct |
| 1–2 simple rules or conventions | ⚠️ `CLAUDE.md` or `.claude/rules/` is simpler |
| Cross-path file sync ("edit X → also update Y, Z") | ⚠️ `.claude/rules/` is more appropriate |
| Something that should auto-fire every time | ⚠️ `hooks` |
| Mix of workflow + sync rules | ⚠️ Split: skill for the workflow, rules for the sync |

If another file type fits better, redirect (see `common.md` for the full decision table).

---

## Step 2 — Check for existing similar skills

1. Glob `.claude/skills/**/SKILL.md` and read each `description` + overview.
2. If a skill has overlapping triggers or similar steps:
   - **Merge** — extend the existing skill to cover this case too (preferred when triggers overlap), or
   - **Keep separate** — only with a clear boundary (distinct trigger conditions, different user flows).
3. No overlap → proceed.

---

## Step 3 — `description` frontmatter (the auto-trigger)

Write it precisely — "when the user says X". Vague descriptions cause false positives.
Only `name` and `description` are needed. Do **not** add `allowed-tools`.

```yaml
---
name: skill-name
description: |
  Trigger when the user says "〜したい", "〜して", or calls `/namespace:skill-name` explicitly.
---
```

---

## Step 4 — Write the JP mirror first (`SKILL.jp.md`), then translate

Per `common.md`, author `.claude/skills/<name>/SKILL.jp.md` in Japanese first, then produce the
English `SKILL.md` from it (by hand or via the `jp-mirror-translator` agent). Stamp both files
(provenance step in `common.md`).

### Step structure

Each step follows this pattern. Use only the subsections a given step needs:

```markdown
### Step N: (Action name)

#### Condition
(Prerequisites for entering this step)

#### Input
(Data, files, prior step output, or user input used here)

#### Process
1. Do X
→ Proceed to Step N+1

#### Output
(What exists when this step is complete)

#### Notes
##### Checklist
##### Branching
##### Prohibitions
```

To delegate a step to a subagent, prefix the item with a delegation marker (see `subagents.md`):

```markdown
#### Process
1. [subagent: parallel · await all] Glob .claude/skills/ and collect each description
   (return: `[{name, description}]`)
→ Proceed to Step 2
```

### Full SKILL.md skeleton

```markdown
---
name: <skill-name>
description: |
  Precise trigger conditions. "When the user says X", "when editing Y".
---

# <skill-name> — one-line summary

<1–2 sentences: what this skill does.>

---

## Overview

<Background, purpose, why this skill exists.>

---

## Tasks

### Step 1: <action>
...
```

---

## Reference material placement

- **Used by multiple steps** → put in a `## References` section at the bottom
- **Used by only one step** → embed directly in that step

For large skills, extract heavy reference material to `references/` and link by path from the skill.

> Note: a skill cannot take CLI-style arguments — it is a Markdown file loaded into context.
> Describe expected inputs as natural-language bullets, never as a `--flag` table.

---

## Final checklist

- [ ] `SKILL.md` (English, loaded by Claude) and `SKILL.jp.md` (JP mirror) both exist with matching structure
- [ ] `description` frontmatter has precise trigger conditions; only `name` + `description` set
- [ ] Shared content is in `## References`; single-step content stays in its step
- [ ] Both files stamped per `provenance.md` (auto-injected when you write the file)

---

## JP Mirror Sync

When editing `SKILL.md`, **update `SKILL.jp.md` in the same commit**.

| Edited file | Must also update |
|---|---|
| `plugins/{name}/skills/{skill}/SKILL.md` | `plugins/{name}/skills/{skill}/SKILL.jp.md` |

### Checklist before committing

- [ ] Changes in `SKILL.md` are reflected in `SKILL.jp.md` in Japanese
- [ ] Section structure in `SKILL.jp.md` matches `SKILL.md`
- [ ] `SKILL.jp.md` has the JP mirror warning comment at the top (`<!-- This file is a Japanese mirror... -->`)
