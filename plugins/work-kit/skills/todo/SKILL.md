---
name: todo
description: |
  Rules for creating and updating TODO.md in .work/tasks/.../PR{N}/.
  Trigger when creating a new TODO.md, updating a checklist, or when the user says
  "TODOを書いて", "TODO更新して", "チェックリスト更新".
allowed-tools: Read Write
---

# work-kit:todo — TODO.md Rules

Defines how to create and maintain `TODO.md`. It is the single source of truth for what a PR does.
Keep it ahead of implementation — a doc that lags behind the actual work is worse than none.

---

## Tasks

### Step 1: Create TODO.md

#### Condition

- A new PR folder has been created by `/work-kit:work-start`

#### Process

1. Create `.work/tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md`:

```markdown
# PR{N} — {title}

## 仕様参照

<!-- Links to related specs -->
<!-- Example: [Feature](../../../specs/{spec-name}.md) -->

## TODO

- [ ] {task item — specific enough to say what file and why}
- [ ] {task item}

## 変更ファイル

<!-- Fill in after committing -->
```

2. Add links to relevant `specs/` documents in `## 仕様参照`

→ Done

#### Notes

##### Prohibitions

- Do not create TODO.md after implementation has started — always create it first
- Do not write vague items like "check X" — specify what changes and why

---

### Step 2: Update TODO.md

#### Condition

- A task is completed
- Scope changes during implementation (additional work or direction change)

#### Process

**When a task is completed:**
1. Mark the item as `- [x]`

**When scope changes (higher priority):**
1. Stop implementation and update TODO.md first
2. Add new tasks as `- [ ]` in `## TODO`
3. Resume implementation following the updated document

→ Done

#### Notes

##### Prohibitions

- Never let TODO.md fall behind the actual work — the document leads implementation

---

### Step 3: Pre-merge check

#### Condition

- Before running `/work-kit:merge`

#### Process

1. Confirm all items in `## TODO` are `- [x]`
2. If any `- [ ]` remain, do not merge — complete them first

#### Notes

##### Checklist

- [ ] All `## TODO` items are `- [x]`
- [ ] `## 変更ファイル` lists the changed files
