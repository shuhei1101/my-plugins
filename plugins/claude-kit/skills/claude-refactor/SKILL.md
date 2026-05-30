---
name: claude-refactor
description: |
  Audit and organize Claude configuration (rules / skills / CLAUDE.md / hooks).
  Trigger when the user says "ルールを整理して", "設定が肥大化してきた",
  "スキルに重複がある気がする", "CLAUDE.md が長くなってきた",
  ".claude/ をきれいにしたい", or calls `/claude-kit:claude-refactor` explicitly.
---

# claude-refactor — Audit and Reorganize Claude Configuration

Audits rules / skills / CLAUDE.md / hooks under `.claude/` and proposes folder restructuring,
over-coupling / duplicate detection, file-type migration, and JP/EN mirror integrity checks.

All the criteria for these judgments live in this plugin's `references/` (read in Step 1). This skill
is the **workflow** (collect → analyze → present → execute); it does not restate the criteria inline.

---

## Tasks

### Step 1: Collect target files and load the criteria

#### Process

1. Read the reference guides (this plugin's `references/`) — they are the criteria for every judgment below:
   - `common.md` — file-type decision criteria, anti-proliferation guard, JP/EN mirror rules
   - `rules.md` — two rule types, use-case-oriented design, consolidation/separation, folder structure
   - `skills.md` — when a skill is the right type, step structure
   - `hooks.md` — hook events, when to use hooks
   - `claude-md.md` — thinness principle, extraction destinations
2. Collect the targets:

| Scope | Collection target |
|---|---|
| rules | Glob `.claude/rules/**/*.md`; read each `paths:` and summary |
| rules JP | Glob `.claude/rules-jp/**/*.md`; check pairing with English rules |
| skills | Glob `.claude/skills/**/SKILL.md` + `plugins/*/skills/**/SKILL.md`; read `name` / `description` |
| skills JP | Check existence of each `SKILL.jp.md` |
| CLAUDE.md | List all `CLAUDE.md` (root + subfolders); check line counts |
| CLAUDE.md JP | Check existence of each `CLAUDE.jp.md` |
| hooks | Read the hooks section of `.claude/settings.json` / `settings.local.json` / `hooks/hooks.json` |

→ Proceed to Step 2

---

### Step 2: Analyze each scope against the references

#### Process

Apply the criteria from the Step 1 references — do not re-derive them here.

- **rules** (`rules.md` + `common.md`): folder-structure cleanup (flat files → `core/` / `feature/` / optional folders), consolidation candidates (same domain / duplicated `paths:`), separation candidates (`paths:` spanning unrelated domains), and file-type fit.
- **skills** (`skills.md` + `common.md`): similar-skill pairs (overlapping `description` triggers — present, do not force-merge) and file-type fit (should it be a rule / CLAUDE.md line instead?).
- **CLAUDE.md** (`claude-md.md`): bloat (over ~200 lines, or detail/workflow/reference material that belongs elsewhere) and per-section extraction destinations.
- **hooks** (`hooks.md`): content in rules/CLAUDE.md that should become a hook (per the event mapping), and redundant/unused existing hook entries.
- **JP/EN mirrors** (`common.md`): missing `.jp.md` / `rules-jp/` / `CLAUDE.jp.md` counterparts.

→ Proceed to Step 3

---

### Step 3: Present proposals and confirm

#### Process

1. Organize findings into these tables (omit a table if it has no items; report "no issues" per empty scope):

   - **rules: folder moves** — file (current) / destination / reason
   - **rules: consolidation** — target / merge into / reason
   - **rules: separation** — target / split plan / reason (context savings)
   - **file-type migration** — target (current) / destination type / reason
   - **CLAUDE.md extraction** — section / destination / reason
   - **hook migration** — target (current) / hook event / reason
   - **similar skills** — skill A / skill B / similarities / differences
   - **missing JP mirrors** — English file / JP mirror to create

2. Ask the user: **run all**, **select individually**, or **cancel**. Wait for confirmation.

→ Proceed to Step 4

---

### Step 4: Execute the confirmed changes

#### Process

Apply only what the user approved. **Edit the target files directly** — the authoring guides
(`skills.md` / `rules.md` / `claude-md.md` / `hooks.md` + `provenance.md`) are auto-injected by the
`claude-kit-references-injection` hook when you write each file, so follow them in place.

- **rule folder restructure**: move with `git mv` (preserve history); generate an `_overview.md` per folder:

  ```markdown
  # {folder-name} — {one-line category description}

  ## About this folder

  {1–3 sentences on the policy for rules in this category}

  ## File list

  | File | Content |
  |---|---|
  | `{file}.md` | {one-line description} |
  ```

- **rule / skill / CLAUDE.md / hook create / convert / consolidate / split**: edit directly per the injected guide; keep the JP mirror in sync.
- **JP mirror creation**: author the `.jp.md` (or use the `jp-mirror-translator` agent).
- After any rename/move, update every reference to the file elsewhere in the project.

→ Proceed to Step 5

#### Notes

##### Prohibitions

- Use `git mv`, not `cp` (preserve git history)
- Always update references in other skills/rules that mention renamed/moved files

---

### Step 5: Report results

#### Process

1. Report changed / generated / deleted files
2. Prompt the user to review and commit

---

## References

The criteria live in this plugin's `references/` (read in Step 1): `common.md`, `rules.md`,
`skills.md`, `hooks.md`, `claude-md.md` — plus `provenance.md` for stamping edited files.
