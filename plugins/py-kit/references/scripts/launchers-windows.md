# launchers-windows — bat launcher

Conventions for `.bat` files that launch Python scripts on Windows.

---

## Standard template

```bat
@echo off
chcp 65001 > nul
setlocal

:: ----- このスクリプトの場所をカレントにする -----
cd /d "%~dp0"

:: ----- venv 有効化（存在すれば） -----
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

:: ----- タイムスタンプ（YYYYMMDD-HHMMSS）を PowerShell で生成 -----
for /f "delims=" %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set TS=%%i

:: ----- ログディレクトリ -----
if not exist log mkdir log
set LOG=log\script-%TS%.log

:: ----- 実行 -----
python script.py %* > "%LOG%" 2>&1
set EXIT_CODE=%ERRORLEVEL%

:: ----- 結果を表示 -----
type "%LOG%"
echo.
echo (log: %LOG%)
echo (exit: %EXIT_CODE%)

endlocal & exit /b %EXIT_CODE%
```

---

## Required elements

| Element | Reason |
|---|---|
| `@echo off` | Don't echo the commands themselves to the screen |
| `chcp 65001 > nul` | Avoid UTF-8 mojibake |
| `setlocal` ... `endlocal` | Avoid polluting environment variables |
| `cd /d "%~dp0"` | Use the location of the bat file as the base |
| `.venv\Scripts\activate.bat` (with existence check) | Auto-activate venv |
| **Timestamp via PowerShell** | `%time%` is locale-dependent (mix of `9:30` and `09:30`); PowerShell is safe |
| Ensure `log\` directory | Log output destination |
| `> "%LOG%" 2>&1` | Send both stdout and stderr to the log |
| `type "%LOG%"` | Also display on screen after execution |
| `exit /b %EXIT_CODE%` | Propagate Python's exit code to the caller |

---

## Timestamp generation: why PowerShell

`%date%` and `%time%` change format with the Windows locale setting:
- `2026/05/28 ` / `2026-05-28` / `05/28/2026` …
- `9:30:45.12` / `09:30:45.12` …

Per-locale parsing for these is accident-prone. **PowerShell's `Get-Date -Format`** is locale-independent:

```bat
for /f "delims=" %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set TS=%%i
```

Add `-NoProfile` to reduce startup cost.

---

## Argument forwarding

Pass all arguments to Python verbatim with `%*`:

```bat
python script.py %* > "%LOG%" 2>&1
```

Example:

```bash
run.bat --input data.csv --output result.json -v
```

→ Python's argparse interprets them as-is.

---

## Choosing among multiple binaries

When `python` is not in PATH / you want to use the `py` launcher:

```bat
:: py がある場合は優先（Windows 標準）
where py >nul 2>&1 && (set PY=py) || (set PY=python)
%PY% -3.12 script.py %*
```

However, in the standard flow where you activate venv, `python` is fine
(venv's `Scripts\python.exe` will be called).

---

## Output messages in English

bat scripts are prone to Windows code-page issues, so write output messages in **English**:

```bat
echo (log: %LOG%)         :: ✅
echo （ログ：%LOG%）        :: ❌（文字化けリスクあり）
```

Even with `chcp 65001`, mojibake can still happen depending on console behavior or redirection target.

---

## Sample: run-server.bat for launching FastAPI

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
:: ❌ chcp なし → 文字化けの種
@echo off
python script.py

:: ❌ setlocal なし → 親シェルを汚染
set TEMPVAR=foo

:: ❌ %time% / %date% を素で連結 → locale 依存で失敗
set TS=%date%-%time%   :: 不正なファイル名になる可能性
```

---

## Related files

- `scripts/launchers-unix.md` — UNIX counterpart
- `scripts/python-script.md` — the Python script that gets called
- `core/language-rules.md` — bat output should be English
