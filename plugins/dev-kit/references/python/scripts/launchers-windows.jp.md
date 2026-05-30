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

> bat 内のコメント (`::`) も全部英語。理由は後述の「bat ファイル内に日本語を書かない」を参照。

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
:: prefer py launcher (Windows standard) if available
where py >nul 2>&1 && (set PY=py) || (set PY=python)
%PY% -3.12 script.py %*
```

ただし、venv を有効化する標準フローでは `python` で OK
（venv 内の Scripts\python.exe が呼ばれる）。

---

## bat ファイル内に日本語を書かない（絶対）

**bat ファイル内の文字列・コメントは全部 ASCII / 英語のみ。日本語は絶対に書かない。**

`chcp 65001` を付けても、以下のいずれかで実害が出る:
- cmd.exe のコードページ初期化タイミングで bat 本体のリテラル文字列が壊れる
- `for /f` などの parse 結果が文字化けする
- リダイレクト先（ファイル / パイプ / 別プロセス）で文字化けする
- 一度文字化けすると `if` 文の比較や `set` の値が壊れて、エラーすら出ずに静かに動作が変わる

```bat
:: ✅ OK
echo (log: %LOG%)
:: comment in English only

:: ❌ NG（chcp ありでも事故る）
echo （ログ：%LOG%）
:: 日本語コメントも禁止
```

例外なし。bat 内の日本語は **編集者の感覚で気付けない事故** を生むので、全面禁止する。

UI 表示用の日本語が必要な場合は、bat はそれを呼び出すだけにして、本体（Python）側で日本語を出力する。

### 関連: sh ランチャーは緩い

`launchers-unix.md` の sh / bash は UTF-8 環境が標準なので日本語可。
**bat だけが特殊** という認識でいい。

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

## 関連ファイル

- `scripts/launchers-unix.md` — UNIX 側の対応版
- `scripts/python-script.md` — 呼ばれる側の Python スクリプト
- `core/language-rules.md` — bat の出力は英語
