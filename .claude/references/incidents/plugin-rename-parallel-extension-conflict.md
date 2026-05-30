# Plugin Rename with Parallel Extension Conflict

**Date**: 2026-05-30
**Category**: tool-misuse

## What Happened

In PR172 (renaming `plugins/work-kit/` → `plugins/workspace/`), master had received PR167 which added new skill files (`plugins/work-kit/skills/config/SKILL.md` and `SKILL.jp.md`) while the rename PR was in progress.

When running `git merge master` in the PR172 worktree, git flagged:

```
CONFLICT (file location): plugins/work-kit/skills/config/SKILL.md added in master
inside a directory that was renamed in HEAD, suggesting it should perhaps be moved to
plugins/workspace/skills/config/SKILL.md.
```

This happened because:
- PR172 renamed `plugins/work-kit/` → `plugins/workspace/` via `git mv`
- master independently added new files under `plugins/work-kit/skills/config/`
- Git cannot automatically resolve where the new files should go after the rename

## How to Avoid

When merging master into a plugin-rename PR:

1. Look for `CONFLICT (file location)` messages referencing the old plugin path
2. For each conflicted file, manually move it:
   ```bash
   mkdir -p plugins/{new-name}/skills/{skill-name}/
   mv plugins/{old-name}/skills/{skill-name}/SKILL.md plugins/{new-name}/skills/{skill-name}/SKILL.md
   mv plugins/{old-name}/skills/{skill-name}/SKILL.jp.md plugins/{new-name}/skills/{skill-name}/SKILL.jp.md
   ```
3. Update any internal references (`old-name:` → `new-name:`) in the moved files
4. Stage the removal and addition:
   ```bash
   git rm plugins/{old-name}/skills/{skill-name}/SKILL.md
   git rm plugins/{old-name}/skills/{skill-name}/SKILL.jp.md
   git add plugins/{new-name}/skills/{skill-name}/
   ```
5. Also update any glossary entries referencing the new skill name

## Context

Applies to any PR that renames a plugin folder (`git mv plugins/old plugins/new`) when another PR has simultaneously added files under the old path. The broader lesson: coordinate plugin renames with any concurrent PRs that modify the same plugin, or expect location conflicts during merge.
