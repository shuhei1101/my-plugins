> Japanese mirror: `CLAUDE.jp.md` (human reference only — not auto-loaded by Claude Code)
> When editing: update the JP mirror first, then apply the same change here.

# .work/ — work-kit Task Management Directory

Managed by the work-kit plugin. Claude reads and writes files here to track task and PR lifecycle state.

---

## Directory Structure

| Path | Purpose |
|---|---|
| `tasks/index.yaml` | PR index (`completed: false` = in progress) |
| `tasks/{YYYYMMDD}_{title}/PR{N}/TODO.md` | PR task checklist and spec references |
| `tasks/{YYYYMMDD}_{title}/PR{N}/QA.md` | Unresolved questions scoped to this PR |
| `specs/{feature-name}.md` | Feature specifications (referenced across tasks) |

### tasks/

`tasks/index.yaml` is the single source of truth for PR status. In-progress PRs have `completed: false`; merged ones have `completed: true`. Always read index.yaml at the start of a session to identify the active PR.

One folder per task (`{YYYYMMDD}_{title}/`), containing one or more PR folders (`PR{N}/`).
Each PR folder holds `TODO.md` (task checklist) and `QA.md` (unresolved questions for this PR).

`TODO.md` is the single source of truth for what a PR does. Create it before starting implementation and keep it current. Mark completed tasks as `- [x]`; confirm all items are checked before merging.

`QA.md` records unresolved questions scoped to this PR. When the user decides, reflect the decision in the relevant spec or document.

### specs/

Flat structure (**no subfolders**). One-fact-one-document: never duplicate content; use links instead.
Update specs whenever implementation changes documented behavior.

---

## Conventions

- Read `tasks/index.yaml` at session start to find the active PR
- Mark completed tasks as `- [x]`
- Reflect spec changes in the relevant `specs/` document
- Append unresolved questions to the PR's `QA.md`
- Confirm all `## TODO` items are `- [x]` before merging

---

## work-kit Skills

| Skill | Purpose |
|---|---|
| `/work-kit:setup` | Initialize `.work/` (run once per project) |
| `/work-kit:work-start` | Create task folder, PR folder, TODO.md, QA.md, and index.yaml entry |
| `/work-kit:merge` | Verify TODO, merge, update index.yaml, and clean up worktree |
