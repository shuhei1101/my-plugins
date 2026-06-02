# `.work/specs/` Folder Name Implies Official Documents and Causes Staleness

## What happened

The `.work/specs/` folder in work-kit was designed to hold temporary design memos and investigation notes per PR.
However, the name `specs` (= specifications) carries a "formal specification document" connotation, causing:

- Files appearing important because they look like official specs, even though they are not auto-loaded by Claude
- Files going stale because they are actually temporary memos that don't get updated
- Users feeling pressure to "write a spec", not doing it, leaving the folder empty, and the feature going unused

## Fix

Renamed `.work/specs/` → `.work/notes/` and updated all references (PR88).

The name `notes` communicates:
- This is a temporary memo area, not official documentation
- Stale files are "old notes" not "outdated specs" — lower psychological cost
- Lower barrier to use → more likely to actually be used

## Lesson

**Files in folders that are not auto-loaded by Claude will go stale if abandoned.**
Name such folders with informal-sounding names (`notes/`, `scratch/`, `drafts/`) that don't imply maintenance obligations.
Avoid names like `specs/`, `docs/`, `references/` — they imply a duty to keep files current.
