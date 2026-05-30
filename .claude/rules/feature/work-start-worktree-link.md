---
paths:
  - "plugins/workspace/skills/work-start/SKILL.md"
  - "plugins/workspace/skills/work-add/SKILL.md"
  - "plugins/workspace/skills/vscode-workspace-sync/SKILL.md"
---

# work-start ↔ worktree skills Link Rule

## Overview

PR163 merged the worktree-kit plugin into workspace. The two worktree-related skills
(`work-add` / `vscode-workspace-sync`) now live under workspace.
`work-start` Step 4 delegates to `workspace:work-add`, so their interfaces must stay aligned.

## File dependencies

| Edited file | Also verify / update |
|---|---|
| `plugins/workspace/skills/work-start/SKILL.md` | `plugins/workspace/skills/work-add/SKILL.md` — confirm the interface (PR number / branch args) matches |
| `plugins/workspace/skills/work-add/SKILL.md` | `plugins/workspace/skills/work-start/SKILL.md` — confirm the Step 4 call form matches |
| `plugins/workspace/skills/vscode-workspace-sync/SKILL.md` | confirm the namespace is `workspace:` |

## Toggling worktree usage

- Worktree usage is controlled by the `WORK_KIT_USE_WORKTREE` env var (enabled by default)
- Setting `false` / `0` / `no` / `off` makes `work-start` skip worktree creation and run with `.work/` management only
- This check is performed by `work-start` Step 4

## Rule Maintenance

- Added / removed / renamed a worktree-related skill → update `paths:` and the dependency table
- Changed the env var semantics → keep the Overview and `work-start` Step 4 in sync
