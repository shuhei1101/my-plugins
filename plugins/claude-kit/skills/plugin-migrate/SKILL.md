---
name: plugin-migrate
description: |
  Walk the project's claude-kit-authored artifacts (`.claude/skills/**` / `.claude/rules/**` /
  `.claude/hooks/**` / `**/CLAUDE.md` / `**/.claude-plugin/{plugin,marketplace}.json`) and
  bring them in line with the currently installed claude-kit reference conventions, applying
  minimal in-place edits where they deviate. Also re-applies the statusline if claude-kit's
  version is currently set in `~/.claude/settings.json`.
  Manual invocation only — use /claude-kit:plugin-migrate.
---

# claude-kit:plugin-migrate — Sync to claude-kit Conventions

Where `dev-kit` / `work` plugin-migrate is **static template re-copy**, claude-kit does not
ship templates into projects: each creator skill is a thin wrapper that defers to authoring
guides in `references/*.md`. So claude-kit's plugin-migrate is a **semantic migration**:
walk each existing artifact, compare it against the current reference, and apply the deltas.

The mechanic that makes this cheap: opening any target file with `Read` triggers the
`claude-kit-references-injection` hook, which inlines the matching reference in full.
The skill does not restate conventions — it **treats the injected reference as the
source of truth** and corrects the file against it.

Other plugins' artifacts are out of scope. Branch management (commit / merge) is the user's
responsibility.

---

## Sync targets (project artifact → claude-kit reference auto-injected on Read)

| Project pattern | Reference |
|---|---|
| `**/skills/*/SKILL{.jp,}.md` | `references/skill/skills.md` + `common/common.md` |
| `**/.claude/rules/**/*.md`, `**/.claude/rules-jp/**/*.md` | `references/claude-md/rules.md` + `common/common.md` |
| `**/CLAUDE{.local,.jp,}.md` | `references/claude-md/claude-md.md` + `common/common.md` |
| `plugins/*/CLAUDE{.jp,}.md` | `references/plugin/plugin-claude-md.md` + `references/plugin/version-sync.md` (additional) |
| `**/hooks/hooks.json` | `references/hook/hooks.md` + `common/common.md` + `common/environment.md` |
| `**/.claude/settings{.local,}.json` | `references/hook/hooks.md` + `common/common.md` + `common/environment.md` |
| `**/hooks/prompts/*.md` | `references/hook/hooks.md` |
| `**/.claude-plugin/{plugin,marketplace}.json` | `references/plugin/plugin-structure.md` + `common/common.md` + `plugin/version-sync.md` |
| `~/.claude/settings.json` `statusLine` block | `scripts/apply-statusline.py` definition |

`agents/` has no dedicated claude-kit reference yet (only `common.md`'s file-type +
JP/EN mirror rules apply). A future `agents.md` reference will be added.

---

## Tasks

### Step 1: Check the current branch

#### Condition

- Always — run first

#### Process

1. Run `git rev-parse --abbrev-ref HEAD`
2. If `master` / `main` → tell the user "Cannot run on master / main. Create a working branch first and re-run." and stop
3. Otherwise → proceed

→ Proceed to Step 2

#### Output

- The branch where the following edits will land is confirmed to be neither `master` nor `main`

#### Notes

##### Prohibitions

- Running on `master` / `main`

---

### Step 2: Walk each category and fix deviations

#### Condition

- Step 1 complete

#### Process

Walk the following categories in this order. For each, "enumerate → Read one file at a time → apply deltas":

1. **Skills** — `find . -type f -path '*/skills/*/SKILL.md' -not -path '*/node_modules/*' -not -path '*/.git/*'`
2. **Rules** — `find .claude/rules .claude/rules-jp -type f -name '*.md' 2>/dev/null` (skip if dirs absent)
3. **CLAUDE.md** — `find . -type f \( -name 'CLAUDE.md' -o -name 'CLAUDE.jp.md' -o -name 'CLAUDE.local.md' \) -not -path '*/node_modules/*' -not -path '*/.git/*'`
4. **Hooks (manifest)** — `find . -type f -name 'hooks.json' -not -path '*/node_modules/*' -not -path '*/.git/*'` plus `.claude/settings.json` / `.claude/settings.local.json`
5. **Hook prompts** — `find . -type f -path '*/hooks/prompts/*.md' -not -path '*/node_modules/*' -not -path '*/.git/*'`
6. **Plugin manifests** — `find . -type f \( -name 'plugin.json' -o -name 'marketplace.json' \) -path '*/.claude-plugin/*' -not -path '*/node_modules/*' -not -path '*/.git/*'` (marketplace repos only)

For each file:

a. Open with `Read` — the injection hook supplies the matching references
b. Treat the injected reference body as the **authoritative convention**
c. Enumerate deviations (missing required sections, outdated patterns, convention violations)
d. Use `Edit` to apply **minimal deltas** — preserve existing user content; never rewrite wholesale
e. JP mirrors (`*.jp.md` / `CLAUDE.jp.md` / `rules-jp/`) are updated in parallel after the English file is fixed
f. If the file is already compliant, skip it

→ Proceed to Step 3

#### Notes

##### Branching

- If a file is so far gone that "regenerate" is more sensible than "delta-fix", ask the user before regenerating (default is delta-only)

##### Prohibitions

- Wholesale file replacement (it stops being a migration and becomes a template drop)
- Modifying other plugins' artifacts (e.g. `plugins/work/skills/*/SKILL.md`) — those belong to each plugin's own `plugin-migrate`

---

### Step 3: Re-apply statusline if currently claude-kit's

#### Condition

- Step 2 complete

#### Process

1. Read `~/.claude/settings.json` (skip if absent)
2. Check whether `statusLine.command` contains claude-kit's signature (e.g. the `ctx ` literal or `ml=m.lower()` from `apply-statusline.py`)
3. If yes → run `python ${CLAUDE_PLUGIN_ROOT}/scripts/apply-statusline.py` to re-write with the current definition
4. If no → skip (user isn't on claude-kit's statusline)

→ Proceed to Step 4

---

### Step 4: Report the diff

#### Condition

- Step 3 complete

#### Process

1. Show `git status` and `git diff` (truncate if huge)
2. If no changes → report "All claude-kit-authored artifacts already comply with v{N}" and stop
3. Otherwise, list the edited files and a suggested commit message:
   - Example: `chore: sync claude-kit-authored artifacts to v{N}`
4. Read the current version `{N}` from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`
5. **This skill never commits on its own** — commit / merge is the user's responsibility

→ Done

#### Notes

##### Prohibitions

- Auto-committing (same policy as `dev-kit` / `work` plugin-migrate)
