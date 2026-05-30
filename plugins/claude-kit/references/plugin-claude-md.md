# Plugin CLAUDE.md Authoring Guide

How to write the root `CLAUDE.md` (and `CLAUDE.jp.md` mirror) for a plugin.
This guide is self-contained: when injected (because you are editing a plugin's `CLAUDE.md`),
follow it to author the file directly. Read `common.md` alongside it.
Japanese mirror: `references/plugin-claude-md.jp.md`

---

## Required sections

| Section | Content | Required |
|---|---|---|
| H1 title | Plugin name | **Always required** |
| `## Overview` | 1–3 sentence description of what the plugin does | **Always required** |
| `## Skills` | Table: skill / description / caller (who invokes it) | **Always required** |
| `## Changelog` | Table at the bottom: version / date / summary | **Always required** |
| `## Hooks` | Table: trigger type (merged rows) / hook name / behavior | Required when plugin ships hooks |
| `## Environment Variables` | Table: key / values (BR-separated if multiple) / description | Required when plugin reads env vars |
| `## Dependencies` | Table: plugin / relationship | Required when plugin has dependencies |
| `## Overall Policy` | Major design decisions or version-transition notes | Optional |
| `## Plugin Structure` | Directory tree | Optional |
| `## Structure of references/` | Reference file hierarchy | Optional (for plugins with many references) |

---

## Overview section

Write 1–3 sentences explaining the plugin's purpose — what it does, who uses it, and the main
problem it solves. Keep it self-contained so a reader knows the plugin's scope without reading
any other file.

```markdown
## Overview

{One-to-three sentence description of what this plugin does, who uses it, and what problem it solves.}
```

---

## Skills table

List every skill the plugin ships. The **Caller** column records who or what invokes the skill —
the SKILL.md description already carries the trigger condition, so here we note the dispatch path:
explicit user call, a named hook, or another skill.

```markdown
## Skills

| Skill | Description | Caller |
|---|---|---|
| `{plugin}:{skill}` | {one-line purpose} | User calls `/{plugin}:{skill}` explicitly |
| `{plugin}:{skill-2}` | {one-line purpose} | Dispatched by the `{hook-name}` hook |
| `{plugin}:{skill-3}` | {one-line purpose} | Called by `{plugin}:{other-skill}` Step 4 |
```

---

## Hooks table

Group rows by trigger type. When consecutive rows share the same trigger, leave the trigger cell
blank (visual merging). Order: `PreToolUse` → `PostToolUse` → `UserPromptSubmit` → `Stop`.

```markdown
## Hooks

| Trigger | Hook | Behavior |
|---|---|---|
| `PreToolUse(Edit \| Write)` | `{hook-name}` | {what it does on every edit/write} |
| | `{hook-name-2}` | {second hook with the same trigger — trigger cell is blank} |
| `UserPromptSubmit` | `{hook-name}` | {what it injects into context at prompt time} |
| `Stop` | `{hook-name}` | {what it runs when Claude stops} |
```

---

## Environment variables table

List every env var the plugin reads. In the **Values** column:

- Use `<br>` to separate multiple values on separate lines
- Mark the default with **(default)**
- For boolean toggles, always list both `true` / `false`

```markdown
## Environment Variables

| Key | Values | Description |
|---|---|---|
| `{PREFIX}_INJECTION_TTL` | integer seconds **(default: 3600)** | TTL for the injection token cache |
| `{PREFIX}_INJECTION_LANG` | `en` **(default)**<br>`jp` | Language for injected descriptions |
| `{PREFIX}_SOME_TOGGLE` | `true` **(default)**<br>`false` | Enables / disables some behavior when falsy (`false` / `0` / `no` / `off`) |
```

Set these in `settings.json` → `env` block. Full guide: `environment.md`.

---

## Dependencies table

List plugins this plugin depends on or closely coordinates with.

```markdown
## Dependencies

| Plugin | Relationship |
|---|---|
| `claude-kit` | Source of creator skills and hook policy |
| `ref-inject` | Provides the injection hook template; regenerate via `/ref-inject:apply` |
```

---

## Changelog table

Always placed **at the bottom** of the file. One row per version; newest at the top.
Keep summaries brief — git history has the full diff.
**Replaces the `changelogs/` directory** — do not create `changelogs/vX.Y.Z.md` files.

```markdown
## Changelog

| Version | Date | Summary |
|---|---|---|
| 1.1.0 | YYYY-MM-DD | {brief summary of what changed} |
| 1.0.0 | YYYY-MM-DD | Initial release |
```

---

## Full template

Copy this and fill in the placeholders:

```markdown
# {Plugin Name} Plugin Developer Guide

## Overview

{One-to-three sentence description of what this plugin does.}

---

## Skills

| Skill | Description | Caller |
|---|---|---|
| `{plugin}:{skill}` | {purpose} | {explicit / hook dispatch / called by skill} |

---

## Hooks

| Trigger | Hook | Behavior |
|---|---|---|
| `{trigger}` | `{hook-name}` | {behavior} |

---

## Environment Variables

| Key | Values | Description |
|---|---|---|
| `{PREFIX}_{KEY}` | `{value}` **(default)**<br>`{alt}` | {description} |

---

## Dependencies

| Plugin | Relationship |
|---|---|
| `{plugin}` | {relationship} |

---

## Changelog

| Version | Date | Summary |
|---|---|---|
| 1.0.0 | YYYY-MM-DD | Initial release |
```

Omit `## Hooks`, `## Environment Variables`, and `## Dependencies` sections if the plugin has none.
