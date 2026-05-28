# next-kit references — index

The next-kit conventions are split into **1 file = 1 use case** reference files.
You only read the ones relevant to your current edit.

Management is split across two files:

| File | Role |
|---|---|
| **`index.yaml`** (English) / **`index.jp.yaml`** (Japanese mirror) | Reference list + one-line `description`. The hook parses the English version for injection (Japanese version is a human-only mirror). |
| **`injection_rules.yaml`** | Mapping of edit-target file-path patterns → required / optional references (language-independent). |

---

## Reading manually

1. Read **`index.yaml`** to see what each reference covers.
2. Match the edit-target file path against the `rules[].pattern` entries in **`injection_rules.yaml`**.
   - Example: editing `src/app/api/v1/resources/route.ts` matches both `**/*.{ts,tsx}` and `**/app/api/v1/**/route.ts`.
3. Read all `required` references for the matching rules; read `optional` ones if relevant.

---

## Reading automatically

The `next-references-injection` hook (PreToolUse) does this on every `Edit` / `Write` / `MultiEdit` / `Read`:

1. Reads `injection_rules.yaml` and collects matching rules
2. Looks up each reference's description from `index.yaml`
3. Reads each `required` reference body in full (`optional` stays path + description only)
4. Renders the Jinja2 template (`hooks/templates/injection.md.j2`)
5. Injects the result via `decision: block` in the `reason` field

A two-tier TTL token (`~/.claude/tokens/next-kit/{session_id}.yaml`) throttles re-injection within the TTL window (default 3600s, env `NEXT_KIT_INJECTION_TTL`): the `patterns` map skips an already-injected pattern, and the `references` map shows a `required` reference already injected this session (via any pattern) by **path only**, so a reference shared across patterns is never re-injected.

Switch the injection language by setting `NEXT_KIT_INJECTION_LANG=jp` (default is `en`).

---

## TypeScript type-check hook

The `next-ts-check` hook (PostToolUse, `hooks/ts_check.py`) runs automatically after every `Edit` / `Write` / `MultiEdit` on `*.ts` / `*.tsx` files:

1. Searches upward from the edited file to find the nearest `tsconfig.json` (monorepo-aware)
2. Runs `tsc --noEmit --incremental` in that directory
3. If type errors are found, outputs them to stdout so Claude can see and fix them
4. Never blocks (`decision: block` is not used) — errors are informational

Switch to `tsc --noEmit` (without `--incremental`) if you want to disable the build cache.

---

## Used by SKILLs

| Skill | Role | When to use |
|---|---|---|
| `next-kit:implement` | Reads the matching reference for the edit-target file and implements according to it | When writing or editing a specific file |
| `next-kit:plan` | Loads references matching the user's request scope and outputs an implementation plan document (file tree + per-file roles + conventions) | Before starting implementation — to plan what files to create |

---

## Maintenance

- When adding a new reference, update **all three**: `index.yaml`, `index.jp.yaml`, and `injection_rules.yaml`.
- Same for deletes / renames.
- Keep this file (`references/CLAUDE.md`) minimal — point to the two management files; the per-reference descriptions live only in `index.yaml` (and its JP mirror).

---

## Cross-kit sync

py-kit also uses the same structure (`index.yaml` + `injection_rules.yaml` + `hooks/inject_references.py` + Jinja2 templates).
**If you change the structure on one side, change it on the other** — see `.claude/rules/feature/kit-hooks-index-sync.md`.
