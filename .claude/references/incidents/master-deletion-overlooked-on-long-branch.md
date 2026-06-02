# Editing a file on a long-lived branch that was already deleted on master

**Date**: 2026-05-28
**PR**: PR135 (review-next-kit-plugin)

## Background

PR135 was a multi-day branch with many commits. In the final cleanup phase, AI added a new entry (`kit-hooks-index-sync.md`) to `.claude/rules/feature/_overview.md`.

When the user merged master in, the `_overview.md` file was found to have been **deleted on master** (by PR141 / `move-jp-mirror-agent-to-claude-kit` and related cleanup). The file existed on PR135's branch only because PR135 had not synced with master since branching.

This caused a "ghost file" situation: PR135 was actively editing a file that master no longer expected to exist. Resolution required a separate commit to delete `_overview.md` on the branch as well, just to restore parity with master before the actual merge.

## Root cause

On a long-lived branch, AI assumed the files it saw locally were the canonical set. It did not check whether any of them had been deleted on master since branching.

Specifically, when adding a new entry to a list-style file like `_overview.md` or `incidents.md`, AI's reflex is "open and append" — it doesn't first run `git log master -- {file}` to confirm the file is still a live concept upstream.

## Lesson

When editing a file on a long-lived branch (especially `.claude/rules/**`, `.claude/references/**`, overview / index files), **first verify the file still exists on master**:

```bash
git log master --oneline -- {file} | head -5
git show master:{file} 2>&1 | head -3   # error → deleted on master
```

If the file was deleted on master, the action should be one of:

1. **Don't touch it** — write the content elsewhere (e.g., directly under `.claude/rules/feature/{name}.md` without indexing in an overview file)
2. **Resurrect deliberately** — only if there's a clear reason to bring it back
3. **Match master's deletion** — `git rm` on the branch too, before the merge

## Recurrence prevention

- Add an explicit check before editing rule / overview / index files: `git log master..HEAD --oneline -- {file}` and `git log HEAD..master --oneline -- {file}`
- For `_overview.md`-style index files, prefer not to maintain them at all — let the folder listing be the index. The PR135 incident confirms `_overview.md` was being phased out.
- During merge prep (work-kit:merge Step 3), explicitly check master's deletions: `git diff --diff-filter=D --name-only HEAD..master | grep "{paths edited in this PR}"`.

## Related

- `extract-step-check-master-first.md` (similar lesson: check master before extracting a skill step)
- `unnecessary-jp-mirror-sync-rule-for-agents.md` (PR141 — the change that deleted `_overview.md` cluster)
- PR135 commit `5c8ad7d` (the cleanup commit that restored parity)
