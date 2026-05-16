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
| `specs/{feature-name}.md` | Feature specifications (referenced across tasks) |
| `QA.md` | Open questions and unresolved design decisions |

### tasks/

`tasks/index.yaml` is the single source of truth for PR status. In-progress PRs have `completed: false`; merged ones have `completed: true`. Always read index.yaml at the start of a session to identify the active PR.

One folder per task (`{YYYYMMDD}_{title}/`), containing one or more PR folders (`PR{N}/`).
`TODO.md` is the single source of truth for what a PR does. Create it before starting implementation and keep it current. Mark completed tasks as `- [x]`; confirm all items are checked before merging.

### specs/

Flat structure (**no subfolders**). One-fact-one-document: never duplicate content; use links instead.
Update specs whenever implementation changes documented behavior.
When an unresolved question arises, record it in `QA.md` immediately — do not leave `TBD` or `要検討` in the spec body.

### QA.md

Records unresolved questions as QA-XXX numbered entries.
Always include a recommended approach — deferring without one is not allowed.
When resolved: reflect the decision in the relevant spec/document, then delete the QA entry.

---

## Conventions

- Read `tasks/index.yaml` at session start to find the active PR
- Mark completed tasks as `- [x]`
- Reflect spec changes in the relevant `specs/` document
- Append unresolved questions to `QA.md`
- Confirm all `## TODO` items are `- [x]` before merging

---

## work-kit Skills

| Skill | Purpose |
|---|---|
| `/work-kit:setup` | Initialize `.work/` (run once per project) |
| `/work-kit:work-start` | Create task folder, PR folder, TODO.md, and index.yaml entry |
| `/work-kit:merge` | Verify TODO, merge, update index.yaml, and clean up worktree |
