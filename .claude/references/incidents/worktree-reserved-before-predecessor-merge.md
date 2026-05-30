# A worktree reserved before its predecessor PR merged has a stale "gold standard"

## What happened

PR158's job was to migrate `next-kit` onto the `ref-inject` injection form — the exact
same migration PR157 had just done for `py-kit`. The plan was to use the migrated `py-kit`
(and the `ref-inject` templates) as the gold standard to mirror.

But an early diff showed `py-kit`'s injection hook still on the **old** per-pattern
empty-file token design, contradicting the glossary which said PR157 had already switched
it to the `expires_at` TTL form. The `ref-inject` template also still said `injected_at`.

The cause: the PR158 worktree had been reserved by `pr-handoff` off master **before PR157
merged**. `git merge-base --is-ancestor 542a9c8 HEAD` returned false — PR157 was not in the
branch's history. The branch's in-tree `py-kit` and `ref-inject` files were the pre-PR157
versions, so they were the wrong template to copy.

## Root cause

`pr-handoff` reserves the next PR's worktree immediately, branching off whatever master is
at reservation time. When the reserved PR's purpose is to **mirror a predecessor PR's
change**, and that predecessor merges *after* the reservation, the predecessor's result is
absent from the branch. Treating the in-tree files as "current" then mirrors stale code.

## Fix

Merged master into the PR158 branch first (`git merge master`, clean), which pulled in
PR157's migrated `py-kit` and the `expires_at`-updated `ref-inject` template. Only then was
`py-kit` a valid gold standard, and the `next-kit` regeneration came out byte-identical to
`py-kit` except the plugin-name strings.

## Lesson

When a PR's purpose is to follow / mirror a predecessor PR, before using any in-tree file as
the reference template, verify the predecessor is actually in the branch history:

```bash
git merge-base --is-ancestor {predecessor-commit} HEAD && echo included || echo "merge master first"
```

If it is not included, `git merge master` into the branch first. A `pr-handoff`-reserved
branch is **not** guaranteed to contain its predecessor's work — reservation time and
predecessor merge time are independent.
