# work — Project Lifecycle Management

Hook-based project lifecycle management for Claude Code. Injects branch context on every prompt,
reminds task updates on stop, manages worktrees, and guards force-operations on protected branches.

## Lifecycle

The plugin enforces a "one task = one branch" lifecycle through hooks. The full flow:

1. **Prompt received → branch gate** (`UserPromptSubmit` hook / `hooks/prompts/user-prompt-submit.md`)
   Determines whether a branch is in progress this session.
   - **No branch** → run `/work:start` to create a branch. Committing without a branch, and committing directly to master, are prohibited.
   - **Branch in progress** → move to its worktree and read the task document. If `## QA` has unresolved entries, **stop there** and ask the user to resolve them. If clear, add the new request to `## 作業内容`, then continue.

2. **Branch creation** (`work:start` → `work:worktree-create`)
   Decide the branch name (`{type}/{title}`, with an author segment when `${WORK_BRANCH_AUTHOR}` is set) → collect details (Japanese title, TODOs, note, open questions) → add an `index.yaml` entry in the main repo → create the worktree + branch → choose/create the task folder → author the task document from the injected template → record open questions in `## QA` → **first commit (task document only)**.

3. **Implementation** (inside the worktree)
   Edits and commits happen on the branch. Two `PreToolUse(Bash)` guards protect the repo: `master-commit-guard` blocks `git commit` on protected branches (`master` / `main` / `develop`), and `git-guard` confirms `git push` / non-upstream `git merge`.

4. **Final commit** (`work:start` Step 9)
   Update or create the related note in `.work/notes/`, link it from `## 参考ドキュメント`, update `_index.md`, and commit the note + task document together as the last commit.

5. **Response end → stop reminder** (`Stop` hook / `hooks/prompts/stop.md`)
   Mark finished `## 作業内容` rows with `済`, confirm `## QA` is clear and the note is updated, then **suggest running `/work:merge`** (suppressed when `${WORK_MERGE_PROPOSAL}` is falsy → uses `stop-no-merge.md`).

6. **Merge** (`work:merge`)
   Verify the TODO checklist → merge the parent branch in → **close related issues** (each `## 関連イシュー` row via `issue-tool.py close`, moving it to `.work/issues/closed/` and recording it in `_index.archive.yaml`) → mark the branch completed in `index.yaml` → archive the task document → `--no-ff` merge into the parent → remove the worktree → confirm remaining QA → auto-invoke `branch-reserve` for next candidates.

**Issue sub-cycle**: issues live in `.work/issues/ISSUE-{N}.md` as a two-part Markdown file with
**no frontmatter** — the `# ユーザー回答欄` (user answer section: `## 意思` / `## QA`) at the **top**
first, then the AI-authored issue body after `---`. `## 意思` has three options — `対応する（自動マージ）`
/ `対応する（マージはAIに任せる）` / `対応しない` — pre-filled as unchecked checkboxes (`- [ ]`), the
user checks one with `[x]`. Each QA carries a number, title, and an AI 推奨; **choice-type** QA lists
its options as `- [ ]` checkboxes (user checks one), **input-type** QA leaves a `**回答**:` line (user
fills it in). Work state (`status` / `branches`) lives only in `_index.yaml`. The flow:
**create** (`issue-create` / `issue-scan` → answer-section scaffolding written at the top, 意思 + any QA
pre-filled, followed by the issue body) →
**review** (`issue-review`, mobile-first → user checks one `## 意思` option and answers each `## QA`
— choice-type by checking one box, input-type by filling in `**回答**:`) →
**resolve** (`issue-resolve` under `/loop`, one issue per tick → affirmative 意思 dispatches an
`issue-resolver` subagent; `direct_merge` is set by the chosen 意思 variant — `対応する（自動マージ）`
→ `true` (merges immediately), `対応する（マージはAIに任せる）` → the AI decides from the `_index.yaml`
`direct_merge` field or issue content (UI-related→`false`, others→`true`); negative 意思 closes on a
throwaway per-issue branch and merges it to master immediately within the same tick) →
**close** (`merge` closes an accept branch's `## 関連イシュー` as `resolved` when `direct_merge: false`;
the resolver itself closes when `direct_merge: true`; a reject is closed as `wontfix` and already
merged at resolve time). Because QA is settled on the issue at review time, the resolver subagent
reaches the final commit without stopping for questions.

## Skills

| # | Skill | Purpose |
|---|---|---|
| 1 | `work:start` | Create a new branch + task document in `.work/tasks/` |
| 2 | `work:branch-reserve` | Reserve the next branch using the same flow as `work:start`, after the current branch is complete |
| 3 | `work:branch-show` | Present next branch candidates in 3 categories (ready to start / in progress elsewhere / has conditions) |
| 4 | `work:merge` | Merge the current branch, close related issues, archive the task document |
| 5 | `work:qa-wizard` | Present unresolved QA items and collect decisions |
| 6 | `work:issue-create` | Create issue files under `.work/issues/` |
| 7 | `work:issue-scan` | Orchestrate parallel `work:issue-scanner` subagents to scan perspectives; record findings as issues and auto-merge |
| 8 | `work:issue-review` | Triage un-reviewed issues (check one `## 意思` option, answer each `## QA` — choice-type box or input-type `**回答**:`) — mobile-first via AskUserQuestion |
| 9 | `work:issue-resolve` | Loop-driven: work through reviewed issues — accept→`issue-resolver` subagent, reject→throwaway branch merged to master immediately |
| 10 | `work:impl-review` | Review implementation against the task document |
| 11 | `work:setup` | Initialize `.work/` directory structure from templates |
| 12 | `work:plugin-migrate` | Update `.work/` static templates to the current work version |
| 13 | `work:worktree-create` | Create a git worktree for a branch |
| 14 | `work:vscode-workspace-sync` | Keep a VS Code `.code-workspace` file in sync with git worktrees |
| 15 | `work:branch-index-cleanup` | Remove stale entries from `.work/tasks/index.yaml` |
| 16 | `work:conversation-to-claude` | Analyze the session and auto-generate artifacts (skill / rule / hook / CLAUDE.md / incidents / glossary); delegates to claude-kit creator skills |
| 17 | `work:plugin-config` | Interactively configure work plugin env toggles (branch enforcement, merge proposal, worktree, commit type, etc.) |

## Agents

| # | Agent | Purpose |
|---|---|---|
| 1 | `work:issue-scanner` | Scan one perspective (folder / grep / layer / file-group) against ref-inject references and write ISSUE files; spawned by `work:issue-scan` |
| 2 | `work:issue-resolver` | Resolve one accepted issue: create a branch, implement the fix, then either merge directly into master (`direct_merge: true`, default) or stop at the merge-waiting commit (`direct_merge: false`); spawned by `work:issue-resolve` |

## Hooks

| # | Event | Trigger | Script / Prompt |
|---|---|---|---|
| 1 | `PreToolUse` | Edit / Write / MultiEdit / Read | `hooks/scripts/inject_references.py` — reference auto-injection |
| 2 | `PreToolUse` | Bash | `hooks/prompts/master-commit-guard.md` — block commits to protected branches |
| 3 | `PreToolUse` | Bash | `hooks/prompts/git-guard.md` — confirm `git push` / `git merge` |
| 4 | `UserPromptSubmit` | — | `hooks/prompts/user-prompt-submit.md` — inject branch context before each prompt |
| 5 | `Stop` | — | `hooks/prompts/stop.md` — remind task update / propose merge |
| 6 | `PreCompact` | — | `hooks/prompts/pre-compact.md` — run `/work:conversation-to-claude` before `/compact` |

## Environment Variables

**Bold** = default value (applied when the key is unset). Booleans list `true` / `false` only (`1` / `yes` / `on` are also accepted as truthy).

| Variable | Description | Values |
|---|---|---|
| `${WORK_USE_WORKTREE}` | Create a git worktree for each new branch | - **true**<br>- false |
| `${WORK_GUARD}` | Enable the git-guard hook (confirm push / merge). When `false`, `issue-resolver` direct merges proceed without a confirmation prompt. | - **true**<br>- false |
| `${WORK_PROTECTED_BRANCHES}` | Branches protected by master-commit-guard (comma-separated) | **master,main,develop** |
| `${WORKSPACE_STOP_REMINDER}` | Show the task-update reminder on Stop | - **true**<br>- false |
| `${WORKSPACE_MERGE_PROPOSAL}` | Suggest running `/work:merge` on Stop | - **true**<br>- false |
| `${WORK_BRANCH_AUTHOR}` | Author segment inserted into branch names (`{type}/{author}/{title}`); set any name to enable | **(unset)** |
| `${WORK_BASE_BRANCH}` | Base branch for new worktrees; when set, `git worktree add` branches from this commit-ish instead of `HEAD` | **(unset)** |
| `${CLAUDE_KIT_INJECTION_DISABLE}` | Kill switch — a truthy value disables claude-kit reference injection | - true<br>- **false** |
| `${DEV_KIT_INJECTION_DISABLE}` | Kill switch — a truthy value disables dev-kit reference injection | - true<br>- **false** |
| `${WORK_COMMIT_LANG}` | Commit message language (`JP` = Japanese, `EN` = English) | - **JP**<br>- EN |
| `${WORK_COMMIT_TYPE}` | Include the conventional commit type prefix (`feat:` / `fix:` / `chore:` …) | - **true**<br>- false |
| `${ISSUE_SCAN_AGENTS}` | Perspectives scanned per `issue-scan` run (= parallel `issue-scanner` subagents); integer | **1** |
| `${ISSUE_RESOLVE_AGENTS}` | Maximum actionable issues processed per `issue-resolve` invocation (sequential); integer | **1** |
| `${WORK_PRECOMPACT_CONV2CLAUDE}` | Run `/work:conversation-to-claude` on `PreCompact` (before `/compact`) | - **true**<br>- false |
| `${WORK_MERGE_CONV2CLAUDE}` | Run `/work:conversation-to-claude` inside the worktree during `work:merge` | - **true**<br>- false |

## Task Document Structure

Each branch uses a single file at `.work/tasks/{YYMMDD}_{title}/{YYMMDD}-{日本語タイトル}.task.md` with sections:

- `## 作業内容` — task description and checklist
- `## QA` — questions to resolve before implementation
- `## テスト` — test items
- `## 変更内容` — implementation notes

Branches are named `{type}/{title}` by default; `{type}/{author}/{title}` when `${WORK_BRANCH_AUTHOR}` is set. Internal IDs are tracked in `index.yaml`.

## Changelog

| # | Version | Date | Summary |
|---|---|---|---|
| 1 | 2.76.0 | 2026-06-03 | Split `## 意思` `対応する` into two merge-mode options — `対応する（自動マージ）` (forces `direct_merge: true`) and `対応する（マージはAIに任せる）` (AI decides via the `_index.yaml` `direct_merge` field / content heuristic), so the user's choice drives `direct_merge` (explicit 自動マージ takes precedence; the heuristic is kept for the AI-delegated path); add **input-type QA** (free-form answer on a `**回答**:` line, no checkbox) alongside choice-type QA (checkbox); update `イシュー.md` template + JP mirror, `issue-create` / `issue-review` / `issue-resolve` / `issue-scan` / `issue-scanner` agent, and this CLAUDE.md |
| 〃 | 2.75.0 | 2026-06-03 | Move `# ユーザー回答欄` to the **top** of the issue file (before the AI body, after title/date); replace `**回答**: 対応する / 対応しない` and QA `**回答**: A / B` with Markdown unchecked checkboxes (`- [ ]`); remove the `> 回答方法:` explanation block; update `イシュー.md` template, `issue-create` / `issue-review` / `issue-resolve` / `issue-scan` / `issue-scanner` agent / `issue-resolver` agent, and this CLAUDE.md |
| 〃 | 2.74.0 | 2026-06-02 | Add `direct_merge` parameter to `issue-resolver` (default `true`) — when true the resolver merges the branch to master directly after the final commit and closes the issue; `issue-resolve` determines the value from `_index.yaml` or by analyzing issue content (UI-related→false, refactor/test/backend→true); `issue-scan` sets `direct_merge: true` in `_index.yaml` for single-solution non-UI issues; add `direct_merge` field to `_index.yaml` schema; document `WORK_GUARD=false` as the way to skip the merge-guard prompt during automated direct merges |
| 〃 | 2.73.0 | 2026-06-02 | `issue-scan` Step 0 now copies uncommitted `.work/issues/` changes from the main repo into the scan worktree before committing, so user-answered issue files are committed together with the scan results |
| 〃 | 2.72.0 | 2026-06-02 | Add `${ISSUE_RESOLVE_AGENTS}` env var (default `1`) — maximum actionable issues processed per `issue-resolve` invocation; issues are handled sequentially in ascending issue-number order; update `issue-resolve` SKILL.md + JP mirror and this CLAUDE.md |
| 〃 | 2.71.0 | 2026-06-02 | Move `# ユーザー回答欄` to the **bottom** of the issue file (after `---`, following the AI-authored body); update `イシュー.md` template, `issue-create` / `issue-review` / `issue-resolve`, the `issue-scanner` agent, and this CLAUDE.md |
| 〃 | 2.70.0 | 2026-06-02 | Remove `work:quick-task` skill and revert the UserPromptSubmit hook Step 3 to always run `work:start` |
| 〃 | 2.69.0 | 2026-06-02 | Rename the task-document file extension `.branch.md` → `.task.md` (matches the `tasks/` folder) and bulk-rename the 266 existing documents; rename the concept **"branch document" → "task document"** across all current-spec references / skills / agents / hooks / CLAUDE.md (changelog history left unchanged) |
| 1 | 2.68.0 | 2026-06-02 | Change `issue-resolve`'s REJECT flow: instead of accumulating rejects on a shared `chore/rejected-issues` branch, each reject is closed on a throwaway per-issue branch (`chore/reject-ISSUE-{N}`) and **merged to master immediately** within the same tick. The close runs in the **main repo** (not a worktree) so it updates the gitignored `_index.yaml` (the source of truth Step 1 reads); the gitignored edit survives the `master` switch while the tracked file move reaches master via the merge commit — keeping master and the issue index consistent every tick (no drift). Update `issue-resolve` SKILL + JP mirror and this CLAUDE.md (lifecycle prose + Skills table) |
| 1 | 2.67.0 | 2026-06-02 | Redesign the ISSUE user-answer section: move `# ユーザー回答欄` (`## 意思` / `## QA`) to the **top** of the file (answered-state visible without scrolling), AI-authored issue body below; each QA now carries a number, title, options, and an AI `**推奨**:`; drop `## 自由記述` (free-form notes go inline on the `## 意思` answer); replace the `回答候補`/blank-`回答` model — the AI pre-fills each `**回答**:` with all candidates and the user narrows it to one. Update `イシュー.md` template, `issue-create` / `issue-review` / `issue-resolve` / `issue-scan`, the `issue-scanner` / `issue-resolver` agents, and this CLAUDE.md |
| 1 | 2.66.0 | 2026-06-02 | Restore `work:plugin-config` skill — interactive env toggle configuration for work plugin variables |
| 2 | 2.65.1 | 2026-06-02 | Fix stale skill names in `## Skills` table: `work:pr-handoff` → `work:branch-reserve`, `work:pr-show` → `work:branch-show` |
| 2 | 2.65.0 | 2026-06-02 | Remove the interactive `work:plugin-config` skill (env toggles are edited directly in `settings.json`); reformat the `## Environment Variables` table to the unified 3-column layout (Variable / Description / Values, default in **bold**) |
| 1 | 2.64.0 | 2026-06-02 | Rename the glossary authoring-guide reference `references/conversation/` file to a Japanese name `用語集.md` (+ `.jp.md`) — drop the katakana filename; update `injection_rules` / `_index` / cross-links and all pointers accordingly |
| 1 | 2.63.0 | 2026-06-02 | Redesign the ISSUE file format: drop YAML frontmatter; two-part Markdown layout (AI-authored top half + `# ユーザー回答欄` with `## 意思` / `## QA` / `## 自由記述`, answer candidates pre-filled, `**回答**:` left blank); rename `## 修正案`→`## 対応案` and drop the 問題点/詳細 section (背景/現状 cover it); move `status` / `branches` to `_index.yaml` (`issue-tool.py` gains `add-branch`); update `issue-create` / `issue-review` / `issue-resolve` / `issue-scan`, the `issue-scanner` / `issue-resolver` agents, and `work:start` issue-linking accordingly |
| 2 | 2.61.0 | 2026-06-02 | Add `${WORK_BASE_BRANCH}` env var — specify base branch for new worktrees; `git worktree add` branches from this commit-ish when set |
| 2 | 2.60.0 | 2026-06-01 | Issue review/resolve workflow: add ISSUE frontmatter (`decision` / `status` / `branches` / free-form `instruction`) and move QA onto the issue; add `work:issue-review` (mobile-first triage via AskUserQuestion) + `work:issue-resolve` (loop-driven, one issue/tick: accept→`issue-resolver` subagent whose model is chosen by issue difficulty — sonnet/opus, never haiku; reject→shared `chore/rejected-issues`) + `work:issue-resolver` agent; `work:start` links issues (sets `status: in_progress`, appends `branches`, fills `## 関連イシュー`); `issue-tool.py` gains `set-status` and `close --linked-branch` is now an optional branch name; document the work lifecycle in CLAUDE.md |
| 1 | 2.62.0 | 2026-06-02 | Revive `work:conversation-to-claude` (formerly claude-kit, removed in PR181) — analyzes the session and auto-generates artifacts (skill / rule / hook / CLAUDE.md / incidents / glossary), delegating skill/rule/hook/CLAUDE.md to claude-kit creator skills; tighten the glossary/incidents inclusion bars (skip what is already in CLAUDE.md / a rule / the folder structure, and code bug fixes are not incidents). Add the `PreCompact` hook (`pre-compact.py`, toggle `${WORK_PRECOMPACT_CONV2CLAUDE}`) to run it before `/compact`, and restore the `work:merge` step that runs it inside the worktree (toggle `WORK_MERGE_CONV2CLAUDE`). Add `references/conversation/用語集.md` + `インシデント.md` (glossary/incidents authoring guides) auto-injected via ref-inject when editing `.claude/rules/glossary.md` / `.claude/rules/incidents.md` / `.claude/references/incidents/**` |
| 2 | 2.59.0 | 2026-06-01 | Remove `work:setup-wizard` skill and `SessionStart` hook (`setup_check.py`) |
| 2 | 2.56.0 | 2026-05-31 | Redesign `issue-scan` as an orchestrator delegating to parallel `work:issue-scanner` subagents (new agent); scan by perspective (folder/grep/layer/file-group); add `${ISSUE_SCAN_AGENTS}`; remove `issue-save` skill — issue file format now in the `work-dir/イシュー` reference, authored by `issue-create` and `issue-scanner` |
| 2 | 2.55.0 | 2026-05-31 | Remove `plugins/work/templates/` and `setup-task.py`; move templates/structure defs into `references/work-dir/` (`タスクドキュメント` / `タスクインデックス` / `イシュー` / `ワークディレクトリ構成`), injected by ref-inject on the matching `.work/` path. `work:start` authors the branch doc from the injected template; branch doc filename gains `.branch.md`. Rename `ドットワークディレクトリ構成`→`ワークディレクトリ構成`; remove `TODOテンプレート同期` |
| 3 | 2.54.0 | 2026-05-31 | index.yaml branch index keyed by `branch` (drop id/last_id/tags); add `created` surrogate; legacy backlog migrated to `index.archive.yaml`; `next-id` removed and `set-completed` switched to `--branch` |
| 4 | 2.53.1 | 2026-05-31 | Split `references/` into category subfolders: `notes/`, `work-dir/`, `skill-sync/` |
| 2 | 2.53.0 | 2026-05-31 | Redefine notes as a current spec sheet (snapshot; no history in the body, `## 変更履歴` table only, no frontmatter); add `ノート記述内容ルール` reference; merge `.work/specs` into notes and remove the folder |
| 2 | 2.52.0 | 2026-05-31 | Branch doc filename uses Japanese title (`{YYMMDD}-{日本語タイトル}.md`); add `branch` field to `index.yaml` |
| 2 | 2.51.0 | 2026-05-31 | Add `${WORK_COMMIT_LANG}` / `${WORK_COMMIT_TYPE}` env vars — configurable commit message language and type prefix |
| 2 | 2.50.0 | 2026-05-31 | Add `${WORK_BRANCH_AUTHOR}` env var — insert author name into branch names |
| 2 | 2.48.0 | 2026-05-30 | Remove `work:notes-to-claude` skill — inter-plugin dependency eliminated |
| 3 | 2.47.0 | 2026-05-30 | Add `${CLAUDE_KIT_INJECTION_DISABLE}` / `${DEV_KIT_INJECTION_DISABLE}` to `work:plugin-config` managed toggles |
| 4 | 2.46.2 | 2026-05-30 | Fix `issue-scan` skill: remove stale `py-kit`/`next-kit` references, update to `_injection_rules.yaml` |
| 5 | 2.46.0 | 2026-05-30 | Extract Stop hook inline python to `hooks/scripts/stop.py` + `_common.py` |
| 6 | 2.44.0 | 2026-05-30 | Unify branch document to single file (`{branch-hyphenated}.md`); rename `plugin-migrate` skill |
| 7 | 2.43.0 | 2026-05-30 | Add `${WORKSPACE_MERGE_PROPOSAL}` env toggle |
| 8 | 2.42.0 | 2026-05-30 | Add `WORKSPACE_PROTECTED_BRANCHES` env toggle |
| 9 | 2.41.0 | 2026-05-30 | Change `impl-review` Step 4 to batch AskUserQuestion (max 4 per call) |
| 10 | 2.40.0 | 2026-05-30 | Integrate `guard-kit` into work plugin |
| 11 | 2.39.0 | 2026-05-30 | Add `work:plugin-config` skill for interactive env toggle configuration |
| 1 | 2.57.0 | 2026-05-31 | Task folder names are now Japanese (`{YYMMDD}_{日本語タイトル}`); existing 217 folders renamed in bulk, `index.archive.yaml` `task:` fields followed (8→6 digit normalized), and `work:start` / `work-dir` references updated to the Japanese-name convention |
| 2 | 2.56.0 | 2026-05-31 | Redesign `issue-scan` as an orchestrator delegating to parallel `work:issue-scanner` subagents (new agent); scan by perspective (folder/grep/layer/file-group); add `${ISSUE_SCAN_AGENTS}`; remove `issue-save` skill — issue file format now in the `work-dir/イシュー` reference, authored by `issue-create` and `issue-scanner` |
| 3 | 2.55.0 | 2026-05-31 | Remove `plugins/work/templates/` and `setup-task.py`; move templates/structure defs into `references/work-dir/` (`タスクドキュメント` / `タスクインデックス` / `イシュー` / `ワークディレクトリ構成`), injected by ref-inject on the matching `.work/` path. `work:start` authors the branch doc from the injected template; branch doc filename gains `.branch.md`. Rename `ドットワークディレクトリ構成`→`ワークディレクトリ構成`; remove `TODOテンプレート同期` |
| 4 | 2.54.0 | 2026-05-31 | index.yaml branch index keyed by `branch` (drop id/last_id/tags); add `created` surrogate; legacy backlog migrated to `index.archive.yaml`; `next-id` removed and `set-completed` switched to `--branch` |
| 5 | 2.53.1 | 2026-05-31 | Split `references/` into category subfolders: `notes/`, `work-dir/`, `skill-sync/` |
| 3 | 2.53.0 | 2026-05-31 | Redefine notes as a current spec sheet (snapshot; no history in the body, `## 変更履歴` table only, no frontmatter); add `ノート記述内容ルール` reference; merge `.work/specs` into notes and remove the folder |
| 3 | 2.52.0 | 2026-05-31 | Branch doc filename uses Japanese title (`{YYMMDD}-{日本語タイトル}.md`); add `branch` field to `index.yaml` |
| 3 | 2.51.0 | 2026-05-31 | Add `${WORK_COMMIT_LANG}` / `${WORK_COMMIT_TYPE}` env vars — configurable commit message language and type prefix |
| 3 | 2.50.0 | 2026-05-31 | Add `${WORK_BRANCH_AUTHOR}` env var — insert author name into branch names |
| 3 | 2.48.0 | 2026-05-30 | Remove `work:notes-to-claude` skill — inter-plugin dependency eliminated |
| 4 | 2.47.0 | 2026-05-30 | Add `${CLAUDE_KIT_INJECTION_DISABLE}` / `${DEV_KIT_INJECTION_DISABLE}` to `work:plugin-config` managed toggles |
| 5 | 2.46.2 | 2026-05-30 | Fix `issue-scan` skill: remove stale `py-kit`/`next-kit` references, update to `_injection_rules.yaml` |
| 6 | 2.46.0 | 2026-05-30 | Extract Stop hook inline python to `hooks/scripts/stop.py` + `_common.py` |
| 7 | 2.44.0 | 2026-05-30 | Unify branch document to single file (`{branch-hyphenated}.md`); rename `plugin-migrate` skill |
| 8 | 2.43.0 | 2026-05-30 | Add `${WORKSPACE_MERGE_PROPOSAL}` env toggle |
| 9 | 2.42.0 | 2026-05-30 | Add `WORKSPACE_PROTECTED_BRANCHES` env toggle |
| 10 | 2.41.0 | 2026-05-30 | Change `impl-review` Step 4 to batch AskUserQuestion (max 4 per call) |
| 11 | 2.40.0 | 2026-05-30 | Integrate `guard-kit` into work plugin |
| 12 | 2.39.0 | 2026-05-30 | Add `work:plugin-config` skill for interactive env toggle configuration |