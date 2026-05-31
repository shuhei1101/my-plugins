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
| `**/skills/*/SKILL{.jp,}.md` | `references/skill/スキル.md` + `common/共通ガイド.md` |
| `**/.claude/rules/**/*.md`, `**/.claude/rules-jp/**/*.md` | `references/claude-md/記述ルール.md` + `common/共通ガイド.md` |
| `**/CLAUDE{.local,.jp,}.md` | `references/claude-md/CLAUDE-md記述ガイド.md` + `common/共通ガイド.md` |
| `plugins/*/CLAUDE{.jp,}.md` | `references/plugin/プラグインCLAUDE-md.md` + `references/plugin/バージョン同期.md` (additional) |
| `**/hooks/hooks.json` | `references/hook/フック.md` + `common/共通ガイド.md` + `common/環境変数.md` |
| `**/.claude/settings{.local,}.json` | `references/hook/フック.md` + `common/共通ガイド.md` + `common/環境変数.md` |
| `**/hooks/prompts/*.md` | `references/hook/フック.md` |
| `**/.claude-plugin/{plugin,marketplace}.json` | `references/plugin/プラグイン構造.md` + `common/共通ガイド.md` + `plugin/バージョン同期.md` |
| `~/.claude/settings.json` `statusLine` block | `scripts/apply-statusline.py` definition |

`agents/` has no dedicated claude-kit reference yet (only `common.md`'s file-type +
JP/EN mirror rules apply). A future `agents.md` reference will be added.

---

## Tasks

### Step 1: Walk each category and fix deviations

#### Condition

- Always — run first

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

→ Proceed to Step 2

#### Notes

##### Branching

- If a file is so far gone that "regenerate" is more sensible than "delta-fix", ask the user before regenerating (default is delta-only)

##### Prohibitions

- Wholesale file replacement (it stops being a migration and becomes a template drop)
- Modifying other plugins' artifacts (e.g. `plugins/work/skills/*/SKILL.md`) — those belong to each plugin's own `plugin-migrate`

---

### Step 2: Re-apply statusline if currently claude-kit's

#### Condition

- Step 1 complete

#### Process

1. Read `~/.claude/settings.json` (skip if absent)
2. Check whether `statusLine.command` contains claude-kit's signature (e.g. the `ctx ` literal or `ml=m.lower()` from `apply-statusline.py`)
3. If yes → run `python ${CLAUDE_PLUGIN_ROOT}/scripts/apply-statusline.py` to re-write with the current definition
4. If no → skip (user isn't on claude-kit's statusline)

→ Proceed to Step 3

---

### Step 3: Report the diff

#### Condition

- Step 2 complete

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
