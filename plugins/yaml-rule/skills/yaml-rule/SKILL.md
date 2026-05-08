---
name: yaml-rule
description: YAML file management conventions for project assets and configuration. Always apply this skill when: creating or editing index.yaml, settings.yaml, or settings.yaml.sample; setting up asset or media file management in a project; asking about the difference between index.yaml and settings.yaml; or designing any project structure that references files via YAML. Trigger immediately when the user says "create index.yaml", "set up settings.yaml", "manage assets with YAML", or starts a new project that needs asset or configuration management.
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
- Each developer copies this file to `settings.yaml` and fills in their own values

## Document conventions outside the YAML

Do **not** put management rules, change history, or per-field explanations inside the YAML as comment blocks. The YAML is data — keep it terse.

Document those conventions in `.claude/rules/<name>.md` instead, with a `paths:` frontmatter targeting the relevant YAML files. The rule file loads automatically when Claude reads a matching YAML, so it serves the same "context for whoever opens this file" purpose without bloating the data file. See the `claude-rule` skill for how to author rule files.

A short pointer comment at the top of a YAML (e.g., one line saying "see .claude/rules/assets-bgm.md") is fine, but never duplicate the rule's body inside the YAML.

## File Structure Pattern

```
{feature}/
├── index.yaml           # asset catalog (committed, environment-independent)
├── settings.yaml        # local config (gitignored, per-developer)
└── settings.yaml.sample # template (committed)
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
| Structure change | Update | Update | Update manually |
