# py-kit References — Index

py-kit's Python conventions are organized as **multiple reference files split along topical axes**.
Metadata and injection rules are consolidated in `index.yaml` so that only the necessary files
need to be read depending on what is being edited.

---

## File to read first

**`plugins/py-kit/references/index.yaml`**

This file contains:
- `path` and a one-line `description` for every reference
- `injection_rules` (star chart) keyed by the file path being edited

---

## How to read (manual case)

1. **Read `index.yaml`**
2. **Match the path of the file you are editing against the `pattern` entries in `injection_rules`**
   - Example: editing `src/{pkg}/features/chat/service.py` → both `**/*.py` and `**/features/**/service.py` match
3. **Read all of the matched rule's `required` items, plus relevant items from `optional` as needed**
4. If something feels missing, look at the `description` of each entry in `references` and pull in any file that looks applicable

---

## How to read (automatic case)

The **PreToolUse hook** to be implemented in the next PR `add-py-kit-references-injection-hook`
automatically evaluates `injection_rules` against the file path being edited
and injects the necessary references into Claude via `decision: block`.

Once that hook is in place, the required references will automatically flow into the context
every time the user invokes `Edit` / `Write`, so Claude no longer needs to read `index.yaml` itself each time.

---

## Invocation from SKILLs

Step 1 of each of `py-kit:py-project` / `py-kit:py-script` instructs reading
this directory's `index.yaml` first.
Skill-specific scenarios (e.g. force-injecting `scripts/python-script.md` for `py-script`)
are written on the SKILL.md side.

---

## Maintenance

- When adding a new reference, always update both `references:` and `injection_rules:` in `index.yaml`
- Update `index.yaml` likewise when deleting or renaming files
- As a rule, write nothing in `references/CLAUDE.md` other than "read `index.yaml`"
  (per-reference explanations are consolidated in the `description` field within `index.yaml`)
