---
name: yaml-rule
description: YAML file management conventions for project assets and configuration. Always apply this skill when: creating or editing index.yaml, settings.yaml, or settings.yaml.sample; setting up asset or media file management in a project; asking about the difference between index.yaml and settings.yaml; adding a developer note or change history to a YAML file; or designing any project structure that references files via YAML. Trigger immediately when the user says "create index.yaml", "set up settings.yaml", "manage assets with YAML", "add a developer note to YAML", or starts a new project that needs asset or configuration management.
---

# YAML File Management Rules

These rules apply to all YAML files used for asset catalogs and project configuration.

## Core Principle

Physical files (assets, media, etc.) can be placed in any folder structure freely. Programs and AI must not hard-code file paths — they must reference files through YAML.

## Two Types of YAML Files

### index.yaml — Asset Catalog

- Lists all assets or files that belong to a category
- Created once at project setup; updated only when new files are added or removed
- Values are environment-independent (same across all developers and deployments)
- Think of it as a manifest: it describes what exists, not how to use it

### settings.yaml — Environment Configuration

- Contains settings for items registered in `index.yaml` (keyed by ID)
- Values are environment-specific — they differ between developers and deployments
- Think of it like a `.env` file: each environment has its own copy
- **Never commit `settings.yaml` to the repository.** Instead, commit `settings.yaml.sample` and have each developer create their own `settings.yaml` from it

### settings.yaml.sample

- A template version of `settings.yaml` committed to the repository
- Contains all keys with placeholder or default values
- Includes comments explaining each field
- Each developer copies this file to `settings.yaml` and fills in their own values

## Developer Note Block

Every `index.yaml` and `settings.yaml.sample` must begin with a developer note comment block. The `settings.yaml` actual file does not need this.

The note block serves as living documentation for AI-driven development — recording management rules and change history so future sessions have full context without needing to trace git history manually.

### Format

```yaml
# =============================================================================
# Developer Note
# =============================================================================
# Purpose:
#   {What this file manages and why it exists}
#
# Management Rules:
#   - {Rule 1: e.g., "Always assign a unique snake_case ID to each entry"}
#   - {Rule 2: e.g., "Do not remove entries — mark them inactive instead"}
#
# Change History:
#   - PR{N} ({date}): {What changed and why}
#   - commit {hash} ({date}): {What changed and why}
# =============================================================================
```

### index.yaml example

```yaml
# =============================================================================
# Developer Note
# =============================================================================
# Purpose:
#   Catalogs all background image assets for the VTuber application.
#   Programs load backgrounds by ID; physical file paths may change freely.
#
# Management Rules:
#   - IDs are snake_case and permanent — never rename or reuse an ID
#   - Add new entries at the bottom to preserve history
#
# Change History:
#   - PR1 (2026-05-01): Initial creation with 3 backgrounds
#   - PR4 (2026-05-08): Added "night_city" background
# =============================================================================

backgrounds:
  - id: living_room
    path: assets/backgrounds/living_room.png
    label: Living Room
  - id: night_city
    path: assets/backgrounds/night_city.png
    label: Night City
```

### settings.yaml.sample example

```yaml
# =============================================================================
# Developer Note
# =============================================================================
# Purpose:
#   Per-environment settings for backgrounds registered in index.yaml.
#   Copy this file to settings.yaml and adjust values for your environment.
#
# Management Rules:
#   - Keys must match IDs defined in index.yaml
#   - settings.yaml is gitignored — never commit it
#
# Change History:
#   - PR1 (2026-05-01): Initial creation
#   - PR4 (2026-05-08): Added "night_city" entry
# =============================================================================

backgrounds:
  living_room:
    enabled: true
    display_order: 1
  night_city:
    enabled: false   # set to true to enable in your environment
    display_order: 2
```

## File Structure Pattern

```
{feature}/
├── index.yaml           # asset catalog (committed, environment-independent)
├── settings.yaml        # local config (gitignored, per-developer)
└── settings.yaml.sample # template (committed, with developer note + comments)
```

Add `settings.yaml` to `.gitignore`:

```
settings.yaml
```

## When to Update Each File

| Event | index.yaml | settings.yaml.sample | settings.yaml |
|-------|------------|----------------------|---------------|
| New asset added | Add entry | Add key with placeholder | Add key with local value |
| Asset removed | Mark inactive or remove | Remove key | Remove key |
| New config option | — | Add key + comment | Add key + local value |
| Structure change | Update + add to Change History | Update + add to Change History | Update manually |
