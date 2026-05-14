---
name: yaml-rule
description: YAML file management conventions for project assets and configuration. Always apply this skill when: creating or editing index.yaml, settings.yaml, or settings.yaml.sample; setting up asset or media file management in a project; asking about the difference between index.yaml and settings.yaml; or designing any project structure that references files via YAML. Trigger immediately when the user says "create index.yaml", "set up settings.yaml", "manage assets with YAML", or starts a new project that needs asset or configuration management.
---

# yaml-rule — YAML File Management

Defines how to create and manage `index.yaml`, `settings.yaml`, and `settings.yaml.sample` for asset catalogs and project configuration.

---

## Overview

Physical files (assets, media, etc.) can be placed in any folder structure freely. Programs and AI must not hard-code file paths — they must reference files through YAML.

**Three-file pattern per feature:**

```
{feature}/
├── index.yaml           # asset catalog (committed, environment-independent)
├── settings.yaml        # local config (gitignored, per-developer)
└── settings.yaml.sample # template (committed)
```

---

## Tasks

### Step 1: Identify the YAML operation

#### Condition

- Always — before creating or editing any YAML file

#### Process

1. Determine what the user needs:

   | User request | Go to |
   |---|---|
   | Register new assets or list what exists | Step 2 (index.yaml) |
   | Create or update environment-specific config | Step 3 (settings.yaml.sample) |
   | Handle gitignore for settings.yaml | Step 4 (gitignore) |
   | Runtime-editable YAML in a worktree project | Step 5 (worktree safety) |
   | Document YAML conventions for this domain | Step 6 (rules file) |

→ Proceed to the appropriate step

#### Output

- Confirmed YAML operation type

---

### Step 2: Create or update index.yaml

#### Condition

- User wants to register assets or catalog files for a feature

#### Input

- Feature name and list of files to register

#### Process

1. Add entries to `{feature}/index.yaml`:
   - Values must be **environment-independent** — same across all developers and deployments
   - Think of it as a manifest: it describes what exists, not how to use it
   - Keep the YAML terse — no comment blocks with rules or change history (see Step 6 for that)
2. A short pointer comment at the top is fine:
   ```yaml
   # See .claude/rules/assets-{feature}.md for management conventions
   ```
3. When a new asset is added → add an entry to `index.yaml` AND add the corresponding key to `settings.yaml.sample`.
4. When an asset is removed → mark inactive or remove the entry from `index.yaml` AND remove the key from `settings.yaml.sample`.

→ Proceed to Step 3 to update settings.yaml.sample if new keys were added

#### Output

- `index.yaml` updated with new or modified entries

#### Notes

##### Prohibitions

- Do not put management rules, change history, or per-field explanations inside `index.yaml` as comment blocks — keep the YAML as data only

---

### Step 3: Create or update settings.yaml.sample

#### Condition

- New keys were added to index.yaml, or a new config option is introduced

#### Input

- Keys to add, with placeholder or default values

#### Process

1. Add the new keys to `{feature}/settings.yaml.sample` with placeholder values and short inline comments.
2. `settings.yaml.sample` is the **template** committed to the repository — each developer copies it to `settings.yaml` and fills in their own values.
3. `settings.yaml` itself is **never committed** — it is gitignored (see Step 4).

→ Proceed to Step 4 to verify gitignore, or done if gitignore is already configured

#### Output

- `settings.yaml.sample` updated with new keys

---

### Step 4: Configure gitignore

#### Condition

- `settings.yaml` is not yet listed in `.gitignore`

#### Input

- Project root `.gitignore`

#### Process

1. Add `settings.yaml` to `.gitignore`:
   ```
   settings.yaml
   ```
2. Verify that `settings.yaml.sample` is **not** in `.gitignore` — it must be committed.

→ Done

#### Output

- `settings.yaml` excluded from version control
- `settings.yaml.sample` committed as template

---

### Step 5: Handle runtime-editable YAML for worktrees

#### Condition

- The project uses git worktrees AND a YAML file is written at runtime by the UI or API (e.g., `settings.yaml`, `runtime_state.yaml`)

#### Input

- The YAML file that needs to be written at runtime
- The worktree setup method available (symlink / junction / copy)

#### Process

1. Determine which YAML files this applies to:

   | YAML | Apply this rule? | Reason |
   |---|---|---|
   | `settings.yaml` | ✅ Yes | Written by the UI / config screen |
   | `mock_notes.yaml`, `runtime_state.yaml`, etc. | ✅ Yes | Written by the app via API |
   | `index.yaml` | ❌ No | Hand-edited catalog — each worktree has its own copy |
   | `settings.yaml.sample` | ❌ No | Committed template |

2. Choose one of the two valid implementations:

   **A. Filesystem level (symlink / junction)**
   In the worktree setup script, link `<worktree>/path/to/settings.yaml` → `<main-repo>/path/to/settings.yaml`. The app reads and writes using the regular path; the symlink transparently routes to main. Fall back to copy on platforms that don't support symlinks.

   **B. App level (runtime path resolution)**
   Provide a helper like `main_repo_root()` that returns the main repository path even when called from a linked worktree. Detection uses `git rev-parse --git-common-dir`:
   - In the main worktree it returns `.git` (relative)
   - In a linked worktree it returns an absolute path to main's `.git` directory

   App code composes runtime-editable YAML paths as `main_repo_root() / "path/to/file.yaml"` so every worktree resolves to the same canonical file.

3. Document the choice in the matching `.claude/rules/<name>.md` (see Step 6):
   - Which resolution method (A: symlink / B: runtime helper)
   - Where the canonical file lives (`<main-repo>/data/...` or similar)
   - Whether the file is gitignored

→ Done

#### Output

- Runtime-editable YAML resolves to the main repository copy in all worktrees
- Method documented in the rules file

#### Notes

##### Why this matters

If runtime-editable YAML lives inside the worktree: the user works in worktree A and saves settings via the UI → the worktree's YAML is updated, but the main repository's YAML is unchanged → when the worktree is deleted, the saved configuration is **lost**. Everything the user configured disappears — the worst possible outcome for runtime state.

---

### Step 6: Document conventions in a rules file

#### Condition

- A new feature introduces YAML files with domain-specific management conventions

#### Input

- Feature name and the set of YAML files involved

#### Process

1. Create `.claude/rules/<feature-name>.md` with `paths:` frontmatter targeting the relevant YAML files.
2. The rule file loads automatically when Claude reads a matching YAML, so it provides context without bloating the data file.
3. Include in the rules file:
   - What each field means
   - Update procedure (when to update index.yaml vs settings.yaml.sample)
   - Runtime resolution method if applicable (from Step 5)
   - What NOT to do

→ Done

#### Output

- `.claude/rules/<feature-name>.md` created with domain-specific YAML conventions

#### Notes

##### Prohibitions

- Do not duplicate the rules content inside the YAML file itself
- A short pointer comment at the top of the YAML (one line) is fine — but never the full rule body

---

## References

### When to update each file

| Event | index.yaml | settings.yaml.sample | settings.yaml |
|-------|------------|----------------------|---------------|
| New asset added | Add entry | Add key with placeholder | Add key with local value |
| Asset removed | Mark inactive or remove | Remove key | Remove key |
| New config option | — | Add key + comment | Add key + local value |
| Structure change | Update | Update | Update manually |
