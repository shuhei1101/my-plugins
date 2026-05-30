# `git merge master -X theirs` silently drops branch-only additions inside heavily-edited shared files

## Context

- PR: PR168 (`refactor-task-doc-structure`)
- Date: 2026-05-30

## What happened

PR168 was long-running, and master had been overhauled by 5 PRs (PR165 / PR166 / PR169 / PR170 / PR172) while it sat. After confirming with the user "master is canonical; layer PR168 on top," I ran:

```bash
git merge master -X theirs
```

to resolve dozens of structural conflicts (e.g. `plugins/work-kit/` → `plugins/workspace/` rename, `mark-generated` skill removal, `version-sync` removal) by preferring master in every conflict.

The strategy worked for **files master also touched** — master's version won, as intended. But PR168 had also **appended 4 new entries to `.claude/rules/core/glossary.md`** (a file master had likewise heavily edited for PR172). Even though those PR168 additions did not overlap master's edits, the resulting merged glossary lost them — they did not appear in the post-merge tree at all.

I noticed only because I grepped for the new term names after merge:

```bash
grep -n "PR168\|plugin-update\|変更内容セクション\|テストセクション\|単一ファイル化" .claude/rules/core/glossary.md
# (no output)
```

Re-appending the 4 entries manually was straightforward, but had I committed without checking, the glossary additions would have silently vanished.

## Lesson

`-X theirs` is not a precision tool when both sides have appended to the same file. Git's auto-merge can pick "theirs" entirely for files that look hunk-conflicted, dropping additions the branch had made elsewhere in the file. After a `-X theirs` merge into a long-lived branch:

- Identify every file your PR **appended** to (not just modified or moved): glossary tables, incidents tables, marketplace plugin list, index-style files.
- For each, run a `grep` for your PR's distinguishing identifiers (new term names, new file paths, the PR number) immediately after the merge.
- If anything is missing, re-append it before the merge commit.

A safer alternative when the branch's additions are isolated: drop the `-X theirs` and resolve each "both modified" conflict manually for append-style files, even if you accept `theirs` for everything else.

## Related

- `large-master-adapt-user-decisions.md` — master-overhaul-during-long-PR pattern; this is a follow-on lesson about which strategy to use once you've decided to "layer on top."
- `parallel-pr-version-bump-collision.md` — another long-PR pitfall when master is far ahead.
