# work — Project Lifecycle Management

Hook-based project lifecycle management for Claude Code. Injects branch context on every prompt,
reminds task updates on stop, manages worktrees, and guards force-operations on protected branches.

## Skills

| # | Skill | Purpose |
|---|---|---|
| 1 | `work:start` | Create a new branch + branch document in `.work/tasks/` |
| 2 | `work:pr-handoff` | Reserve the next branch after the current one is complete |
| 3 | `work:pr-show` | Show next branch candidates in 3 categories (ready / in-progress / conditional) |
| 4 | `work:merge` | Merge the current branch, close related issues, archive the branch document |
| 5 | `work:qa-review` | Review QA items in the current branch document |
| 6 | `work:plugin-config` | Interactively configure work env toggles in `settings.json` |
| 7 | `work:issue-create` | Create issue files under `.work/issues/` |
| 8 | `work:issue-scan` | Scan a random source file for rule violations, record as issues |
| 9 | `work:issue-save` | Save a one-off issue from conversation |
| 10 | `work:impl-review` | Review implementation against the branch document |
| 11 | `work:setup` | Initialize `.work/` directory structure from templates |
| 12 | `work:plugin-migrate` | Update `.work/` static templates to the current work version |
| 13 | `work:worktree-create` | Create a git worktree for a branch |
| 14 | `work:vscode-workspace-sync` | Keep a VS Code `.code-workspace` file in sync with git worktrees |
| 15 | `work:branch-index-cleanup` | Remove stale entries from `.work/tasks/index.yaml` |

## Hooks

| # | Event | Trigger | Script / Prompt |
|---|---|---|---|
| 1 | `PreToolUse` | Edit / Write / MultiEdit / Read | `hooks/scripts/inject_references.py` — reference auto-injection |
| 2 | `PreToolUse` | Bash | `hooks/prompts/master-commit-guard.md` — block commits to protected branches |
| 3 | `PreToolUse` | Bash | `hooks/prompts/git-guard.md` — confirm `git push` / `git merge` |
| 4 | `UserPromptSubmit` | — | `hooks/prompts/user-prompt-submit.md` — inject branch context before each prompt |
| 5 | `Stop` | — | `hooks/prompts/stop.md` — remind task update / propose merge |

## Environment Variables

| # | Variable | Default | Description |
|---|---|---|---|
| 1 | `WORK_USE_WORKTREE` | `true` | Create git worktrees for new branches |
| 2 | `WORK_GUARD` | `true` | Enable git-guard hook (confirm push/merge) |
| 3 | `WORK_PROTECTED_BRANCHES` | `master,main,develop` | Comma-separated list of branches protected by master-commit-guard |
| 4 | `WORKSPACE_STOP_REMINDER` | `true` | Show task-update reminder on Stop |
| 5 | `WORKSPACE_MERGE_PROPOSAL` | `true` | Suggest running `/work:merge` on Stop |
| 6 | `CLAUDE_KIT_INJECTION_DISABLE` | (off) | Disable reference injection (kill switch) |
| 7 | `DEV_KIT_INJECTION_DISABLE` | (off) | Disable dev-kit reference injection |

## Branch Document Structure

Each branch uses a single file at `.work/tasks/{YYMMDD}_{title}/{branch-hyphenated}.md` with sections:

- `## 作業内容` — task description and checklist
- `## QA` — questions to resolve before implementation
- `## テスト` — test items
- `## 変更内容` — implementation notes

Branches are named `{type}/{title}` (no PR-number prefix); internal IDs are tracked in `index.yaml`.

## Changelog

| # | Version | Date | Summary |
|---|---|---|---|
| 1 | 2.48.0 | 2026-05-30 | Remove `work:notes-to-claude` skill — inter-plugin dependency eliminated |
| 2 | 2.47.0 | 2026-05-30 | Add `CLAUDE_KIT_INJECTION_DISABLE` / `DEV_KIT_INJECTION_DISABLE` to `work:plugin-config` managed toggles |
| 3 | 2.46.2 | 2026-05-30 | Fix `issue-scan` skill: remove stale `py-kit`/`next-kit` references, update to `_injection_rules.yaml` |
| 4 | 2.46.0 | 2026-05-30 | Extract Stop hook inline python to `hooks/scripts/stop.py` + `_common.py` |
| 5 | 2.44.0 | 2026-05-30 | Unify branch document to single file (`{branch-hyphenated}.md`); rename `plugin-migrate` skill |
| 6 | 2.43.0 | 2026-05-30 | Add `WORKSPACE_MERGE_PROPOSAL` env toggle |
| 7 | 2.42.0 | 2026-05-30 | Add `WORKSPACE_PROTECTED_BRANCHES` env toggle |
| 8 | 2.41.0 | 2026-05-30 | Change `impl-review` Step 4 to batch AskUserQuestion (max 4 per call) |
| 9 | 2.40.0 | 2026-05-30 | Integrate `guard-kit` into work plugin |
| 10 | 2.39.0 | 2026-05-30 | Add `work:plugin-config` skill for interactive env toggle configuration |
