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

### tasks/

One folder per task (`{YYYYMMDD}_{title}/`), containing one or more PR folders (`PR{N}/`).
A single task may span multiple PRs.

`TODO.md` is the single source of truth for what a PR does. Create it before starting implementation and keep it current throughout. Mark completed tasks as `- [x]`; confirm all items are checked before merging.
When scope changes, update `TODO.md` before continuing implementation — a doc that lags behind the actual work is worse than none.

### specs/

Flat structure (**no subfolders**). Follow the one-fact-one-document principle: never duplicate content across files; use links instead.

Update specs whenever implementation changes documented behavior.
When an unresolved question arises while writing a spec, record it immediately in `QA.md` — do not leave `TBD` or `要検討` markers in the spec body.

### QA.md

Records unresolved design and implementation questions. Two sections: `## 進行中` (open) and `## 解決済み` (resolved).

Add entries immediately when questions arise. Always include a recommended approach with reasoning — deferring without a recommendation is not allowed.
When resolved: reflect the decision in the relevant spec, then move the entry to `## 解決済み` and remove it from `## 進行中` entirely.

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
