# Plugin Authoring Guide

How to create or update a Claude Code plugin. This guide is self-contained: when injected (because
you are editing a `plugin.json` or `marketplace.json`), follow it to author the change directly.
Read `common.md` alongside it.
Japanese mirror: `references/plugin-structure.jp.md`

---

## Standard directory layout

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (required)
├── CLAUDE.md                # Plugin developer guide (required)
├── CLAUDE.jp.md             # Japanese mirror (required)
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md         # Skill definition (English, auto-loaded)
│       └── SKILL.jp.md      # Japanese mirror (reference only)
├── agents/
│   └── <agent-name>.md      # Agent definitions (optional)
├── hooks/
│   └── hooks.json           # Hook configuration (optional)
├── references/              # Shared reference docs (optional)
│   └── <topic>.md
└── .mcp.json                # MCP server config (optional)
```

---

## Zero inter-plugin dependency principle

**Design every plugin as an independent distribution unit. Keep dependencies on other plugins' skills, commands, and script paths as close to zero as possible.**

### Why

A plugin is installed, updated, and removed individually. References to other plugins cause:

- Install-order dependency (the dependee plugin must be installed first)
- Cascading edits on rename (renaming a dependee plugin forces every reference to be updated)
- Parallel-PR conflicts (PRs that cut across multiple plugins are harder to merge as their footprint grows)
- Loss of reusability of the plugin on its own

### Acceptable exceptions

| Pattern | Reason |
|---|---|
| Calls between skills inside the same plugin | Same distribution unit — independence is not compromised |
| Static template expansion via `ref-inject:apply` | Designed as something "shipped to" another plugin; after expansion the result lives entirely inside the destination plugin |
| `claude-kit`'s references injection mechanism (other plugins opt in) | The consumer plugin opts in voluntarily — not a forced dependency |

### Prohibited dependencies

- A skill A's steps invoke `/other-plugin:skill-B`
- A hook directly references a script file path inside another plugin (e.g. `${CLAUDE_PLUGIN_ROOT}/../other-plugin/...`)
- A reference instructs the user to "run another plugin's command and come back"

### How to detect violations

Apply the following checks when designing both new and existing plugins:

```bash
# Find calls to other plugins' skills
grep -rn "/[a-z-]\+:[a-z-]\+" plugins/<name>/skills/ plugins/<name>/references/

# Check whether hook config references paths outside this plugin's CLAUDE_PLUGIN_ROOT
grep -rn "CLAUDE_PLUGIN_ROOT.*\.\." plugins/<name>/hooks/
```

For each match, confirm it falls under "Acceptable exceptions" above; otherwise rewrite it to be self-contained within the plugin.

---

## Required skills

### `plugin-update` (mandatory for every plugin)

Every plugin **must** ship a `plugin-update` skill that brings the project's plugin-related
artifacts into compliance with the currently installed plugin version. Manual invocation only
(`/<plugin>:plugin-update`).

**What "plugin-related artifacts" means**:

Two categories, handled differently:

| Category | Examples | Action |
|---|---|---|
| Static templates | Files the plugin copies verbatim into the project (rule templates, widget assets, config stubs) | Re-copy from plugin source (straightforward, automatic) |
| Convention-following files | Files the user created *following this plugin's guidance* (skills, hooks, agents, source code) | Inspect against current references; detect deviations and fix with user confirmation |

The static-copy part is easy. The convention-inspection part is the main value: when a plugin's
references or guidelines change, existing project files written under the old conventions may
now violate the new standards. `plugin-update` surfaces those violations and applies the fix.

**Why**: without this, version upgrades are silent. Users can install a newer plugin but their
existing project files continue to follow the old conventions — invisible drift that produces
inconsistent outputs over time.

**Standard contract**:

| Item | Convention |
|---|---|
| Name | `plugin-update` (kebab-case literal — not `<plugin>-update`) |
| Trigger | Manual only (no `description` auto-triggers; explicit `/<plugin>:plugin-update`) |
| First action | Refuse to run on `master` / `main` and ask the user to create a working branch first |
| Branch management | Do **not** create branches, commit, or merge — leave all branch operations to the user |
| Inter-plugin dependency | None — must not invoke skills or commands from other plugins |
| Scope | Only this plugin's own artifacts; never modify files owned by other plugins |
| Fix confirmation | Never modify convention-following files without explicit user confirmation |

When creating a new plugin, generate `skills/plugin-update/SKILL.md` (and `.jp.md`), list the
static templates to re-copy, and describe how to detect and fix deviations in files created by
this plugin's skills. The skill must be self-contained.

---

## Authoring workflow

### Step 1 — Determine mode: create or update

- **Mode**: new plugin, or updating an existing one?
- **Plugin name**: kebab-case (e.g. `code-reviewer`, `claude-kit`)
- If **updating**: read the existing `plugins/<name>/.claude-plugin/plugin.json` for the current version.

### Step 2 — Gather change details

**Creating**: description (one line), skills to include (name + purpose, at least one), other
components (agents/hooks/MCP).

**Updating**: what changed (skills added/modified/removed, structural changes, fixes), and the
**change type** to determine the version bump.

### Step 3 — Apply file changes

- **Creating**: generate the directory structure above. Add agents/hooks/MCP dirs only if requested.
  Create `CLAUDE.md` and `CLAUDE.jp.md` following `plugin-claude-md.md` — every plugin requires them.
- **Updating**: edit only the changed files; do not touch unrelated files. Also update
  `plugins/<name>/CLAUDE.md` to reflect any added/changed skills, hooks, or environment variables.

### Step 4 — plugin.json + marketplace.json + CLAUDE.md (keep versions and content in sync)

See the field/format/version sections below. Before committing, verify all three of the following
are updated:

- [ ] `plugins/<name>/CLAUDE.md` — reflect added/changed skills, hooks, environment variables, or behavior; bump `## Changelog`
- [ ] `plugins/<name>/.claude-plugin/plugin.json` — bump `version`
- [ ] `.claude-plugin/marketplace.json` — bump the matching plugin's `version`

**The version in `plugin.json`, the `.claude-plugin/marketplace.json` entry, and the `## Changelog`
table in `CLAUDE.md` must always be identical.** Never let these three drift.

> If two parallel PRs bump the same plugin and one merges first, rebump the other to the next
> version on its branch before merging (incident `parallel-pr-version-bump-collision`).

### Step 5 — Report

Report mode (created/updated), new version, files changed, and how to test locally:

```bash
claude --plugin-dir ./plugins/<plugin-name>
/<skill-name>
```

---

## plugin.json fields

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Plugin identifier (kebab-case). Used as the skill namespace. |
| `description` | Yes | Plugin description |
| `version` | Yes | Semantic versioning (e.g. `1.0.0`) |
| `author` | No | Author info |

```json
{
  "name": "<plugin-name>",
  "description": "<description>",
  "version": "1.0.0"
}
```

---

## marketplace.json entry

Add to `.claude-plugin/marketplace.json` → `plugins` array:

```json
{
  "name": "<plugin-name>",
  "source": "./plugins/<plugin-name>",
  "description": "<description>",
  "version": "1.0.0"
}
```

---

## Version bump rules

| Change type | Bump |
|---|---|
| Bug fix / minor correction | PATCH (`1.x.y` → `1.x.y+1`) |
| New skill or behavior change | MINOR (`1.x.0` → `1.x+1.0`) |
| Complete redesign | MAJOR (`1.0.0` → `2.0.0`) |

---

## Changelog

Version history is recorded in the `## Changelog` table at the bottom of the plugin's `CLAUDE.md`
(not in a separate `changelogs/` directory). One row per version, newest at the top. Keep summaries
brief — git history has the full diff.

Full authoring guide: `plugin-claude-md.md`.

---

## Environment variables

A plugin's hooks/scripts can be made configurable via environment variables set in `settings.json`'s
`env` block and read with `os.environ` (full guide: `environment.md`). When a plugin reads any env var,
**document it in the `## Environment Variables` table of the plugin's `CLAUDE.md`** — key, values
(with default marked), and description. Namespace the key with the plugin name
(e.g. `PY_KIT_INJECTION_TTL`). See `plugin-claude-md.md` for the table format.

### Markdown files cannot read environment variables

**Only hooks and scripts (`.py` files, inline `-c` commands) can read env vars via `os.environ`.**
Markdown instruction files (`CLAUDE.md`, rules, `SKILL.md`, references) are loaded into context
as text — they are never executed and have no access to the process environment.

Never instruct Claude to "run `echo $VAR`" inside a Markdown file to detect an env var value.
Instead, use one of these patterns:

| Pattern | When to use |
|---|---|
| **Hook template injection** | Hook reads the var and passes it as a Jinja2 variable to the injection template; the template adds a one-line notice (e.g. `` `CLAUDE_KIT_JP_MIRROR=false` ``). Claude reads the notice in its injected context and branches accordingly. Best for a small number of vars affecting a specific skill/rule. |
| **Session-start env injection** | A dedicated hook runs at `UserPromptSubmit` and injects all env var values into Claude's context once per session. Best when many vars need to be visible across all Markdown files. |
