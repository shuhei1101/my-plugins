# work — Project Lifecycle Management

Hook-based project lifecycle management for Claude Code. Injects branch context on every prompt,
reminds task updates on stop, manages worktrees, and guards force-operations on protected branches.

## Lifecycle

The plugin enforces a "one task = one branch" lifecycle through hooks. The full flow:

1. **Prompt received → branch gate** (`UserPromptSubmit` hook / `hooks/prompts/user-prompt-submit.md`)
   Determines whether a branch is in progress this session.
   - **No branch** → `work:start` must run before editing or committing anything (editing/committing without a branch, and committing directly to master, are prohibited).
   - **Branch in progress** → move to its worktree and read the branch document. If `## QA` has unresolved entries, **stop there** and ask the user to resolve them. If clear, add the new request to `## 作業内容`, then continue.

2. **Branch creation** (`work:start` → `work:worktree-create`)
   Decide the branch name (`{type}/{title}`, with an author segment when `WORK_BRANCH_AUTHOR` is set) → collect details (Japanese title, TODOs, note, open questions) → add an `index.yaml` entry in the main repo → create the worktree + branch → choose/create the task folder → author the branch document from the injected template → record open questions in `## QA` → **first commit (branch document only)**.

3. **Implementation** (inside the worktree)
   Edits and commits happen on the branch. Two `PreToolUse(Bash)` guards protect the repo: `master-commit-guard` blocks `git commit` on protected branches (`master` / `main` / `develop`), and `git-guard` confirms `git push` / non-upstream `git merge`.

4. **Final commit** (`work:start` Step 9)
   Update or create the related note in `.work/notes/`, link it from `## 参考ドキュメント`, update `_index.md`, and commit the note + branch document together as the last commit.

5. **Response end → stop reminder** (`Stop` hook / `hooks/prompts/stop.md`)
   Mark finished `## 作業内容` rows with `済`, confirm `## QA` is clear and the note is updated, then **suggest running `/work:merge`** (suppressed when `WORK_MERGE_PROPOSAL` is falsy → uses `stop-no-merge.md`).

6. **Merge** (`work:merge`)
   Verify the TODO checklist → merge the parent branch in → **close related issues** (each `## 関連イシュー` row via `issue-tool.py close`, moving it to `.work/issues/closed/` and recording it in `_index.archive.yaml`) → mark the branch completed in `index.yaml` → archive the branch document → `--no-ff` merge into the parent → remove the worktree → confirm remaining QA → auto-invoke `branch-reserve` for next candidates.

**Issue sub-cycle**: issues live in `.work/issues/ISSUE-{N}.md`, are created by `issue-create` / `issue-scan`, and the ones listed in a branch's `## 関連イシュー` are closed automatically at merge time (above).

## Skills

| # | Skill | Purpose |
|---|---|---|
| 1 | `work:start` | Create a new branch + branch document in `.work/tasks/` |
| 2 | `work:pr-handoff` | Reserve the next branch after the current one is complete |
| 3 | `work:pr-show` | Show next branch candidates in 3 categories (ready / in-progress / conditional) |
| 4 | `work:merge` | Merge the current branch, close related issues, archive the branch document |
| 5 | `work:qa-wizard` | Present unresolved QA items and collect decisions |
| 6 | `work:plugin-config` | Interactively configure work env toggles in `settings.json` |
| 7 | `work:issue-create` | Create issue files under `.work/issues/` |
| 8 | `work:issue-scan` | Orchestrate parallel `work:issue-scanner` subagents to scan perspectives; record findings as issues and auto-merge |
| 9 | `work:impl-review` | Review implementation against the branch document |
| 10 | `work:setup` | Initialize `.work/` directory structure from templates |
| 11 | `work:plugin-migrate` | Update `.work/` static templates to the current work version |
| 12 | `work:worktree-create` | Create a git worktree for a branch |
| 13 | `work:vscode-workspace-sync` | Keep a VS Code `.code-workspace` file in sync with git worktrees |
| 14 | `work:branch-index-cleanup` | Remove stale entries from `.work/tasks/index.yaml` |

## Agents

| # | Agent | Purpose |
|---|---|---|
| 1 | `work:issue-scanner` | Scan one perspective (folder / grep / layer / file-group) against ref-inject references and write ISSUE files; spawned by `work:issue-scan` |

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
| 6 | `WORK_BRANCH_AUTHOR` | (empty) | Author name inserted into branch names: `{type}/{author}/{title}` |
| 7 | `CLAUDE_KIT_INJECTION_DISABLE` | (off) | Disable reference injection (kill switch) |
| 8 | `DEV_KIT_INJECTION_DISABLE` | (off) | Disable dev-kit reference injection |
| 9 | `WORK_COMMIT_LANG` | `JP` | Language of commit messages: `JP` = Japanese, `EN` = English |
| 10 | `WORK_COMMIT_TYPE` | `true` | Include conventional commit type prefix (`feat:`, `fix:`, `chore:`, etc.) |
| 11 | `ISSUE_SCAN_AGENTS` | `1` | Perspectives scanned per `issue-scan` run (= parallel `issue-scanner` subagents) |

## Branch Document Structure

Each branch uses a single file at `.work/tasks/{YYMMDD}_{title}/{YYMMDD}-{日本語タイトル}.md` with sections:

- `## 作業内容` — task description and checklist
- `## QA` — questions to resolve before implementation
- `## テスト` — test items
- `## 変更内容` — implementation notes

Branches are named `{type}/{title}` by default; `{type}/{author}/{title}` when `WORK_BRANCH_AUTHOR` is set. Internal IDs are tracked in `index.yaml`.

## Changelog

| # | Version | Date | Summary |
|---|---|---|---|
| 1 | 2.59.0 | 2026-06-01 | Remove `work:setup-wizard` skill and `SessionStart` hook (`setup_check.py`) |
| 2 | 2.56.0 | 2026-05-31 | Redesign `issue-scan` as an orchestrator delegating to parallel `work:issue-scanner` subagents (new agent); scan by perspective (folder/grep/layer/file-group); add `ISSUE_SCAN_AGENTS`; remove `issue-save` skill — issue file format now in the `work-dir/イシュー` reference, authored by `issue-create` and `issue-scanner` |
| 2 | 2.55.0 | 2026-05-31 | Remove `plugins/work/templates/` and `setup-task.py`; move templates/structure defs into `references/work-dir/` (`タスクドキュメント` / `タスクインデックス` / `イシュー` / `ワークディレクトリ構成`), injected by ref-inject on the matching `.work/` path. `work:start` authors the branch doc from the injected template; branch doc filename gains `.branch.md`. Rename `ドットワークディレクトリ構成`→`ワークディレクトリ構成`; remove `TODOテンプレート同期` |
| 3 | 2.54.0 | 2026-05-31 | index.yaml branch index keyed by `branch` (drop id/last_id/tags); add `created` surrogate; legacy backlog migrated to `index.archive.yaml`; `next-id` removed and `set-completed` switched to `--branch` |
| 4 | 2.53.1 | 2026-05-31 | Split `references/` into category subfolders: `notes/`, `work-dir/`, `skill-sync/` |
| 2 | 2.53.0 | 2026-05-31 | Redefine notes as a current spec sheet (snapshot; no history in the body, `## 変更履歴` table only, no frontmatter); add `ノート記述内容ルール` reference; merge `.work/specs` into notes and remove the folder |
| 2 | 2.52.0 | 2026-05-31 | Branch doc filename uses Japanese title (`{YYMMDD}-{日本語タイトル}.md`); add `branch` field to `index.yaml` |
| 2 | 2.51.0 | 2026-05-31 | Add `WORK_COMMIT_LANG` / `WORK_COMMIT_TYPE` env vars — configurable commit message language and type prefix |
| 2 | 2.50.0 | 2026-05-31 | Add `WORK_BRANCH_AUTHOR` env var — insert author name into branch names |
| 2 | 2.48.0 | 2026-05-30 | Remove `work:notes-to-claude` skill — inter-plugin dependency eliminated |
| 3 | 2.47.0 | 2026-05-30 | Add `CLAUDE_KIT_INJECTION_DISABLE` / `DEV_KIT_INJECTION_DISABLE` to `work:plugin-config` managed toggles |
| 4 | 2.46.2 | 2026-05-30 | Fix `issue-scan` skill: remove stale `py-kit`/`next-kit` references, update to `_injection_rules.yaml` |
| 5 | 2.46.0 | 2026-05-30 | Extract Stop hook inline python to `hooks/scripts/stop.py` + `_common.py` |
| 6 | 2.44.0 | 2026-05-30 | Unify branch document to single file (`{branch-hyphenated}.md`); rename `plugin-migrate` skill |
| 7 | 2.43.0 | 2026-05-30 | Add `WORKSPACE_MERGE_PROPOSAL` env toggle |
| 8 | 2.42.0 | 2026-05-30 | Add `WORKSPACE_PROTECTED_BRANCHES` env toggle |
| 9 | 2.41.0 | 2026-05-30 | Change `impl-review` Step 4 to batch AskUserQuestion (max 4 per call) |
| 10 | 2.40.0 | 2026-05-30 | Integrate `guard-kit` into work plugin |
| 11 | 2.39.0 | 2026-05-30 | Add `work:plugin-config` skill for interactive env toggle configuration |
| 1 | 2.57.0 | 2026-05-31 | Task folder names are now Japanese (`{YYMMDD}_{日本語タイトル}`); existing 217 folders renamed in bulk, `index.archive.yaml` `task:` fields followed (8→6 digit normalized), and `work:start` / `work-dir` references updated to the Japanese-name convention |
| 2 | 2.56.0 | 2026-05-31 | Redesign `issue-scan` as an orchestrator delegating to parallel `work:issue-scanner` subagents (new agent); scan by perspective (folder/grep/layer/file-group); add `ISSUE_SCAN_AGENTS`; remove `issue-save` skill — issue file format now in the `work-dir/イシュー` reference, authored by `issue-create` and `issue-scanner` |
| 3 | 2.55.0 | 2026-05-31 | Remove `plugins/work/templates/` and `setup-task.py`; move templates/structure defs into `references/work-dir/` (`タスクドキュメント` / `タスクインデックス` / `イシュー` / `ワークディレクトリ構成`), injected by ref-inject on the matching `.work/` path. `work:start` authors the branch doc from the injected template; branch doc filename gains `.branch.md`. Rename `ドットワークディレクトリ構成`→`ワークディレクトリ構成`; remove `TODOテンプレート同期` |
| 4 | 2.54.0 | 2026-05-31 | index.yaml branch index keyed by `branch` (drop id/last_id/tags); add `created` surrogate; legacy backlog migrated to `index.archive.yaml`; `next-id` removed and `set-completed` switched to `--branch` |
| 5 | 2.53.1 | 2026-05-31 | Split `references/` into category subfolders: `notes/`, `work-dir/`, `skill-sync/` |
| 3 | 2.53.0 | 2026-05-31 | Redefine notes as a current spec sheet (snapshot; no history in the body, `## 変更履歴` table only, no frontmatter); add `ノート記述内容ルール` reference; merge `.work/specs` into notes and remove the folder |
| 3 | 2.52.0 | 2026-05-31 | Branch doc filename uses Japanese title (`{YYMMDD}-{日本語タイトル}.md`); add `branch` field to `index.yaml` |
| 3 | 2.51.0 | 2026-05-31 | Add `WORK_COMMIT_LANG` / `WORK_COMMIT_TYPE` env vars — configurable commit message language and type prefix |
| 3 | 2.50.0 | 2026-05-31 | Add `WORK_BRANCH_AUTHOR` env var — insert author name into branch names |
| 3 | 2.48.0 | 2026-05-30 | Remove `work:notes-to-claude` skill — inter-plugin dependency eliminated |
| 4 | 2.47.0 | 2026-05-30 | Add `CLAUDE_KIT_INJECTION_DISABLE` / `DEV_KIT_INJECTION_DISABLE` to `work:plugin-config` managed toggles |
| 5 | 2.46.2 | 2026-05-30 | Fix `issue-scan` skill: remove stale `py-kit`/`next-kit` references, update to `_injection_rules.yaml` |
| 6 | 2.46.0 | 2026-05-30 | Extract Stop hook inline python to `hooks/scripts/stop.py` + `_common.py` |
| 7 | 2.44.0 | 2026-05-30 | Unify branch document to single file (`{branch-hyphenated}.md`); rename `plugin-migrate` skill |
| 8 | 2.43.0 | 2026-05-30 | Add `WORKSPACE_MERGE_PROPOSAL` env toggle |
| 9 | 2.42.0 | 2026-05-30 | Add `WORKSPACE_PROTECTED_BRANCHES` env toggle |
| 10 | 2.41.0 | 2026-05-30 | Change `impl-review` Step 4 to batch AskUserQuestion (max 4 per call) |
| 11 | 2.40.0 | 2026-05-30 | Integrate `guard-kit` into work plugin |
| 12 | 2.39.0 | 2026-05-30 | Add `work:plugin-config` skill for interactive env toggle configuration |