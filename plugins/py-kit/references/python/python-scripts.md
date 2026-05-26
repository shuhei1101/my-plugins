# Python Scripts Standards — py-kit

Conventions for standalone scripts, bat launchers, and simple automation.

---

## Simple Script Structure

For single-file scripts that do not need a full project scaffold:

**File header (required):**

```python
"""
{script_name} — {one-line description}

Usage:
  python {script_name}.py [options] {positional_args}
"""
```

**Code structure:**

```python
"""...(header)..."""

# ── stdlib ──────────────────────────────────────────────────
import argparse
from pathlib import Path
from typing import Optional

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
    main(parse_args())
```

No `logger.py`, `config.py`, tests, bat files, setup scripts, or `pyproject.toml`. Document required packages with `# pip install {package}` inline.

---

## Bat Launcher Template

> **Windows only.** Bat files and the rules in this section do not apply to Linux or macOS environments.
> For Linux/macOS, use shell scripts or `Makefile` targets instead.

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

**Rules:**
- Timestamped log filenames are mandatory — never use a fixed name
- All bat file content must be ASCII only — Japanese causes CP932 parse errors in cmd.exe
- Use PowerShell `Get-Date` for timestamps — `wmic` is removed in Windows 11 24H2+

For simultaneous console + log output (long-running commands):

```bat
long_command.exe 2>&1 | powershell -NoProfile -Command "[Console]::InputEncoding=[System.Text.Encoding]::UTF8; $input | ForEach-Object { Write-Host $_; Add-Content -LiteralPath '%BAT_LOG%' -Value $_ -Encoding utf8 }"
```

---

## FastAPI run.bat Template

> **Windows only.** See the Bat Launcher Template note above.

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

Port conventions: reserve a fixed port for the main repo; use fixed-port + 1 or higher for worktree test servers.

---

## GUI (tkinter)

- Action buttons: blue color
- Settings button → opens modal settings dialog
- Settings dialog: all config items editable from GUI; saves to `.env`
- Settings requiring restart: shown in red with "再起動後に適用されます"
- Layout: generate 3 proposals → user selects one
