---
paths:
  - "**/*"
---

# Auto Rule Registration

<when_to_apply>
When editing any file in the project.
</when_to_apply>

When editing any file, verify it is covered by an existing path-scoped rule. If not, create one.

## How to check coverage

<steps>

Scan `.claude/rules/**/*.md` for `paths:` patterns.
Test whether the edited file's repo-relative path matches any pattern using glob semantics.

A file is covered if a broad pattern applies (e.g. `src/**/*.py` covers all Python source).
No separate rule is needed in that case.

</steps>

## When to create a new rule

<policy>

Create a rule when:
- The file belongs to a domain with no existing coverage
- The domain has specific constraints, referenced docs, or cascade dependencies worth recording

No rule needed for:
- Auto-generated files that should never be manually edited
- Files already covered by a broad existing pattern
- One-off scripts with no docs and no domain constraints

</policy>

## How to create the rule

<steps>

1. Create `.claude/rules/<domain>.md` with `paths:` frontmatter and at minimum:
   - Domain description and activation condition
   - Referenced doc list
   - Any cascade-sync notes
2. Create `.claude/rules-jp/<domain>.md` — Japanese mirror with identical structure.
3. Add a row to `CLAUDE.md` under the Folder-scoped rules table.
4. Commit all three changes together (EN rule + JP mirror + CLAUDE.md row).

Use the `/rules-creator` skill to scaffold files automatically.

</steps>
