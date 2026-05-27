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

The **`refs-inject-kit` plugin** (separate plugin, PR140) does this on every `Edit` / `Write` / `MultiEdit`:

1. Auto-discovers installed plugins that have `references/injection_rules.yaml`
2. Reads each plugin's `injection_rules.yaml` and collects matching rules
3. Looks up each reference's description from the plugin's `index.yaml`
4. Reads each reference body
5. Renders the Jinja2 template (`refs-inject-kit/hooks/templates/injection.md.j2`)
6. Injects the result via `decision: block` in the `reason` field

A session + file-hash token prevents the hook from blocking the same file twice in one session.

Switch the injection language by setting `REFS_INJECT_KIT_LANG=jp` (default is `en`).

---

## Used by SKILLs

`py-kit:py-project` and `py-kit:py-script` both read `index.yaml` first in their Step 1.
Skill-specific behavior (e.g. `py-script` force-loading `scripts/python-script.md`) is encoded in the SKILL file itself.

---

## Maintenance

- When adding a new reference, update **all three**: `index.yaml`, `index.jp.yaml`, and `injection_rules.yaml`.
- Same for deletes / renames.
- Keep `references/CLAUDE.md` minimal — point to the two management files; the per-reference descriptions live only in `index.yaml` (and its JP mirror).
