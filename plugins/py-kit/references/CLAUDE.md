# py-kit references — index

The py-kit Python conventions are split into **topic-axis reference files**.
You only read the ones relevant to your current edit.

| File | Role |
|---|---|
| **`index.yaml`** (English) / **`index.jp.yaml`** (Japanese mirror) | Reference list + one-line `description`. The refs-inject-kit hook parses the English version (Japanese version is used when `REFS_INJECT_KIT_LANG=jp`). |

Injection rules — which file-path patterns inject which references — are **not in py-kit**. They live in **`refs-inject-kit/injection_rules.yaml`** and reference py-kit content using the `${py-kit}/path/to/ref.md` placeholder syntax.

---

## Reading manually

1. Read **`index.yaml`** to see what each reference covers.
2. To know which references apply to a given file path, see `refs-inject-kit/injection_rules.yaml` (the rules whose `pattern` matches the edit target).

---

## Reading automatically

The **`refs-inject-kit` plugin** (separate plugin, PR140) does this on every `Edit` / `Write` / `MultiEdit`:

1. Reads its own central `injection_rules.yaml`
2. Matches the edit target against `rules[].pattern` and collects `${plugin-name}/path` references
3. Resolves `${py-kit}` to py-kit's installed `references/` directory
4. Looks up each reference's description from py-kit's `index.yaml`
5. Reads each reference body
6. Renders the Jinja2 template and injects via `decision: block`

A session + file-hash token prevents the hook from blocking the same file twice in one session.

Switch the injection language by setting `REFS_INJECT_KIT_LANG=jp` (default is `en`).

---

## Used by SKILLs

`py-kit:py-project` and `py-kit:py-script` both read `index.yaml` first in their Step 1.
Skill-specific behavior (e.g. `py-script` force-loading `scripts/python-script.md`) is encoded in the SKILL file itself.

---

## Maintenance

- When adding a new reference: update **`index.yaml`** and **`index.jp.yaml`** in py-kit, and **add a rule in `refs-inject-kit/injection_rules.yaml`** using the `${py-kit}/...` syntax.
- Same for deletes / renames.
- Keep `references/CLAUDE.md` minimal — the per-reference descriptions live only in `index.yaml` (and its JP mirror).
