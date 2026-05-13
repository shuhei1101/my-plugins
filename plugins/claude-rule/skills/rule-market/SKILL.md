---
name: rule-market
description: Rule library for Claude Code projects. Use when the user wants to install rules, says "rule-market", "ルールマーケット", "ルールをインストール", "add rules to this project", or when rules-creator is about to create a new rule (always check here first). Lists available rules, installs them into the project, and syncs modified rules back to the library.
---

# rule-market — Rule Library for Claude Code Projects

Installs battle-tested, project-agnostic path-scoped rules from this plugin's library into
the current project. Always check here before creating a new rule from scratch.

---

## Available Rules

<rule_library>

| Rule name | Paths | Description |
|---|---|---|
| `cascade-sync` | `**/*` | Keep rules, docs, and JP mirrors in sync on every edit |
| `auto-register` | `**/*` | Ensure every edited file is covered by a path-scoped rule |

> `rule-market-managed` is always installed alongside any selected rule (management rule).

</rule_library>

---

## Operations

### `list` — Show the rule library

Display the Available Rules table above. No files are created.

### `install <rule-name>` or `install-all` — Deploy to current project

<steps>

1. **Identify the target project.** Use the current working directory (`$PWD`) as the project
   root. If the session is in a worktree or sub-directory, confirm with the user.
2. **Check for conflicts.** If a file with the same name already exists in
   `PROJECT/.claude/rules/`, show the diff and ask before overwriting.
3. **Write the rule template** to `PROJECT/.claude/rules/<rule-name>.md` using the inline
   template content below.
4. **Write the JP mirror template** to `PROJECT/.claude/rules-jp/<rule-name>.md`.
5. **Install `rule-market-managed.md`** to `PROJECT/.claude/rules/rule-market-managed.md`
   and its JP mirror, if not already present. This management rule is always co-installed.
6. **Update `CLAUDE.md`** if the project has a `Folder-scoped rules` table — add a row for
   each installed rule.
7. Report created files.

</steps>

### `sync <rule-name>` — Push project edits back to plugin library

<steps>

Use when a project's installed rule has been customized and you want to propagate the change
back to the plugin's template so future installs get the improved version.

1. Locate the sync script:
   ```
   Get-ChildItem ~/.claude -Recurse -Filter "sync_rules.py" | Where-Object { $_.FullName -like "*claude-rule*" }
   ```
2. Run it:
   ```
   python <script-path> sync <project-root> <rule-name>
   ```
   The script copies `PROJECT/.claude/rules/<rule-name>.md` →
   `<plugin>/skills/rule-market/rules/<rule-name>.md`.
3. Remind the user to also update the JP mirror in `rules-jp/` and bump the plugin version.

</steps>

---

## Rule Templates (inline)

The following templates are the source of truth for each rule. They are also stored as files
in `skills/rule-market/rules/` (human-readable source) and `rules-jp/` (JP mirrors).

---

### `cascade-sync.md`

```markdown
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
```

---

### `auto-register.md`

```markdown
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
```

---

### `rule-market-managed.md`

```markdown
---
paths:
  - ".claude/rules/**/*.md"
---

# Rule Market Managed Rules

<when_to_apply>
When editing any file under .claude/rules/.
</when_to_apply>

<policy>

Some rules in this project were installed from the `claude-rule` plugin's rule-market library.
If you modify one of those rules and want to contribute the improvement back to the library,
use the sync operation:

```
/claude-rule:rule-market sync <rule-name>
```

Or run the sync script directly (locate it first):
```powershell
Get-ChildItem ~/.claude -Recurse -Filter "sync_rules.py" |
  Where-Object { $_.FullName -like "*claude-rule*" }
python <script-path> sync <project-root> <rule-name>
```

After syncing, update the JP mirror in `rules-jp/` and bump the plugin version.

</policy>

## Market-installed rules in this project

<!-- List the rules installed from rule-market here, one per line: -->
<!-- - cascade-sync -->
<!-- - auto-register -->
```

---
