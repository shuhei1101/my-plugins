> Japanese mirror: `CLAUDE.jp.md` (human reference only — not auto-loaded by Claude Code)
> When editing: update the JP mirror first, then apply the same change here.

# .work/ — work-kit Task Management Directory

This directory is managed by the work-kit plugin.
Claude reads and writes files here to track task and PR lifecycle state.

---

## Directory Structure

```
.work/
├── tasks/
│   └── {YYYYMMDD}_{title}/       # Task folder (one per new request)
│       └── PR{N}/                # PR folder (a task may have multiple PRs)
│           └── TODO.md           # Checklist and spec references for this PR
├── specs/                        # Feature specifications (referenced across tasks)
│   └── {feature-name}.md
└── QA.md                         # Open questions and unresolved design decisions
```

---

## Tasks

### Step 1: Starting new work

#### Process

1. Run `/work-kit:work-start`
2. Follow the skill to create TODO.md, spec doc, and QA entries
3. Wait for user approval before starting implementation

---

### Step 2: During implementation

#### Process

1. Read the active PR's `TODO.md` before starting work to confirm scope
2. Mark completed tasks as `- [x]`
3. Update `specs/` if any specification changes
4. Append unresolved questions or decisions to `QA.md`

---

### Step 3: Merging a PR

#### Process

1. Confirm all items in `TODO.md`'s `## TODO` section are `- [x]`
2. Run `/work-kit:merge`
3. After merge, move resolved items in `QA.md` to the `## 解決済み` section

---

## References

### work-kit skills

| Skill | Purpose |
|---|---|
| `/work-kit:setup` | Initialize `.work/` (run once per project) |
| `/work-kit:work-start` | Create task folder, PR folder, and TODO.md |
| `/work-kit:merge` | Verify TODO, merge, and clean up worktree |

### Correspondence table

| File path | Description |
|---|---|
| `.work/tasks/{date}_{title}/PR{N}/TODO.md` | PR task checklist and spec links |
| `.work/specs/{feature-name}.md` | Feature specification document |
| `.work/QA.md` | Open questions and design decisions |
