# Python Scripts Standards — py-kit

Conventions for standalone scripts, bat launchers, and simple automation.
Read together with `python-core.md`. This file applies to:

- Single-file Python scripts (no `pyproject.toml`, no package directory)
- Windows `.bat` launchers (any project)
- FastAPI `run.bat` shortcut launchers
- tkinter GUI quick prototypes

Do **not** apply this file to full projects — those follow `python-architecture.md`.

---

## 1. Simple Script Structure

A simple script is a single `.py` file that does one job and exits. Examples:
"convert this CSV", "scrape this page once", "regenerate this report".

### 1.1 Required File Header

Every script starts with a docstring of at least three lines:

```python
"""
{script_name} — {one-line purpose}

Usage:
  python {script_name}.py [options] {positional_args}
"""
```

The `argparse.ArgumentParser` reuses this as `description=__doc__`, so the
`--help` output stays consistent with the file header.

### 1.2 Section Markers

Use horizontal-rule comments to delimit the four logical regions of the file.
Exact format (Unicode box drawing characters allowed in comments, not output):

```python
"""...(header)..."""

# ── stdlib ──────────────────────────────────────────────────
import argparse
import logging
from pathlib import Path
from typing import Optional

# ── third-party ─────────────────────────────────────────────
import httpx           # pip install httpx
from pydantic import BaseModel  # pip install pydantic

# ── constants ───────────────────────────────────────────────
DEFAULT_TIMEOUT: float = 30.0
USER_AGENT: str = "py-kit-script/1.0"

# ── private helpers ─────────────────────────────────────────
def _slugify(value: str) -> str:
    return value.strip().lower().replace(" ", "-")

# ── main ────────────────────────────────────────────────────
def main(args: argparse.Namespace) -> int:
    """Return the exit code; 0 on success, non-zero on error."""
    ...
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", type=Path, help="input file")
    parser.add_argument("--out", type=Path, default=Path("out.csv"), help="output file")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="request timeout in seconds")
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main(parse_args()))
```

### 1.3 Section Order Is Fixed

| Region | Contains | Why this order |
|---|---|---|
| Header docstring | name, purpose, usage | Read by `argparse` |
| stdlib imports | only stdlib modules | Resolves first, has no third-party requirement |
| third-party imports | third-party modules, with `# pip install` comment | Caller can see what to install before running |
| constants | module-level `UPPER_SNAKE_CASE` constants with type annotations | Visible before any function reads them |
| private helpers | `_helper()` functions with leading underscore | Used by `main()` |
| main + parse_args | the entry point | At the bottom — easiest to find |

Do not reorder these regions.

### 1.4 `# pip install` Comment Is Required

Every third-party import carries an inline `# pip install {package}` comment so
the script is runnable from a fresh interpreter without external documentation.

```python
# ✅ Good
import httpx       # pip install httpx
from pydantic import BaseModel  # pip install pydantic

# ❌ Bad — caller must guess
import httpx
from pydantic import BaseModel
```

For modules that are part of the stdlib (`json`, `pathlib`, `typing`), no comment.

### 1.5 `main()` Returns the Exit Code

`main()` returns an `int`. Use `sys.exit(main(parse_args()))` to wire the exit
code back to the shell so bat launchers can branch on `%ERRORLEVEL%`.

```python
# ✅ Good
def main(args: argparse.Namespace) -> int:
    if not args.input.exists():
        print(f"Input file not found: {args.input}", file=sys.stderr)
        return 1
    process(args.input, args.out)
    return 0

if __name__ == "__main__":
    sys.exit(main(parse_args()))
```

```python
# ❌ Bad — no exit code propagation
def main(args):
    process(...)

if __name__ == "__main__":
    main(parse_args())
```

### 1.6 What a Simple Script Must NOT Contain

A script is "simple" by virtue of NOT having these things. If it grows them, it
has become a project — graduate it to a `pyproject.toml`-backed package and
apply `python-architecture.md` instead.

| Forbidden in a simple script | Reason |
|---|---|
| `pyproject.toml` | That's a project |
| `logger.py` | One file should not import another `.py` file in this folder; use stdlib `logging.basicConfig()` inline |
| Separate `config.py` | Use constants and CLI args |
| Bat launchers | Run with `python script.py` directly |
| `setup/setup_venv.bat` | Tell the user to `pip install` the modules listed in the comments |
| A `tests/` folder | If it needs tests, it's a project |
| Multiple files | A "simple script" is one file |

If you reach for any of these, stop and ask: "is this really a script?" Most "scripts" that grow these features should have been projects from the start.

### 1.7 argparse Patterns

#### 1.7.1 Standard Pattern

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", type=Path, help="input CSV file")
    parser.add_argument("--out", type=Path, default=Path("out.csv"), help="output CSV file")
    parser.add_argument("--dry-run", action="store_true", help="do not write output")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity (-v, -vv)")
    return parser.parse_args()
```

#### 1.7.2 Subcommands

When a script grows multiple modes, use subparsers; do not pass a `--mode` string.

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="run the job")
    p_run.add_argument("input", type=Path)

    p_validate = sub.add_parser("validate", help="validate input without running")
    p_validate.add_argument("input", type=Path)

    return parser.parse_args()


def main(args: argparse.Namespace) -> int:
    match args.command:
        case "run":      return run(args.input)
        case "validate": return validate(args.input)
        case _:          return 2
```

#### 1.7.3 Verbosity Flag → Logging Level

```python
def main(args: argparse.Namespace) -> int:
    level = logging.WARNING - 10 * args.verbose  # -v=INFO, -vv=DEBUG
    logging.basicConfig(level=max(level, logging.DEBUG), format="[%(levelname)s] %(message)s")
    ...
```

### 1.8 Logging in Simple Scripts

Use `logging.basicConfig()` inline — do not introduce a `logger.py` file.

```python
import logging

def main(args: argparse.Namespace) -> int:
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
    logger = logging.getLogger(__name__)
    logger.info("Starting %s", args.input)
    ...
```

For longer-running scripts that need a log file, projects are the right tool — see `python-testing.md` Logger Specification.

### 1.9 Error Handling in Simple Scripts

Exit codes:

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Operational failure (missing input file, network error, etc.) |
| 2 | User error (bad CLI args — argparse exits 2 automatically) |
| 130 | Interrupted by user (Ctrl+C) — handle `KeyboardInterrupt` explicitly if cleanup is needed |

```python
def main(args: argparse.Namespace) -> int:
    try:
        process(args.input, args.out)
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}", file=sys.stderr)
        return 1
    except httpx.HTTPError as e:
        print(f"Network error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        return 130
    return 0
```

### 1.10 Output Conventions

| Output | Where it goes |
|---|---|
| Normal status (`Starting...`, progress) | `stdout` via `logger.info` |
| Errors / warnings | `stderr` via `print(..., file=sys.stderr)` or `logger.error` |
| Machine-readable result (JSON, CSV) | `stdout` if piping is intended; otherwise to `--out` file |

If a script may be piped, log status to `stderr` so `stdout` stays clean for the consumer.

---

## 2. Bat Launcher Template — Windows Only

> **Windows only.** Bat files and the rules in this section do not apply to
> Linux or macOS. On those platforms, use shell scripts or `Makefile` targets.

### 2.1 Why Bat Launchers Exist

Windows users double-click `run.bat` to start a program; they cannot be expected
to open a venv shell. The bat launcher handles:

1. Setting up the working directory (`%~dp0`)
2. Activating the virtualenv
3. Logging stdout / stderr to a timestamped file
4. Pausing on error so the user can read the message

### 2.2 Standard Template

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

### 2.3 Bat Rules (Hard)

| Rule | Reason |
|---|---|
| `chcp 65001 > nul` at the very top | Force UTF-8 console; otherwise CP932 corrupts Japanese filenames in paths |
| All bat content is ASCII only — no Japanese | `cmd.exe` parses bat files in CP932; Japanese causes "is not recognized as an internal or external command" errors |
| Timestamped log filename via PowerShell `Get-Date` | `wmic` was removed in Windows 11 24H2+; only PowerShell is reliable |
| Log filename: `YYYYMMDDHHMMSS_{purpose}.log` | Sortable; never overwritten |
| Use `%~dp0` for paths, not `%cd%` | `%cd%` depends on how the user launched the bat |
| `setlocal` / `endlocal` for env var isolation | Otherwise leaks into parent shell |
| `pause` only on error, never on success | Successful runs should exit cleanly |
| Propagate `%ERRORLEVEL%` via `exit /b` | Lets CI / chained bats branch on success |
| `> "%BAT_LOG%" 2>&1` | Captures both stdout and stderr |

### 2.4 Bat Forbidden Patterns

```bat
:: ❌ Bad — Japanese in bat file
echo 開始しました

:: ❌ Bad — wmic (removed in Win11 24H2+)
for /f %%I in ('wmic os get LocalDateTime ^| find "."') do set TS=%%I

:: ❌ Bad — no chcp; bat runs in CP932
@echo off
:: (rest of file)

:: ❌ Bad — pause on success
python -m mypkg
pause

:: ❌ Bad — does not propagate exit code
python -m mypkg
exit /b 0
```

### 2.5 Simultaneous Console + Log Output

For long-running commands where the user wants to see progress in real time AND have it logged:

```bat
long_command.exe 2>&1 | powershell -NoProfile -Command "[Console]::InputEncoding=[System.Text.Encoding]::UTF8; $input | ForEach-Object { Write-Host $_; Add-Content -LiteralPath '%BAT_LOG%' -Value $_ -Encoding utf8 }"
```

This is slower than redirect-only logging (every line goes through PowerShell), so use it only when the user genuinely needs both streams.

---

## 3. FastAPI run.bat Template — Windows Only

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

### 3.1 Port Conventions

| Environment | Port |
|---|---|
| Main repository, dev mode | A fixed port reserved for this project (e.g. `8000`) |
| Worktree test server (e.g. PR review) | Main port + 1, + 2, ... (e.g. `8001`, `8002`) |
| Tests (e2e using a live server) | A high random port (`>30000`) selected per test run |

Document the project's fixed port in the project `CLAUDE.md`.

### 3.2 Run via `python -m`, Not `uvicorn` Directly

Make `__main__.py` the canonical entry, with `uvicorn` invoked from inside:

```python
# {package_name}/__main__.py
import uvicorn
from {package_name}.config import Settings

def run() -> None:
    settings = Settings.from_env()
    uvicorn.run(
        f"{__package__}.main:app",
        host="0.0.0.0",
        port=settings.port,
        log_config=None,  # use our logger.py setup
        access_log=False, # we log requests in middleware
    )

if __name__ == "__main__":
    run()
```

This avoids two parallel ways to start the app and lets the bat launcher call `python -m {package_name}` uniformly.

---

## 4. tkinter GUI Quick Prototype

For small GUI tools that don't justify a full project layout:

### 4.1 Style Rules

| Element | Convention |
|---|---|
| Action buttons | Blue color |
| Settings button | Opens a modal Settings dialog |
| Settings dialog | All config items editable from GUI; saves to `.env` |
| Settings requiring restart | Shown in red with "再起動後に適用されます" label |
| Layout | Generate 3 proposals → user picks one |

### 4.2 Minimal tkinter Skeleton

```python
"""
{tool_name} — {one-line purpose}

Usage:
  python {tool_name}.py
"""

# ── stdlib ──────────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk, messagebox

# ── constants ───────────────────────────────────────────────
TITLE: str = "..."
WINDOW_SIZE: str = "640x480"

# ── private helpers ─────────────────────────────────────────
def _open_settings(root: tk.Tk) -> None:
    ...

# ── main ────────────────────────────────────────────────────
def main() -> int:
    root = tk.Tk()
    root.title(TITLE)
    root.geometry(WINDOW_SIZE)

    action = ttk.Button(root, text="実行", command=lambda: _run(root))
    action.configure(style="Accent.TButton")  # blue
    action.pack(pady=20)

    settings = ttk.Button(root, text="設定", command=lambda: _open_settings(root))
    settings.pack()

    root.mainloop()
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

For anything beyond a quick prototype, graduate to a project and put GUI code under `interface/gui/`.

---

## 5. Linux / macOS Equivalent

When bat files don't apply (Linux, macOS, CI), use a shell script wrapper:

```bash
#!/usr/bin/env bash
# run.sh — {one-line purpose}
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/log"
mkdir -p "${LOG_DIR}"
TS="$(date +%Y%m%d%H%M%S)"
LOG_FILE="${LOG_DIR}/${TS}_run.log"

if [[ -f "${SCRIPT_DIR}/.venv/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source "${SCRIPT_DIR}/.venv/bin/activate"
fi

python -m {package_name} "$@" 2>&1 | tee "${LOG_FILE}"
```

| Rule | Reason |
|---|---|
| `set -euo pipefail` at the top | Fail fast on errors / undefined vars / pipe failures |
| `"$(cd ... && pwd)"` for `SCRIPT_DIR` | Resolves symlinks; works regardless of how called |
| `tee` for console + log | Linux equivalent of the PowerShell trick |

---

## 6. Definition of Done — Scripts Checklist

For a "simple script":

- [ ] Three-line header docstring (name, purpose, usage)
- [ ] Section markers in the correct order (stdlib / third-party / constants / helpers / main)
- [ ] Every third-party import has a `# pip install {package}` comment
- [ ] `main()` returns an `int` exit code
- [ ] `sys.exit(main(parse_args()))` at the bottom
- [ ] No `logger.py`, no `config.py`, no extra files
- [ ] All `print()` / logger output is English (per `python-core.md` § 6.1)
- [ ] Type hints on all signatures (per `python-core.md` § 3.1)
- [ ] Errors map to documented exit codes (§ 1.9)

For a bat launcher:

- [ ] `chcp 65001 > nul` at the top
- [ ] No Japanese anywhere in the file
- [ ] PowerShell-based timestamp (no `wmic`)
- [ ] Log written to `log/YYYYMMDDHHMMSS_*.log`
- [ ] `setlocal` / `endlocal` to isolate env vars
- [ ] `pause` only on error
- [ ] `exit /b %EXITCODE%` to propagate the code
