# Incident: Orphaned dispatch prompts — modernize, don't delete

## What happened

In PR153, `plugins/claude-kit/hooks/prompts/hook-creator-dispatch.{md,jp.md}` and
`plugin-creator-dispatch.{md,jp.md}` existed but were not wired into `hooks.json`
(orphaned). git history showed they were originally **UserPromptSubmit keyword-detection**
hooks, dropped when the project migrated creator-dispatch to **PreToolUse file-path**
blocking — only skill/rule/claude/j2 got PreToolUse versions.

AI's first recommendation (QA-001, 案A) was to **delete** the orphaned prompt files,
reasoning that `plugin-creator-dispatch` matching all of `plugins/**` was too broad.
The user corrected this: these were intended features left un-migrated, and the right
move was to **convert them to the current PreToolUse(Edit/Write) pattern**, not delete them.

## Why the deletion instinct was wrong

- An orphaned generated artifact from a **superseded hook style** usually represents an
  *intended-but-unmigrated feature*, not dead weight. The prompt content (route hook-config
  edits through hook-creator; route plugin edits through plugin-creator) was still desirable.
- The over-broadness concern was real but solvable by **rule ordering** (first-match-wins,
  with the broad `plugins/` catch-all placed last so specific rules take precedence), not by
  deletion.
- These hooks fire in *consumer* projects that install claude-kit; "matches everything" is a
  self-application artifact of this marketplace repo, not a flaw of the design.

## Lesson

When you find orphaned artifacts left behind by a style/architecture migration
(e.g. prompts from an old UserPromptSubmit→PreToolUse move), default to **migrating them to
the current pattern**, and confirm with the user before deleting. Deletion discards an
intended feature; migration completes the work the previous PR started.

## Correct approach

1. Check git history (`git log --oneline --all -- {file}`) to learn why the artifact exists.
2. If it maps to a current pattern, migrate it (here: add to the `creator_dispatch.py` `RULES`
   table, rewrite the prompt wording for the new event, sync the JP mirror).
3. Solve breadth/overlap concerns with ordering/scoping, not removal.
4. Only delete when the feature itself is genuinely unwanted — and confirm first.
