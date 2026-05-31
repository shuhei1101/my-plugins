---
name: dev-kit:py-script
description: >
  Create a simple Python script (single file or a few files, no full project scaffold).
  Trigger when the user asks for a quick script, a one-off automation, or anything that
  does not need pyproject.toml, a package directory, or tests.
  Examples: "write a script that...", "make a quick Python file to...", "スクリプト作って".
  Do NOT trigger for full project creation — use dev-kit:py-project instead.
---

# dev-kit:py-script — Simple Python Script

Create a single-file (or few-file) script that follows dev-kit Python conventions.

---

## Tasks

### Step 1: Load standards

First, read the references index:

```
{plugin_root}/references/python/index.yaml
```

The plugin root is two levels above this skill file (e.g. `Base directory: .../skills/py-script` → plugin root is `.../dev-kit/`).

Read the following for this skill:
- `{plugin_root}/references/python/core/命名規則.md` — naming conventions
- `{plugin_root}/references/python/core/コメント.md` — docstrings and field descriptions
- `{plugin_root}/references/python/core/型ヒント.md` — PEP 695 / type annotations
- `{plugin_root}/references/python/core/言語ルール.md` — Japanese comments / English logs
- `{plugin_root}/references/python/core/スタイル.md` — ruff / line length
- `{plugin_root}/references/python/scripts/Pythonスクリプト.md` — script structure

If a bat launcher is also needed:
- `{plugin_root}/references/python/scripts/launchers-windows.md`

For a UNIX launcher:
- `{plugin_root}/references/python/scripts/ランチャー-Unix.md`

For a tkinter GUI:
- `{plugin_root}/references/python/scripts/Tkinter.md`

→ Proceed to Step 2

---

### Step 2: Clarify requirements

#### Process

1. Confirm the script's purpose if unclear.
2. Identify any third-party packages required.
3. Confirm the output location and filename.
4. Confirm whether a GUI (tkinter) is needed.
5. Confirm whether a launcher (bat / sh) is needed.

→ Proceed to Step 3

---

### Step 3: Write the script

#### Process

1. Create the file following the standard template in `scripts/python-script.md`:
   - Module docstring (line 1 describes what it does)
   - `from __future__ import annotations`
   - Imports in order: standard library → third-party → own modules
   - Constants (`UPPER_SNAKE_CASE`)
   - Logger setup
   - `_parse_args()` for argparse
   - Body functions (e.g. `process(...)`)
   - `main() -> int` to tie everything together
   - `if __name__ == "__main__": sys.exit(main())`
2. Apply type hints everywhere (PEP 695).
3. Declare required packages with `# pip install {package}` comments at the top of the file.
4. Follow `core/naming.md` (snake_case functions, UpperCamel types) and `core/comments.md` (docstrings on exported functions).
5. Use `logger` instead of `print()`. Log messages in **English**.
6. Exception handling: catch expected exceptions; for uncaught ones, leave a full traceback via `logger.exception`.
7. If a launcher is needed, create it at the same time (`scripts/launchers-windows.md` / `scripts/launchers-unix.md`).

→ Done

#### Output

- Script file following dev-kit Python conventions
- bat / sh launcher if required

#### Notes

##### Prohibitions

- Do not create `pyproject.toml` (if needed, use `dev-kit:py-project` for a full project).
- Do not create `shared/` modules such as `logger.py` / `settings.py` / `errors.py` (inline them).
- Do not create a `tests/` folder.
- Do not add unnecessary abstraction for a one-off script (YAGNI).
- Do not write unit tests (overall dev-kit Python policy).

---

## References

See `{plugin_root}/references/python/index.yaml` for details.

Primary references:
- `core/*` — language rules
- `scripts/python-script.md` — script skeleton
- `scripts/launchers-*.md` — launchers
- `scripts/tkinter.md` — when adding a GUI
