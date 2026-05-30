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

## Required skills

### `plugin-update` (mandatory for every plugin)

Every plugin **must** ship a `plugin-update` skill that brings the project's plugin-generated
artifacts in line with the currently installed plugin version. Manual invocation only
(`/<plugin>:plugin-update`).

**Why**: when a plugin ships static templates (`.work/CLAUDE.md`, hook prompts, sample configs,
references injected via `injection_rules.yaml`, etc.) into the project, those copies drift behind
the plugin source as new versions are released. Without a per-plugin sync command, the user has
to diff and copy by hand. Each plugin owns its own update path because each plugin knows its own
templates and migration rules.

**Standard contract**:

| Item | Convention |
|---|---|
| Name | `plugin-update` (kebab-case literal — not `<plugin>-update`) |
| Trigger | Manual only (no `description` auto-triggers; explicit `/<plugin>:plugin-update`) |
| First action | Invoke the project's PR-branch skill (e.g. `/workspace:work-start`) so edits land on a reviewable branch |
| Scope | Only this plugin's own static artifacts; never reach into other plugins |
| Reference | See `plugins/workspace/skills/plugin-update/SKILL.md` for the canonical example |

When creating a new plugin, generate `skills/plugin-update/SKILL.md` (and `.jp.md`) following the
workspace example and adapt the template list to whatever static files your plugin ships.

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
- **Updating**: edit only the changed files; do not touch unrelated files.

### Step 4 — plugin.json + marketplace.json + changelog (keep versions identical)

See the field/format/version sections below. **The version in `plugin.json`, the
`.claude-plugin/marketplace.json` entry, and the `## Changelog` table in `CLAUDE.md` must
always be identical.** Never let these three drift.

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
