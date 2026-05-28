# py-kit references — index

The py-kit Python conventions are split into **topic-axis reference files**.
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
   - Example: editing `src/{pkg}/features/chat/service.py` matches both `**/*.py` and `**/features/**/service.py`.
3. Read all `required` references for the matching rules; read `optional` ones if relevant.

---

## Reading automatically

The `py-kit-references-injection` hook (PreToolUse) does this on every `Edit` / `Write` / `MultiEdit` / `Read`:

1. Reads `injection_rules.yaml` and collects matching rules
2. Looks up each reference's description from `index.yaml`
3. Reads each `required` reference body in full (`optional` stays path + description only)
4. Renders the Jinja2 template (`hooks/templates/injection.md.j2`)
5. Injects the result via `decision: block` in the `reason` field

A per-pattern TTL token (`~/.claude/tokens/py-kit/{session_id}.yaml`) prevents re-injecting the same pattern within the TTL window (default 3600s, env `PY_KIT_INJECTION_TTL`).

Switch the injection language by setting `PY_KIT_INJECTION_LANG=jp` (default is `en`).

---

## Used by SKILLs

`py-kit:py-project` and `py-kit:py-script` both read `index.yaml` first in their Step 1.
Skill-specific behavior (e.g. `py-script` force-loading `scripts/python-script.md`) is encoded in the SKILL file itself.

---

## Maintenance

- When adding a new reference, update **all three**: `index.yaml`, `index.jp.yaml`, and `injection_rules.yaml`.
- Same for deletes / renames.
- Keep `references/CLAUDE.md` minimal — point to the two management files; the per-reference descriptions live only in `index.yaml` (and its JP mirror).
