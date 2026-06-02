# Incident 26: migration-reruns-resets-processed-state

Japanese mirror: `migration-reruns-resets-processed-state.jp.md`

## Summary

Re-running a batch-transformation script on already-processed files silently resets their state.
After a merge that introduces new files, apply the script only to those new files — or verify
idempotency first.

## What happened

During `work:merge` Step 3, `git merge master` brought in 6 new issue files (ISSUE-196〜201)
that had not yet been migrated to the v2.75.0 format. The migration script (`migrate_issues.py`)
was re-run on the entire `.work/issues/` directory (77 files) to catch those 6 new files.

Because the script searched for `**回答**: ` markers to detect the answer state, already-migrated
files (which had `- [x]` checkboxes instead) returned `isha_answer = None` — causing all
`## 意思` checkboxes to be written back as `- [ ] 対応する / - [ ] 対応しない` (fully unchecked).
Answered QA checkboxes were similarly reset.

The state reset was silent: the script reported "OK" for all 77 files, and the diff was not
inspected before committing. The error was caught only when spot-checking the output.

## Fix applied

```bash
git reset --hard HEAD~1   # revert the bad commit
python migrate_issues.py  # re-run selectively, only on the 6 new files
git add .work/issues/ISSUE-196.md … ISSUE-201.md
git commit
```

## Prevention

1. **Apply to new files only**: after a merge that adds new files, apply the transformation
   script only to the newly-added files, not the full directory.
2. **Verify idempotency before re-running**: if running on the whole directory is unavoidable,
   test the script on one already-processed file first and confirm the output is unchanged.
3. **Inspect the diff before committing**: `git diff --stat` after running the script should show
   only the expected new/changed files.
