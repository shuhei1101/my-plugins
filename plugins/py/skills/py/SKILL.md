---
name: py
description: Python project coding standards and conventions. Always apply this skill when writing, reviewing, or modifying any Python code, .py files, .bat launchers, pyproject.toml, or when creating a new Python project structure. Trigger automatically whenever the user works on Python code in this repository — including new projects, scripts, tests, config, bat files, or any implementation task involving Python. These rules take precedence over general Python conventions.
---

# py — Python Project Coding Standards

## Design Principle

Each tool is a **fully independent package** (separate repo / separate project). When tools need to interact, use config or environment variables to specify the other tool's path — no automatic downloads, no shared in-process coupling.

---

## Folder Structure

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
├── gui.bat                     # auto-activates venv
├── {mode}.bat                  # one bat per mode, auto-activates venv
├── setup/
│   ├── setup_venv.bat          # creates venv + installs dependencies end-to-end
│   └── install_{tool}.bat      # for external tools that can't be auto-installed
├── docs/
│   └── install_{tool}.md       # manual install guide (linked from README)
├── tests/
│   ├── mocks/
│   │   ├── mock_env.py
│   │   └── mock_externals.py
│   ├── conftest.py
│   └── {feature}/
│       ├── conftest.py
│       └── test_{feature}.py
├── venv/                       # .gitignore — do not commit
├── resources/                  # GUI assets
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

**Notes:**
- All `.bat` files go in the project root — never in a `bat/` subfolder
- Empty folders (`log/`, `input/`, `output/`, `cache/`) use `.gitkeep` — no README.md inside them
- `main.py` handles only argument dispatch and launch routing — no low-level logic

---

## Config

- Provide both `config.py` and `.env` / `.env.sample`
- `config.py`: define defaults at the top, then load `.env` to override (env wins)
- Priority: env vars (initial load) → overridden by CLI arguments
- Make external library settings configurable via env vars where possible
- If `.env` is absent: auto-copy from `.env.sample` with empty values

---

## Launch Behavior

- No arguments + bat execution → launch GUI
- Arguments present → CLI mode
- `--help` / `-h` → show help
- Multiple modes → one bat file per mode
- `main.py` handles only routing; low-level logic lives in dedicated modules

---

## GUI (tkinter)

- Use tkinter for simple GUIs
- Action buttons: blue color
- Include a Settings button → opens a modal settings dialog
- Settings dialog: all config items editable from GUI; saves changes to `.env`
- Settings that require restart: shown in red with "再起動後に適用されます"
- GUI layout: AI generates 3 proposals → user selects one (per project)

---

## Coding Style

- Use `typing` strictly: `Literal`, `Union`, `Optional`, generics — mirror TypeScript discipline
- Docstrings: reStructuredText format (`:param:`, `:return:`, `:raises:`)
- Comments: add for complex logic, deep nesting, non-obvious expressions, unusual library usage
- Write readable code: use intermediate variables to clarify intent (Readable Code principles)
- Apply design patterns where appropriate (Template, Strategy, etc.) — avoid over-abstraction

---

## Pydantic for API / IO Boundaries

Use Pydantic models (not just type hints) at any system boundary where runtime validation matters:

**Use Pydantic for:**
- External API request bodies and responses
- LLM inputs (structured prompts) and outputs (via Instructor)
- Config file reads (YAML / JSON)
- Data passed between files (CSV / JSONL records)
- User input parsing
- Inter-thread / inter-process event data

**`typing` alone is sufficient for:**
- Function argument / return type hints on internal logic
- `dict` / `list` type expressions that stay within a single function

```python
from pydantic import BaseModel, Field
from typing import Optional

class APIRequest(BaseModel):
    user_id: str
    query: str
    max_results: int = Field(default=10, ge=1, le=100)

class APIResponse(BaseModel):
    status: str
    results: list[dict]
    error: Optional[str] = None

def call_api(req: APIRequest) -> APIResponse:
    response = requests.post(URL, json=req.model_dump())
    return APIResponse(**response.json())
```

---

## Language Rules

**English only** (bat files misrender Japanese):
- All `print()` statements
- All `logger` output (`logger.info()`, `logger.error()`, etc.)

**Japanese allowed:**
- Code comments (docstrings, inline comments)
- `.env.sample` comments
- GUI display strings (tkinter UI text)

```python
# ファイル存在チェックを行う
def check_file_exists(file_path: Path) -> bool:
    """
    ファイルが存在するかチェックする。

    :param file_path: チェック対象のファイルパス
    :return: 存在する場合True
    """
    if not file_path.is_file():
        logger.error(f"File not found: {file_path}")   # English
        return False
    logger.info(f"File exists: {file_path}")            # English
    return True
```

---

## Logger Specification

Every project must include `{package_name}/logger.py` with a `setup_logger()` function.

**Required behavior:**
- `constants.py` defines `LOG_DIR = PROJECT_ROOT / "log"`
- `setup_logger()` calls `LOG_DIR.mkdir(parents=True, exist_ok=True)`
- Log filename: `LOG_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{package_name}.log"` — new file every run, never overwrites
- Attach both `StreamHandler(sys.stdout)` and `FileHandler(..., encoding="utf-8")`
- Format: `[%(asctime)s] %(levelname)s %(name)s %(filename)s:%(lineno)d - %(message)s`
- Guard against duplicate handlers: `if logger.handlers: return logger`
- Log on init: `logger.info("Logger initialized. level=%s, log_file=%s", ...)`
- Submodules: `get_logger(__name__)`

Call `setup_logger()` immediately after entry in `main.py` / `__main__.py`.

---

## .bat Launcher Rules

**Every** generated `.bat` file must follow these rules:

### Structure

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

### Critical Rules

**Timestamped log file names are mandatory.** Never use a fixed name like `run_bat.log` — each run must create a new file. Use the PowerShell snippet above (not `wmic`, which is removed in Windows 11 24H2+).

**ASCII-only content inside .bat files.** Never put Japanese characters (comments, echo strings, labels) in a `.bat` file. `cmd.exe` parses bat files using the system ANSI code page (CP932 on Japanese Windows). Even with `chcp 65001` at the top, the parser itself is not affected — Japanese UTF-8 bytes get misread as CP932 lead bytes and swallow the following command characters, causing cryptic errors like `'etlocal' is not recognized`. Write all comments and echo strings in English. Put Japanese explanations in `README.md`.

**For long-running commands** (PyInstaller builds, model downloads, test runs) where console silence would look like a freeze, use PowerShell pipe for simultaneous console + log output:

```bat
long_command.exe args 2>&1 | powershell -NoProfile -Command "[Console]::InputEncoding=[System.Text.Encoding]::UTF8; $input | ForEach-Object { Write-Host $_; Add-Content -LiteralPath '%BAT_LOG%' -Value $_ -Encoding utf8 }"
```

Why not `Tee-Object`: Windows PowerShell 5.1's `Tee-Object` has no `-Encoding` parameter, causing garbled logs on CP932 systems. The `Write-Host` + `Add-Content` pattern works on PS 5.1 with proper UTF-8 handling.

After a piped command, check for success via output artifact existence (not `%ERRORLEVEL%`, which reflects the PowerShell process, not the original command):

```bat
if not exist "dist\foo.exe" (
    echo [ERROR] build failed. see %BAT_LOG%
    pause
    exit /b 1
)
```

**Short commands** (pip show, venv activation) can use plain `>> "%BAT_LOG%" 2>&1`.

---

## FastAPI / HTTP Server Startup Script

When creating a FastAPI server started via `python -m {package_name}`, always provide a `run.bat`.

**Requirements:**
- Accept an optional port argument: `run.bat [port]`
- Fall back to the `PORT` environment variable, then to the default defined in `__main__.py` / `config.py` (do not hard-code a port in the bat)
- Auto-activate `.venv\Scripts\activate.bat` when present

**Template:**

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

**Port conventions:**
- Reserve a fixed port for the main repo (e.g., 8090); document it in `CLAUDE.md`.
- Use fixed-port + 1 or higher (e.g., 8091+) for worktree test servers.
- To launch from a worktree without a separate venv, use `PYTHONPATH` to point at the worktree's `src/` while invoking the main repo's `.venv\Scripts\python.exe` directly. See the wt skill and the repo's `CLAUDE.md` for details.

---

## Naming Conventions

### Interface / Abstract Base Classes

Choose one pattern per project and use it consistently:

1. `{name}able.py` — preferred for interface-like roles (e.g., `media_convertable.py`)
2. `i_{name}.py` — Interface prefix (e.g., `i_converter.py`)
3. `base_{name}.py` — Abstract base class (e.g., `base_converter.py`)
4. `{name}.py` — Simple naming when intent is clear

### Implementation Classes

`{implementation}_{name}.py` — e.g., `ffmpeg_converter.py`, `file_logger.py`

---

## Tests

- Use pytest
- Write integration tests only — no unit tests for individual methods
- Mock external APIs and external libraries
- Mock environment variables too (use `mock_env.py`)
- Reusable mocks go in `tests/mocks/` — never recreate them per test file
- Test folder mirrors the source folder structure

---

## Packaging

- Use `pyproject.toml`
- Python `>= 3.11`
- Pin dependencies with `~=` (compatible release)

---

## Setup Scripts

All setup scripts go in `setup/`:

- `setup_venv.bat`: creates venv + installs all dependencies in one shot (assume Python is already installed)
- `install_{tool}.bat`: for external tools installable via `winget` / `choco` — actually runs the install, doesn't just document it
- For tools requiring manual steps (license agreements, manual DL): create `docs/install_{tool}.md` and link from README

**Forbidden:**
- `install_python.bat` that only prints instructions without installing
- `install_dependencies.bat` for global environments
- Any bat that tells the user to "manually run something" without providing a working script

---

## .gitignore

Always include:
```
.env
__pycache__/
*.pyc
venv/
.venv/
log/
cache/
```

---

## Technology Selection

When choosing libraries or frameworks, use MCP (context7) or web search to check for the latest stable versions and any breaking changes before deciding.

---

## Simple Script Rules

For scripts that fit in a single `.py` file:

### File Header (required)

```python
"""
{script_name} — {one-line description of what it does}

Usage:
  python {script_name}.py [options] {positional_args}

  # Explain arguments / options here
"""
```

### Code Structure

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
    """
    補助処理。

    :param value: 処理対象
    :return: 処理結果
    """
    return value.strip()

# ── main ────────────────────────────────────────────────────
def main(args: argparse.Namespace) -> None:
    """メイン処理。:param args: コマンドライン引数"""
    ...

def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する。:return: 解析済み引数"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(args)
```

**Differences from full package:**
- No `logger.py` — use `print()` or `logging.basicConfig()` for simple output
- No `config.py` / `.env` — manage settings via arguments or constants
- No tests, bat files, setup scripts, or `pyproject.toml`
- Document required third-party packages with `# pip install {package}` comments

---

## Project Rule Deployment

This skill ships with a rule template at `rules/implementation.md` (sibling of this SKILL.md).

**On first use in a project**, check if `.claude/rules/implementation.md` exists. If not, create it:

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
