<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# launchers-windows — bat ランチャー

> このファイルは `launchers-windows.md` の日本語ミラーです。

Windows で Python スクリプトを起動する `.bat` ファイルの規約。

---

## 標準テンプレート

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

## 必須要素

| 要素 | 理由 |
|---|---|
| `@echo off` | コマンド自体を画面に出さない |
| `chcp 65001 > nul` | UTF-8 文字化け回避 |
| `setlocal` ... `endlocal` | 環境変数の汚染を避ける |
| `cd /d "%~dp0"` | bat の置かれた場所を基準にする |
| `.venv\Scripts\activate.bat`（存在チェック付き） | venv を自動で有効化 |
| **PowerShell でのタイムスタンプ取得** | `%time%` は locale 依存（`9:30` と `09:30` の混在）、PowerShell なら安全 |
| `log\` ディレクトリ確保 | ログ出力先 |
| `> "%LOG%" 2>&1` | stdout / stderr 両方をログへ |
| `type "%LOG%"` | 実行後に画面にも出す |
| `exit /b %EXIT_CODE%` | Python の終了コードを呼び出し元に伝える |

---

## タイムスタンプ生成: なぜ PowerShell か

`%date%` `%time%` は Windows の locale 設定で形式が変わる:
- `2026/05/28 ` / `2026-05-28` / `05/28/2026` …
- `9:30:45.12` / `09:30:45.12` …

これに対する個別パーシングは事故のもと。**PowerShell の `Get-Date -Format`** は locale 非依存:

```bat
for /f "delims=" %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set TS=%%i
```

`-NoProfile` を付けて起動コストを下げる。

---

## 引数転送

`%*` で全引数を Python へそのまま渡す:

```bat
python script.py %* > "%LOG%" 2>&1
```

例:

```bash
run.bat --input data.csv --output result.json -v
```

→ Python 側で argparse がそのまま解釈。

---

## 複数バイナリの選択

`python` が PATH にない / `py` ランチャーを使いたい場合:

```bat
:: py がある場合は優先（Windows 標準）
where py >nul 2>&1 && (set PY=py) || (set PY=python)
%PY% -3.12 script.py %*
```

ただし、venv を有効化する標準フローでは `python` で OK
（venv 内の Scripts\python.exe が呼ばれる）。

---

## 出力メッセージは英語

bat スクリプトは Windows のコードページ問題が起きやすいので、出力は **英語** で書く:

```bat
echo (log: %LOG%)         :: ✅
echo （ログ：%LOG%）        :: ❌（文字化けリスクあり）
```

`chcp 65001` を付けても、コンソールやリダイレクト先の挙動次第で文字化けする。

---

## サンプル: FastAPI 起動用 run-server.bat

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

## やってはいけないこと

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

## 関連ファイル

- `scripts/launchers-unix.md` — UNIX 側の対応版
- `scripts/python-script.md` — 呼ばれる側の Python スクリプト
- `core/language-rules.md` — bat の出力は英語
