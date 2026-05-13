---
paths:
  - "**/*"
---

# Cascade Sync

<when_to_apply>
When editing any file in the project.
</when_to_apply>

When you edit any file, update ALL related resources in the same commit.
Never leave referenced documents stale after a change.

## Step 1 — Find the governing rule

<steps>

Look through `.claude/rules/**/*.md` for a rule whose `paths:` pattern matches the edited file.
That rule's referenced doc list shows what to check.

</steps>

## Step 2 — Update docs

<policy>

If the edit changes documented behavior (schema, field names, process, valid values), update
every referenced doc. If behavior is unchanged, no edit needed.

</policy>

## Step 3 — Grep for changed identifiers

When adding, removing, or renaming a domain constant (config key, identifier, model name):

```
grep -r "<old_or_new_identifier>" src/ docs/
```

Update every reference found — source code, config files, docs.

## Step 4 — Update the rule itself

<steps>

If the rule's description or reference list is now inaccurate:
1. Update `.claude/rules/<rule>.md` (English original)
2. Update `.claude/rules-jp/<rule>.md` (Japanese mirror)
3. Commit both together.

</steps>

## Three-way sync loop

```
File change → governing rule loads → update referenced docs
Doc update  → verify rule's reference list is complete
Rule update → sync JP mirror → verify referenced docs
```
