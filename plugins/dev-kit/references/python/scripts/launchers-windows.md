# launchers-windows — bat launcher

Conventions for `.bat` files that launch Python scripts on Windows.

---

## Standard template

```bat
@echo off
chcp 65001 > nul
setlocal

:: ----- cd into this script's directory -----
cd /d "%~dp0"

:: ----- activate venv if present -----
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

:: ----- timestamp (YYYYMMDD-HHMMSS) via PowerShell (locale-independent) -----
for /f "delims=" %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set TS=%%i

:: ----- log directory -----
if not exist log mkdir log
set LOG=log\script-%TS%.log

:: ----- run -----
python script.py %* > "%LOG%" 2>&1
set EXIT_CODE=%ERRORLEVEL%

:: ----- show result -----
type "%LOG%"
echo.
echo (log: %LOG%)
echo (exit: %EXIT_CODE%)

endlocal & exit /b %EXIT_CODE%
```

> Comments inside the bat (`::`) are all English too. See the later "Do not write Japanese inside bat files" section for the reason.

---

## Required elements

| Element | Reason |
|---|---|
| `@echo off` | suppress echoing commands themselves |
| `chcp 65001 > nul` | avoid UTF-8 garbling |
| `setlocal` ... `endlocal` | avoid environment variable pollution |
| `cd /d "%~dp0"` | base on where the bat is located |
| `.venv\Scripts\activate.bat` (with existence check) | auto-activate venv |
| **PowerShell-based timestamp** | `%time%` is locale-dependent (mixing `9:30` and `09:30`); PowerShell is safe |
| ensure `log\` directory | log output destination |
| `> "%LOG%" 2>&1` | route both stdout / stderr to the log |
| `type "%LOG%"` | also show on screen after execution |
| `exit /b %EXIT_CODE%` | propagate Python's exit code to the caller |

---

## Timestamp generation: why PowerShell

`%date%` and `%time%` change format depending on Windows locale settings:
- `2026/05/28 ` / `2026-05-28` / `05/28/2026` …
- `9:30:45.12` / `09:30:45.12` …

Individually parsing all of these is an accident waiting to happen. **PowerShell's `Get-Date -Format`** is locale-independent:

```bat
for /f "delims=" %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set TS=%%i
```

Append `-NoProfile` to reduce startup cost.

---

## Argument forwarding

`%*` passes all arguments through to Python:

```bat
python script.py %* > "%LOG%" 2>&1
```

Example:

```bash
run.bat --input data.csv --output result.json -v
```

→ argparse interprets it directly on the Python side.

---

## Choosing among multiple binaries

When `python` is not on PATH / you want to use the `py` launcher:

```bat
:: prefer py launcher (Windows standard) if available
where py >nul 2>&1 && (set PY=py) || (set PY=python)
%PY% -3.12 script.py %*
```

But in the standard flow that activates a venv, `python` is fine
(it resolves to `Scripts\python.exe` inside the venv).

---

## Do not write Japanese inside bat files (absolute)

**All strings and comments inside a bat file must be ASCII / English only. Never write Japanese.**

Even with `chcp 65001`, real damage occurs through any of the following:
- The cmd.exe code page initialization timing breaks literal strings inside the bat itself
- Parse results of `for /f` and similar get garbled
- Redirect targets (files / pipes / other processes) become garbled
- Once garbled, `if` comparisons and `set` values silently break — behavior changes without even an error

```bat
:: ✅ OK
echo (log: %LOG%)
:: comment in English only

:: ❌ NG (still breaks even with chcp)
echo （ログ：%LOG%）
:: Japanese comments are also forbidden
```

No exceptions. Japanese inside a bat creates **accidents that the editor cannot notice by feel**, so we ban it entirely.

When Japanese is needed for UI display, have the bat just invoke things, and have the main body (Python) output Japanese.

### Related: sh launchers are looser

Under `launchers-unix.md`, sh / bash run in UTF-8 environments by default, so Japanese is allowed.
**Only bat is special** — that's the right mental model.

---

## Sample: run-server.bat for FastAPI

```bat
@echo off
chcp 65001 > nul
setlocal
cd /d "%~dp0"

if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

set HOST=127.0.0.1
set PORT=8000

for /f "delims=" %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set TS=%%i
if not exist log mkdir log
set LOG=log\server-%TS%.log

echo Starting FastAPI on http://%HOST%:%PORT% (log: %LOG%)
uvicorn mypkg.server.app:build_fastapi --factory --host %HOST% --port %PORT% > "%LOG%" 2>&1
endlocal & exit /b %ERRORLEVEL%
```

---

## Things you must not do

```bat
:: NG: no chcp - source of garbling
@echo off
python script.py

:: NG: no setlocal - pollutes parent shell
set TEMPVAR=foo

:: NG: raw concat of %time% / %date% - fails depending on locale
set TS=%date%-%time%   :: may yield an invalid filename

:: NG: Japanese inside bat
echo （ログ出力）
:: 日本語コメントも禁止
```

---

## Related files

- `scripts/launchers-unix.md` — UNIX-side counterpart
- `scripts/python-script.md` — Python script that gets called
- `core/language-rules.md` — bat output is English
