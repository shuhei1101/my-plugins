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

## UI-editable YAML must resolve to the main-repository copy

When the project uses git worktrees, any YAML file that is written **at runtime** by the UI / API (e.g. `settings.yaml`, runtime state files) must always read and write to the **main repository's copy**, never to the worktree's local copy.

### Why this matters

If runtime-editable YAML lives inside the worktree:

1. The user works in worktree A and saves settings via the UI
2. The worktree's YAML is updated, but the main repository's YAML is unchanged
3. When that worktree is deleted (or the user switches to another branch), the saved configuration is **lost**
4. Everything the user clicked through and saved disappears — the worst possible outcome for runtime state

### Two valid implementations (pick one)

**A. Filesystem level (symlink / junction)**

In the worktree setup script, link `<worktree>/path/to/settings.yaml` → `<main-repo>/path/to/settings.yaml`. The app reads and writes using the regular path; the symlink transparently routes to main. Fall back to copy on platforms that don't support symlinks.

**B. App level (runtime path resolution)**

Provide a helper like `main_repo_root()` that returns the main repository path even when called from a linked worktree. Detection uses `git rev-parse --git-common-dir`:

- In the main worktree it returns `.git` (relative)
- In a linked worktree it returns an absolute path to main's `.git` directory

App code composes runtime-editable YAML paths as `main_repo_root() / "path/to/file.yaml"` so every worktree resolves to the same canonical file.

### Which YAML this applies to

| YAML | Apply this rule? | Reason |
|---|---|---|
| `settings.yaml` | ✅ Yes | Written by the UI / config screen |
| `mock_notes.yaml`, `runtime_state.yaml`, etc. | ✅ Yes | Written by the app via API |
| `index.yaml` | ❌ No | Hand-edited catalog. Each worktree has its own copy and merges through git normally |
| `settings.yaml.sample` | ❌ No | Committed template |

### Document the choice

When introducing a new runtime-editable YAML, record in the matching `.claude/rules/<name>.md`:

- Which resolution method (A: symlink / B: runtime helper)
- Where the canonical file lives (`<main-repo>/data/...` or similar)
- Whether the file is gitignored

This way future maintainers (and future Claude sessions) can see the structure at a glance.
