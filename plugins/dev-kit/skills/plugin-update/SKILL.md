---
name: plugin-update
description: |
  Bring the current project's dev-kit-generated artifacts in line with the currently installed
  dev-kit version: re-copy the HTML rule templates that `html-implement` ships into
  `.claude/rules/`, and the debug widget (`uidev.css` / `uidev.js` / `CLAUDE.md`) that
  `html-debug-fab` ships into the project's static asset directory.
  Other plugins' generated artifacts are out of scope.
  Manual invocation only — use /dev-kit:plugin-update.
---

# dev-kit:plugin-update — Sync dev-kit-Generated Artifacts to Latest Versions

Scope is **the static files dev-kit copies into the project** only:

- HTML rule templates that `html-implement` ships into the project's `.claude/rules/`
- The debug widget (`uidev.css` / `uidev.js` / `CLAUDE.md`) that `html-debug-fab` ships into
  the project's static asset directory

`py-script` / `py-project` / `next-implement` / `next-plan` / `yaml` are reference-injection
skills — they do not copy any static files into the project, so they are out of scope. Files
that live only inside the plugin (`references/`, `injection_rules.yaml`, etc.) are also
out of scope.

Per-plugin sync logic for *other* plugins is never touched here — each plugin owns its own
`plugin-update` and ships its own.

---

## Sync targets

| Source (`{dev_kit_root}/`) | Destination |
|---|---|
| `templates/html/rules/css-js-link.md` | `.claude/rules/css-js-link.md` |
| `templates/html/rules/css-js-link.jp.md` | `.claude/rules-jp/css-js-link.md` (drop `.jp.` suffix) |
| `templates/html/rules/common-component-first.md` | `.claude/rules/common-component-first.md` |
| `templates/html/rules/common-component-first.jp.md` | `.claude/rules-jp/common-component-first.md` (same) |
| `skills/html-debug-fab/templates/uidev.css` | Project static asset directory |
| | `uidev.js` in the same directory |
| | `CLAUDE.md` in the same directory |
| | `CLAUDE.jp.md` in the same directory |

`{dev_kit_root}` = `${CLAUDE_PLUGIN_ROOT}` (resolved to the dev-kit plugin at skill runtime).

---

## Tasks

### Step 1: Prepare a PR branch

#### Condition

- Always — run first

#### Process

1. Check whether the workspace plugin's `.work/` directory exists in the current project
2. **If present**:
   - Invoke `/workspace:work-start` to create a PR branch dedicated to this sync
   - Wait until the worktree and branch are created
3. **If absent**:
   - Ask the user: "workspace plugin is not installed — commit directly to the current branch?"
     and proceed only after confirmation

→ Proceed to Step 2

#### Output

- The branch where the following file edits and commit will land (a fresh PR branch or the
  current branch) is decided

---

### Step 2: Overwrite the html-implement rule templates

#### Condition

- Step 1 complete

#### Process

1. Detect whether html-implement is in use by checking the destination
   - If `.claude/rules/css-js-link.md` does **not** exist → treat html-implement as unused;
     skip this step and proceed to Step 3
2. If in use, copy the four files in the html-implement rows of the table above from
   `${CLAUDE_PLUGIN_ROOT}/templates/html/rules/*` over the destinations
3. Report which files were overwritten

→ Proceed to Step 3

#### Output

- `.claude/rules/{css-js-link,common-component-first}.md` and
  `.claude/rules-jp/{css-js-link,common-component-first}.md` match the latest template

---

### Step 3: Overwrite the html-debug-fab widget

#### Condition

- Step 2 complete

#### Process

1. Locate the existing `uidev.css` in the project
   - Example: `find . -name 'uidev.css' -not -path '*/node_modules/*' -not -path '*/.git/*'`
2. **Not found** → treat html-debug-fab as not deployed; skip this step and proceed to Step 4
3. **Exactly one match** → that directory is the deployment target
4. **Multiple matches** → ask the user which directory to target before proceeding
5. Copy the following four files from `${CLAUDE_PLUGIN_ROOT}/skills/html-debug-fab/templates/`
   over the target directory:
   - `uidev.css`
   - `uidev.js`
   - `CLAUDE.md`
   - `CLAUDE.jp.md`
6. Do not copy `example.html` — it is a sample file, not a deployed asset
7. Report which files were overwritten

→ Proceed to Step 4

#### Output

- The target directory's `uidev.css` / `uidev.js` / `CLAUDE.md` / `CLAUDE.jp.md` match the
  latest template

---

### Step 4: Review and commit

#### Condition

- Step 3 complete

#### Process

1. Show the user `git status` and `git diff`
2. If there are no changes, report "All dev-kit artifacts are already up to date" and stop
3. If there are changes, commit them together:
   - When routed through workspace: `chore: sync dev-kit templates to v{N} #PR{N}`
   - Otherwise: `chore: sync dev-kit templates to v{N}`
4. Read the current dev-kit version from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`

→ Proceed to Step 5

#### Notes

##### Prohibitions

- Never commit to master directly (use the PR branch if routed through workspace, or the
  current non-master branch otherwise)

---

### Step 5: Report completion

#### Condition

- Step 4 complete

#### Process

1. List every file that was overwritten
2. If nothing changed, state explicitly "All artifacts already up to date"
3. When routed through workspace, suggest running `/workspace:merge`

→ Done
