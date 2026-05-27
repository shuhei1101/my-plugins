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

The `next-references-injection` hook (PreToolUse, implemented in the same plugin) does this on every `Edit` / `Write` / `MultiEdit`:

1. Reads `injection_rules.yaml` and collects matching rules
2. Looks up each reference's description from `index.yaml`
3. Reads each reference body
4. Renders the Jinja2 template (`hooks/templates/injection.md.j2`)
5. Injects the result via `decision: block` in the `reason` field

A session + file-hash token prevents the hook from blocking the same file twice in one session.

Switch the injection language by setting `NEXT_KIT_INJECTION_LANG=jp` (default is `en`).

---

## Used by SKILLs

`next-kit:implement` reads `index.yaml` first in its Step 1 to identify which reference applies to the edit target.

---

## Maintenance

- When adding a new reference, update **all three**: `index.yaml`, `index.jp.yaml`, and `injection_rules.yaml`.
- Same for deletes / renames.
- Keep this file (`references/CLAUDE.md`) minimal — point to the two management files; the per-reference descriptions live only in `index.yaml` (and its JP mirror).

---

## Cross-kit sync

py-kit also uses the same structure (`index.yaml` + `injection_rules.yaml` + `hooks/inject_references.py` + Jinja2 templates).
**If you change the structure on one side, change it on the other** — see `.claude/rules/feature/kit-hooks-index-sync.md`.
