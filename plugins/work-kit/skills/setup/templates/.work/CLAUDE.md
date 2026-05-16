> Japanese mirror: `CLAUDE.jp.md` (human reference only — not auto-loaded by Claude Code)
> When editing: update the JP mirror first, then apply the same change here.

# .work/ — work-kit Task Management Directory

Managed by the work-kit plugin. Claude reads and writes files here to track task and PR lifecycle state.

---

## Directory Structure

| Path | Purpose |
|---|---|
| `tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md` | PR task checklist and spec references |
| `specs/{feature-name}.md` | Feature specifications (referenced across tasks) |
| `QA.md` | Open questions and unresolved design decisions |

---

## Conventions

- Read the active PR's `TODO.md` before starting work to confirm scope
- Mark completed tasks as `- [x]`
- Reflect spec changes in the relevant `specs/` document
- Append unresolved questions to `QA.md`
- Confirm all `## TODO` items are `- [x]` before merging

---

## work-kit Skills

| Skill | Purpose |
|---|---|
| `/work-kit:setup` | Initialize `.work/` (run once per project) |
| `/work-kit:work-start` | Create task folder, PR folder, and TODO.md |
| `/work-kit:merge` | Verify TODO, merge, and clean up worktree |
