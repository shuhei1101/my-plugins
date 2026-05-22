# creator-skill-inline-duplication — Creator Skill Inline Knowledge Duplication

## What happened

Each of `rule-creator`, `skill-creator`, `hook-creator`, and `claude-creator` had the file-type
usage guide (when to use rules, when to use skills, etc.) written inline as "key points" in Step 0.

At the same time, an external reference file `references/file-types.md` also existed,
resulting in the same content duplicated across 5+ locations.

## Root cause

PR68 adopted the policy "embed judgment knowledge inline in the skill" for token efficiency.
However, the Step 0 design that reads an external file was also kept,
causing both the inline version and the external version to co-exist with the same content.

## Fix (PR71)

1. Deleted `references/file-types.md` and split it into 5 purpose-specific files:
   - `references/common.md` — shared (decision criteria, JP/EN mirror rules)
   - `references/rules.md` — rules-specific (two types, use-case-oriented, folder structure)
   - `references/skills.md` — skills-specific
   - `references/hooks.md` — hooks-specific (includes loop prevention)
   - `references/claude-md.md` — CLAUDE.md-specific (thinning principles)

2. Removed inline "key points" from each creator skill's Step 0;
   replaced with a single line pointing to the relevant `references/` file(s)

3. Created the `claude-refactor` skill that reads all `references/` files and performs cross-type auditing

## Prevention

Shared judgment criteria and guidelines should be written in `references/` from the start.
Skills should only declare which files to read — the content lives in `references/`.

- ✅ Updating one file propagates to all skills
- ✅ Each skill reads only the files it needs (token efficient)
- ❌ Inline knowledge requires updating every skill individually when anything changes
