# YAML — dev-kit Shared Reference

Conventions for YAML files used as asset catalogs and project configuration.
The `dev-kit:yaml` skill performs the operations; this document defines the rules they follow.

---

## Three-file pattern

Physical files (assets, media, etc.) can be placed in any folder structure freely.
Programs and AI must not hard-code file paths — they must reference files through YAML.

Per feature:

```
{feature}/
├── index.yaml           # asset catalog (committed, environment-independent)
├── settings.yaml        # local config (gitignored, per-developer)
└── settings.yaml.sample # template (committed)
```

---

## index.yaml

- Values are **environment-independent** — same across all developers and deployments
- Acts as a manifest: describes what exists, not how to use it
- Keep the YAML terse — no comment blocks with rules or change history
- A single-line pointer comment at the top is fine:
  ```yaml
  # See .claude/rules/assets-{feature}.md for management conventions
  ```

### Update rules

| Event | Action |
|---|---|
| New asset added | Add entry to `index.yaml` AND add the corresponding key to `settings.yaml.sample` |
| Asset removed | Mark inactive or remove from `index.yaml` AND remove the key from `settings.yaml.sample` |

---

## settings.yaml.sample (committed template)

- Each new key gets a placeholder value and a short inline comment
- This file is committed — developers copy it to `settings.yaml` and fill in their local values
- The actual `settings.yaml` is **never committed** (see gitignore section)

---

## gitignore

```
settings.yaml
```

Verify that `settings.yaml.sample` is **not** in `.gitignore` — the template must be committed.

---

## Runtime-editable YAML in worktrees

If the project uses git worktrees AND a YAML file is written at runtime by the UI or API
(e.g., `settings.yaml`, `runtime_state.yaml`), the file must resolve to the main repository copy
in every worktree. Otherwise, when the worktree is deleted, the saved configuration is **lost**.

### Which files this applies to

| YAML | Apply? | Reason |
|---|---|---|
| `settings.yaml` | ✅ | Written by the UI / config screen |
| `mock_notes.yaml`, `runtime_state.yaml`, etc. | ✅ | Written by the app via API |
| `index.yaml` | ❌ | Hand-edited catalog — each worktree has its own copy |
| `settings.yaml.sample` | ❌ | Committed template |

### Two valid implementations

**A. Filesystem level (symlink / junction)**
In the worktree setup script, link `<worktree>/path/to/settings.yaml` → `<main-repo>/path/to/settings.yaml`.
The app reads and writes using the regular path; the symlink transparently routes to main.
Fall back to copy on platforms that don't support symlinks.

**B. App level (runtime path resolution)**
Provide a helper like `main_repo_root()` that returns the main repository path even when called from
a linked worktree. Detection uses `git rev-parse --git-common-dir`:
- In the main worktree it returns `.git` (relative)
- In a linked worktree it returns an absolute path to main's `.git` directory

App code composes runtime-editable YAML paths as `main_repo_root() / "path/to/file.yaml"` so every
worktree resolves to the same canonical file.

### Documentation

The chosen method must be recorded in the matching `.claude/rules/<name>.md`:
- Which resolution method (A: symlink / B: runtime helper)
- Where the canonical file lives (`<main-repo>/data/...` or similar)
- Whether the file is gitignored

---

## Rules file (.claude/rules/)

For features with domain-specific YAML conventions, create `.claude/rules/<feature-name>.md`
with a `paths:` frontmatter targeting the relevant YAML files. The rule auto-loads when Claude
reads a matching YAML, so context is provided without bloating the data file.

Include in the rules file:
- What each field means
- Update procedure (when to update index.yaml vs settings.yaml.sample)
- Runtime resolution method if applicable
- What NOT to do

**Do not** duplicate the rules content inside the YAML file itself. A short pointer comment
(one line) at the top of the YAML is fine — but never the full rule body.

---

## When to update each file

| Event | index.yaml | settings.yaml.sample | settings.yaml |
|---|---|---|---|
| New asset added | Add entry | Add key with placeholder | Add key with local value |
| Asset removed | Mark inactive or remove | Remove key | Remove key |
| New config option | — | Add key + comment | Add key + local value |
| Structure change | Update | Update | Update manually |
