# Incident: Parallel PR Version Bump Collision

## What happened

PR152 and PR153 were developed in parallel. Both bumped claude-kit independently:
- PR153 bumped `3.27.1 → 3.28.0` (modernize creator-dispatch hooks)
- PR152 bumped `3.27.1 → 3.28.0` (add PreCompact hook)

PR153 merged first (it was already done). When PR152 ran the master compatibility check (`git log HEAD..master --oneline`), it found PR153's commits on master. The `plugins/claude-kit/.claude-plugin/plugin.json` diff showed the same `3.28.0` on both sides — version collision.

## Fix applied

During Step 3 of the merge skill (master compatibility check):
1. Detected that master's claude-kit was already at `3.28.0`
2. PR152 branch also had `3.28.0` from its own bump
3. Bumped PR152 to `3.29.0` before executing the final merge

## How to detect

```bash
git diff HEAD..master -- plugins/claude-kit/.claude-plugin/plugin.json
```

If both sides changed `version` to the same value, a version collision exists.

## Prevention

When `git diff HEAD..master` shows a version bump on the same plugin:
1. Check what version master is now at
2. Bump the PR branch to `master_version + 0.1.0` (next minor)
3. Update both `plugin.json` and `marketplace.json`
4. Commit before merging
