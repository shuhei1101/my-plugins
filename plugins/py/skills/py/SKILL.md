---
name: py
description: Python project coding standards and conventions. Always apply this skill when writing, reviewing, or modifying any Python code, .py files, .bat launchers, pyproject.toml, or when creating a new Python project structure. Trigger automatically whenever the user works on Python code in this repository — including new projects, scripts, tests, config, bat files, or any implementation task involving Python. These rules take precedence over general Python conventions.
---

# py — Python Project Coding Standards

Provides the standards and conventions to follow whenever writing Python code for this project.

---

## Overview

Each tool is a **fully independent package** (separate repo / separate project). When tools need to interact, use config or environment variables to specify the other tool's path — no automatic downloads, no shared in-process coupling.

---

## Tasks

### Step 1: Check context before coding

#### Condition

- Always — before writing any Python code or creating files

#### Process

1. Determine the project type:
   - **New project** → proceed to Step 2 to set up the scaffold
   - **Existing project** → read the existing folder structure, then proceed to Step 3
2. If creating a **simple single-file script** (not a full package) → skip to References → Simple Script Rules

→ Proceed to Step 2 (new project) or Step 3 (existing project or simple script)

#### Output

- Context understood: new project, existing project, or simple script

---

### Step 2: Set up project scaffold

#### Condition

- New Python project being created from scratch

#### Input

- Project / package name

#### Process

1. Create the folder structure (see References → Folder Structure for the full tree).
2. Create `pyproject.toml` with Python `>= 3.11` and dependencies pinned with `~=`.
3. Create `.gitignore` including at minimum: `.env`, `__pycache__/`, `*.pyc`, `venv/`, `.venv/`, `log/`, `cache/`.
4. Create `.env.sample` with placeholder values for all required environment variables.
5. Create `setup/setup_venv.bat` — creates venv and installs all dependencies in one shot.
6. Create `activate.bat` for convenience.
7. Add `.gitkeep` files to empty folders (`log/`, `input/`, `output/`, `cache/`).

→ Proceed to Step 3

#### Output

- Project scaffold created with all required files and directories

#### Notes

##### Prohibitions

- Do not create a `bat/` subfolder — all `.bat` files go in the project root
- Do not put README.md inside empty folders — use `.gitkeep` only

---

### Step 3: Write Python code

#### Condition

- Writing or modifying Python source files (`.py`)

#### Input

- Task description and target file(s)

#### Process

1. Apply typing strictly — use `Literal`, `Union`, `Optional`, generics (mirror TypeScript discipline).
2. Use docstrings in reStructuredText format (`:param:`, `:return:`, `:raises:`).
3. Use Pydantic models (not just type hints) at any system boundary where runtime validation matters (see References → Pydantic Boundaries for the full list).
4. Follow language rules:
   - **English only**: all `print()` and `logger` output
   - **Japanese allowed**: code comments, `.env.sample` comments, GUI display strings
5. Ensure the logger is set up correctly (see References → Logger Specification).
6. Apply design patterns where appropriate (Template, Strategy, etc.) — avoid over-abstraction.
7. Write readable code: use intermediate variables to clarify intent.

→ Proceed to Step 4 if bat launchers are needed, otherwise done

#### Output

- Python code written following project conventions

#### Notes

##### Prohibitions

- Do not write Japanese in `print()` or `logger` calls — bat files misrender Japanese
- Do not use `wmic` in bat files — removed in Windows 11 24H2+; use the PowerShell timestamp snippet instead

---

### Step 4: Create bat launchers

#### Condition

- Creating a `.bat` launch script for the project

#### Input

- Package name and launch mode

#### Process

1. Use the bat template from References → Bat Launcher Template.
2. Key requirements:
   - Timestamped log file names are **mandatory** — never use a fixed name like `run_bat.log`
   - All content inside `.bat` files must be **ASCII only** — never put Japanese in comments, echo strings, or labels
   - Use the PowerShell `Get-Date` snippet for timestamps (not `wmic`)
3. For FastAPI / HTTP servers: use the run.bat template from References → FastAPI run.bat Template.
4. For long-running commands: use the PowerShell pipe pattern for simultaneous console + log output.

→ Done

#### Output

- `.bat` launcher created following all rules

#### Notes

##### Why ASCII-only in bat files

`cmd.exe` parses bat files using the system ANSI code page (CP932 on Japanese Windows). Even with `chcp 65001` at the top, the parser itself is not affected. Japanese UTF-8 bytes get misread as CP932 lead bytes and swallow the following command characters, causing cryptic errors like `'etlocal' is not recognized`. Put all explanations in `README.md`.

---

### Step 5: Write tests

#### Condition

- Writing tests for the project

#### Input

- Feature or module to test

#### Process

1. Use pytest.
2. Write integration tests only — no unit tests for individual methods.
3. Mock external APIs and external libraries.
4. Mock environment variables too — use `mock_env.py`.
5. Put reusable mocks in `tests/mocks/` — never recreate them per test file.
6. Mirror the source folder structure in the test folder.

→ Done

#### Output

- Tests created following project conventions

---

### Step 6: Deploy project rule

#### Condition

- First time using this skill in a project

#### Process

1. Check: `Glob(".claude/rules/implementation.md")` in the project root.
2. If missing, create `.claude/rules/implementation.md` with this content:

```markdown
---
paths:
  - "src/**/*.py"
---

# Implementation Work

## Before writing code

1. Confirm the spec exists in `wiki/`. If the relevant wiki doc is missing or contradicts the request, stop and surface that to the user.
2. If open Issues touch this area (`wiki/Issues.md`), notify the user before proceeding.
3. Read the `/py:py` skill before writing Python code.

## Pre-commit checklist

- [ ] Code / config files changed
- [ ] `docs/PR/PR{N}.md` created or updated
- [ ] Wiki documents updated if the implementation changes documented behavior
- [ ] `.gitignore` updated if new file types or directories were added
- [ ] New design decisions recorded in `wiki/Issues.md` or the relevant feature doc
```

3. Create `.claude/rules-jp/implementation.md` as a stub:

```markdown
> **このファイルは日本語ミラーです。本体は `.claude/rules/implementation.md`。**
```

4. Commit: `git add .claude/rules/ && git commit -m "chore: add implementation rule"`

→ Done

#### Output

- `.claude/rules/implementation.md` created and committed

---

## References

### Folder Structure

```
{package-name}/
├── {package_name}/
│   ├── {feature_subfolder}/    # split by feature
│   ├── __init__.py
│   ├── __main__.py             # entry point for: python -m {package_name}
│   ├── config.py
│   ├── main.py                 # argument handling + launch branching only (high-level)
│   ├── gui.py                  # tkinter GUI
│   ├── cli.py                  # argparse handling
│   ├── logger.py               # logger initialization
│   ├── exceptions.py           # custom exception classes
│   ├── constants.py            # constants (LOG_DIR, PROJECT_ROOT, etc.)
│   └── utils.py or common/     # shared utilities
├── gui.bat
├── {mode}.bat                  # one bat per mode
├── setup/
│   ├── setup_venv.bat
│   └── install_{tool}.bat
├── docs/
│   └── install_{tool}.md
├── tests/
│   ├── mocks/
│   │   ├── mock_env.py
│   │   └── mock_externals.py
│   ├── conftest.py
│   └── {feature}/
│       ├── conftest.py
│       └── test_{feature}.py
├── venv/                       # .gitignore
├── resources/
├── log/                        # .gitkeep
├── input/                      # .gitkeep (optional)
├── output/                     # .gitkeep (optional)
├── cache/                      # .gitkeep (optional)
├── activate.bat
├── .env.sample
├── .gitignore
├── README.md
└── pyproject.toml
```

### Pydantic Boundaries

Use Pydantic models (not just type hints) at system boundaries where runtime validation matters:

**Use Pydantic for:** External API request bodies and responses, LLM inputs and outputs (via Instructor), config file reads (YAML / JSON), data passed between files (CSV / JSONL records), user input parsing, inter-thread / inter-process event data.

**`typing` alone is sufficient for:** Function argument / return type hints on internal logic, `dict` / `list` expressions that stay within a single function.

### Logger Specification

Every project must include `{package_name}/logger.py` with a `setup_logger()` function:

- `constants.py` defines `LOG_DIR = PROJECT_ROOT / "log"`
- `setup_logger()` calls `LOG_DIR.mkdir(parents=True, exist_ok=True)`
- Log filename: `LOG_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{package_name}.log"` — new file every run
- Attach both `StreamHandler(sys.stdout)` and `FileHandler(..., encoding="utf-8")`
- Format: `[%(asctime)s] %(levelname)s %(name)s %(filename)s:%(lineno)d - %(message)s`
- Guard against duplicate handlers: `if logger.handlers: return logger`
- Submodules: `get_logger(__name__)`

Call `setup_logger()` immediately after entry in `main.py` / `__main__.py`.

### Bat Launcher Template

```bat
@echo off
chcp 65001 > nul
setlocal

set "LOG_DIR=%~dp0log"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMddHHmmss"') do set "TS=%%I"
set "BAT_LOG=%LOG_DIR%\%TS%_run_bat.log"

echo [%date% %time%] Starting >> "%BAT_LOG%"
echo [%date% %time%] CWD: %cd% >> "%BAT_LOG%"

if exist "%~dp0venv\Scripts\activate.bat" (
    call "%~dp0venv\Scripts\activate.bat" >> "%BAT_LOG%" 2>&1
)

python -m {package_name} %* >> "%BAT_LOG%" 2>&1
set "EXITCODE=%ERRORLEVEL%"

if %EXITCODE% neq 0 (
    echo [ERROR] Exit code %EXITCODE%. See: %BAT_LOG%
    pause
)

endlocal & exit /b %EXITCODE%
```

For long-running commands, use PowerShell pipe for simultaneous console + log output:

```bat
long_command.exe args 2>&1 | powershell -NoProfile -Command "[Console]::InputEncoding=[System.Text.Encoding]::UTF8; $input | ForEach-Object { Write-Host $_; Add-Content -LiteralPath '%BAT_LOG%' -Value $_ -Encoding utf8 }"
```

After a piped command, check success via output artifact existence (not `%ERRORLEVEL%`):

```bat
if not exist "dist\foo.exe" (
    echo [ERROR] build failed. see %BAT_LOG%
    pause
    exit /b 1
)
```

### FastAPI run.bat Template

```bat
@echo off
chcp 65001 > nul
setlocal

set "LOG_DIR=%~dp0log"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMddHHmmss"') do set "TS=%%I"
set "BAT_LOG=%LOG_DIR%\%TS%_run.log"

if not "%1"=="" set "PORT=%1"

echo [%date% %time%] Starting. PORT=%PORT% >> "%BAT_LOG%"
echo [%date% %time%] CWD: %cd% >> "%BAT_LOG%"

if exist "%~dp0.venv\Scripts\activate.bat" (
    call "%~dp0.venv\Scripts\activate.bat" >> "%BAT_LOG%" 2>&1
)

python -m {package_name} >> "%BAT_LOG%" 2>&1
set "EXITCODE=%ERRORLEVEL%"

if %EXITCODE% neq 0 (
    echo [ERROR] Exit code %EXITCODE%. See: %BAT_LOG%
    pause
)

endlocal & exit /b %EXITCODE%
```

Port conventions: reserve a fixed port for the main repo; use fixed-port + 1 or higher for worktree test servers.

### Simple Script Rules

For scripts that fit in a single `.py` file:

**File header (required):**

```python
"""
{script_name} — {one-line description of what it does}

Usage:
  python {script_name}.py [options] {positional_args}

  # Explain arguments / options here
"""
```

**Code structure:**

```python
"""...(header docstring)..."""

# ── stdlib ──────────────────────────────────────────────────
import argparse
import sys
from pathlib import Path
from typing import Literal, Optional

# ── third-party ─────────────────────────────────────────────
import some_lib  # pip install some_lib

# ── constants ───────────────────────────────────────────────
SOME_CONSTANT: str = "value"

# ── private helpers ─────────────────────────────────────────
def _helper(value: str) -> str:
    return value.strip()

# ── main ────────────────────────────────────────────────────
def main(args: argparse.Namespace) -> None:
    ...

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(args)
```

Differences from full package: no `logger.py`, no `config.py`/`.env`, no tests/bat/setup/`pyproject.toml`. Document required third-party packages with `# pip install {package}` comments.

### Naming Conventions

**Interface / Abstract Base Classes** — choose one pattern per project:
1. `{name}able.py` — preferred (e.g., `media_convertable.py`)
2. `i_{name}.py` — Interface prefix (e.g., `i_converter.py`)
3. `base_{name}.py` — Abstract base class (e.g., `base_converter.py`)

**Implementation classes:** `{implementation}_{name}.py` (e.g., `ffmpeg_converter.py`)

### GUI (tkinter)

- Action buttons: blue color
- Include a Settings button → opens a modal settings dialog
- Settings dialog: all config items editable from GUI; saves changes to `.env`
- Settings that require restart: shown in red with "再起動後に適用されます"
- GUI layout: AI generates 3 proposals → user selects one (per project)
