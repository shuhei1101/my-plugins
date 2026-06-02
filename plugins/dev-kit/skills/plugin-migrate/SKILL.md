---
name: dev-kit:plugin-migrate
description: |
  Inspect and fix dev-kit-generated artifacts in the project (both static templates and
  source files that were created following dev-kit conventions) to ensure they comply with
  the currently installed dev-kit version's conventions.
  Covers both re-copying static templates and detecting/fixing convention deviations in
  existing project source files.
  Manual invocation only — use /dev-kit:plugin-migrate.
---

# dev-kit:plugin-migrate — Bring dev-kit Artifacts into Compliance with Current Conventions

## What it does

Two categories of dev-kit artifacts are handled differently:

| Category | Content | Action |
|---|---|---|
| Static templates | Rule files that `html-implement` ships to `.claude/rules/`, `uidev.css` / `uidev.js` that `html-debug-fab` deploys | Re-copy from plugin source (automatic) |
| Convention-following files | Python / HTML-CSS-JS / Next.js source code written by the user following dev-kit conventions | Inspect against current references; fix deviations with user confirmation |

Static template re-copy is automatic. Convention inspection is performed by Claude using the
current references (auto-injected by the injection hook when each file is `Read`).

Which language conventions to inspect is controlled by `settings.json` env vars
(`${DEV_KIT_PYTHON}` / `${DEV_KIT_HTML}` / `${DEV_KIT_NEXT}`).

This skill depends on no other plugin. Committing and merging are the user's responsibility.

---

## Static templates (re-copied in Step 1)

| Source (`${CLAUDE_PLUGIN_ROOT}/`) | Destination |
|---|---|
| `skills/html-debug-fab/templates/uidev.css` | Project static asset directory |
|  | `uidev.js` in the same directory |
|  | `CLAUDE.md` in the same directory |
|  | `CLAUDE.jp.md` in the same directory |

---

## Tasks

### Step 1: Re-copy html-debug-fab widget

#### Condition

- `uidev.css` exists anywhere in the project (html-debug-fab considered deployed)

#### Process

1. `find . -name 'uidev.css' -not -path '*/node_modules/*' -not -path '*/.git/*'`
2. Not found → treat as not deployed; skip to Step 2
3. Exactly one match → that directory is the target
4. Multiple matches → ask the user which to target
5. Copy `uidev.css` / `uidev.js` / `CLAUDE.md` / `CLAUDE.jp.md` from
   `${CLAUDE_PLUGIN_ROOT}/skills/html-debug-fab/templates/` (skip `example.html`)
6. Report which files were updated

→ Proceed to Step 2

---

### Step 2: Inspect Python source files (if `${DEV_KIT_PYTHON}` is enabled)

#### Condition

- `${DEV_KIT_PYTHON}` is truthy in `settings.json` env

#### Process

1. List Python files in the project
   ```bash
   find . -name "*.py" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/__pycache__/*"
   ```
2. `Read` each file — the injection hook auto-injects the Python references
3. Compare against the current conventions in the injected references; identify deviations
   - Examples: missing type hints, non-standard logger implementation, incorrect settings structure
4. For each file with deviations: show the deviation and proposed fix; get user confirmation before making changes
5. Process in batches of ~10 files if the project is large

→ Proceed to Step 3

#### Notes

The Python references auto-injected from `references/python/` are the authoritative standard.
Do not flag anything not explicitly stated in those references.

---

### Step 3: Inspect HTML/CSS/JS source files (if `${DEV_KIT_HTML}` is enabled)

#### Condition

- `${DEV_KIT_HTML}` is truthy in `settings.json` env

#### Process

1. List HTML / CSS / JS files
   ```bash
   find . \( -name "*.html" -o -name "*.css" -o -name "*.js" \) -not -path "*/node_modules/*" -not -path "*/.git/*"
   ```
2. `Read` each file (HTML references are auto-injected)
3. Inspect against current conventions (FLOCSS, design tokens, DebugFAB usage, etc.)
4. For each deviation: show and propose fix, confirm with user before applying

→ Proceed to Step 4

---

### Step 4: Inspect TypeScript/TSX source files (if `${DEV_KIT_NEXT}` is enabled)

#### Condition

- `${DEV_KIT_NEXT}` is truthy in `settings.json` env

#### Process

1. List TS / TSX files
   ```bash
   find . \( -name "*.ts" -o -name "*.tsx" \) -not -path "*/node_modules/*" -not -path "*/.git/*"
   ```
2. `Read` each file (Next.js references are auto-injected)
3. Inspect against current conventions (file placement, Server Actions, auth, DB helpers, etc.)
4. For each deviation: show and propose fix, confirm with user before applying

→ Proceed to Step 5

---

### Step 5: Report completion

#### Process

1. List all static template files that were re-copied
2. List all source files where convention deviations were found and fixed
3. Show `git diff` for user review
4. Present a suggested commit message; leave the actual commit to the user
   - Suggested: `chore: sync dev-kit generated artifacts to v{N}`
   - Read version from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`

→ Done

#### Notes

##### Prohibitions

- Never commit to master / main directly
- Never apply fixes to convention-following files without explicit user confirmation
