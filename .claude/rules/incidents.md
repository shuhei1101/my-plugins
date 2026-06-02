# Incidents

Recurrence-prevention log of concrete **process mistakes** (operation/judgment errors, not code bugs)
that actually happened, so they do not recur. The full story of each lives in
`.claude/references/incidents/{slug}.md` (+ `.jp.md`).

Japanese mirror: `.claude/rules/incidents.jp.md`

> Authoring bar and format: `plugins/work/references/conversation/インシデント.md`.

---

| No | Category | Incident (slug) | Summary |
|---|---|---|---|
| 1 | Reference / hook-injection authoring | bestprac-over-usecase-references-bloat | Design references from the `injection_rules.yaml` trigger map, not a content TOC — 1 file = 1 use case, no comparison/selection/trade-off sections. |
| 2 | 〃 | orphan-references-not-checked | After editing `injection_rules.yaml`, run a YAML-vs-filesystem orphan check so no reference file is left unbound to a pattern. |
| 3 | 〃 | glob-pattern-missing-recursive-prefix | Prefix by-name folder globs with `**/` (e.g. `**/tools/**/*.py`); root-anchored patterns are only for files that must sit at the project root. |
| 4 | 〃 | yaml-unquoted-colon-space-breaks-parse | Never put `word: ` (colon-space) inside an unquoted YAML scalar — it parses as a nested map and breaks `safe_load`; quote the value and validate. |
| 5 | 〃 | markdown-for-code-consumed-config | Code-consumed config stays in a structured format (YAML/JSON); generate a Markdown view if humans need one — don't convert the source to a table. |
| 6 | 〃 | injection-only-fires-on-write-edit-path | Before converting an AI-called skill into an injected-only reference, confirm every caller's target is on the Write/Edit/Read path; script-generated and non-matched files still need the skill. |
| 7 | 〃 | ref-inject-overbuilt-script-and-hook | Prefer Claude-driven copy+substitute over a generator script, and don't add a hook for behavior an existing TTL/mechanism already covers — default to the leanest mechanism. |
| 8 | Skill / plugin design | skill-reading-token-cost | Don't design skills to load other skills at runtime (≈2,500×N tokens per call); embed the needed decision knowledge in the skill's own references. |
| 9 | 〃 | premature-cross-plugin-centralization | Don't centralize across plugins until 3+ consumers (or repeated drift) exist; copy-paste between 2 plugins is cheaper than a placeholder/path-resolution layer. |
| 10 | 〃 | skill-cli-args-format | Claude Code skills don't take CLI flags — express expected inputs as natural-language bullets, not a `--flag` table. |
| 11 | 〃 | skill-name-log-implies-error-log | Name data-persisting skills/functions `save`/`write`/`record`; reserve `log` for genuine logging-stream output. |
| 12 | Naming / docs | work-folder-name-implies-official-docs | Give folders not auto-loaded by AI an informal name (e.g. `notes/`) — an official-sounding name (`specs/`) invites it to be treated as authoritative and go stale. |
| 13 | Git / branch / merge workflow | stale-session-git-snapshot-already-merged-followup | Before starting follow-up or cross-branch work, check the actual current master (`git log master`, `git worktree list`) — the session-start git snapshot is stale and a candidate may already be merged. |
| 14 | 〃 | large-master-adapt-user-decisions | When adapting to an advanced master would force a new identifier name, a scope-of-branch call, or an abort/proceed call, pause and ask the user 2–4 questions — the merge tiebreaker only covers commit-order facts. |
| 15 | 〃 | master-deletion-overlooked-on-long-branch | On long-lived branches, verify `git show master:{file}` exists before editing rule/index/overview files — master may have already deleted it. |
| 16 | 〃 | parallel-pr-version-bump-collision | When `git diff HEAD..master` shows a version bump on the same plugin, rebump to the next version on the branch before merging. |
| 17 | 〃 | worktree-reserved-before-predecessor-merge | When a branch mirrors a predecessor, verify the predecessor is in the branch history (`git merge-base --is-ancestor`) before treating in-tree files as the template; `git merge master` first if not. |
| 18 | 〃 | merge-theirs-loses-branch-only-additions | `git merge -X theirs` / `checkout --theirs` silently drops branch-only additions; reconcile additions manually instead of blanket-taking one side. |
| 19 | Process / QA | design-qa-implementation-creep | In a policy/design-only branch, QA stops at what/why/where — never implementation detail (how). |
| 20 | Hooks / scripting / environment | git-guard-false-positive-file-content | A command guard can false-positive when the matched string appears as file content or a substring, not the actual command verb; match the command, not a substring. |
| 21 | 〃 | python3-c-backtick-shell-expansion | Backticks inside `python3 -c "..."` are command-substituted by the shell before Python sees them; avoid backticks or feed the code via a single-quoted heredoc/file. |
| 22 | 〃 | path-home-cross-env-mismatch | Scripts using `Path.home()` must run in the same Python environment as Claude Code — running WSL Python while Claude Code runs native Windows (or vice versa) silently edits a different home, applying nothing. |
| 23 | 〃 | template-under-gitignore | Before placing a file under a directory with a `.gitignore`, run `git check-ignore -v` to confirm it is trackable; otherwise have the setup script write it at runtime. |
| 24 | 〃 | claude-plugin-root-unset-manual-steps | `${CLAUDE_PLUGIN_ROOT}` is not set when skill steps are executed manually via the Bash tool (e.g. a skill with `disable-model-invocation: true`); resolve the script path with `find` before running work-plugin script commands. |
| 25 | 〃 | pretooluse-read-block-cancels-tool | Returning `{"decision": "block"}` from a `PreToolUse(Read)` hook cancels the Read; the file content is never delivered to Claude. For Read, use `hookSpecificOutput.permissionDecision: "allow"` + `additionalContext` to inject context while letting the Read proceed. |
