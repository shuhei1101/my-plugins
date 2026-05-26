---
name: py-kit:py-script
description: >
  Create a simple Python script (single file or a few files, no full project scaffold).
  Trigger when the user asks for a quick script, a one-off automation, or anything that
  does not need pyproject.toml, a package directory, or tests.
  Examples: "write a script that...", "make a quick Python file to...", "スクリプト作って".
  Do NOT trigger for full project creation — use py-kit:py-project instead.
---

# py-kit:py-script — Simple Python Script

Creates a clean, standards-compliant single-file Python script.

---

## Tasks

### Step 1: Load standards

Read the index file to identify which references to load:

```
{plugin_root}/references/_index.md
```

The plugin root is two levels above this skill file (e.g. `Base directory: .../skills/py-script` → plugin root is `.../{plugin-name}/`).

Then read:
- `{plugin_root}/references/python-core.md` — naming, type hints, comment rules, language rules
- `{plugin_root}/references/python-scripts.md` — simple script structure

→ Proceed to Step 2

---

### Step 2: Clarify requirements

#### Process

1. Confirm what the script should do if not already clear.
2. Identify required third-party packages (if any).
3. Confirm the output location and filename.

→ Proceed to Step 3

---

### Step 3: Write the script

#### Process

1. Use the Simple Script Structure from `python-scripts.md` (file header docstring → stdlib imports → third-party → constants → private helpers → `main()` → `parse_args()` → `if __name__ == "__main__"`).
2. Apply type hints everywhere.
3. Document required packages with `# pip install {package}` inline comments.
4. Apply naming conventions and comment rules from `python-core.md`.
5. Write `print()` / log output in English only.

→ Done

#### Output

- Script file created following py-kit standards

#### Notes

##### Prohibitions

- Do not create `pyproject.toml`, `logger.py`, `config.py`, bat files, setup scripts, or a tests folder — those belong in a full project
- Do not add unnecessary abstraction for a one-off script

---

## References

- `{plugin_root}/references/python-core.md` — Naming Conventions, Type Hints, Comment Rules, Language Rules
- `{plugin_root}/references/python-scripts.md` — Simple Script Structure
