# Skills Design Guide

Reference for designing, creating, and evaluating `.claude/skills/<name>/SKILL.md` files.
Japanese mirror: `references/skills.jp.md`

---

## When skills load

- When explicitly invoked as `/skill-name`
- When the `description` frontmatter condition is matched (auto-trigger)

Do not use `disable-model-invocation: true` by default.
**Exception**: use it for skills that must only be run by a human (merge, deploy, destructive operations).

---

## When to use skills vs other types

**Good fit for skills**:
- 3 or more steps
- User confirmation points exist
- Branching logic is needed
- Repeated routine work

**Not a good fit**:
- Simple 1–2 line rules → `CLAUDE.md` or `.claude/rules/`
- File-edit-triggered sync reminders → `.claude/rules/`
- Things that should auto-fire every time → `hooks`

---

## `description` frontmatter

The auto-trigger. Write it precisely — "when the user says X". Vague descriptions cause false positives.

```yaml
---
name: skill-name
description: |
  Trigger when the user says "〜したい", "〜して", or calls `/namespace:skill-name` explicitly.
---
```

---

## Step structure

Each step follows this pattern:

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

---

## Reference material placement

- **Used by multiple steps** → put in `## References` section at the bottom
- **Used by only one step** → embed directly in that step

For large skills, extract heavy reference material to `references/` and link by path from the skill.
