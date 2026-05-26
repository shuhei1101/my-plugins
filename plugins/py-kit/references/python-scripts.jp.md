<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Python スクリプト規約 — py-kit（日本語ミラー）

> このファイルは `python-scripts.md` の日本語ミラーです。Claude Code には読み込まれません。

スタンドアロンスクリプト・bat ランチャー・簡易自動化の規約。

---

## 簡易スクリプト構造

フルプロジェクト雛形を必要としない単一ファイルスクリプト用：

**ファイルヘッダー（必須）:**

```python
"""
{script_name} — {1行の説明}

Usage:
  python {script_name}.py [options] {positional_args}
"""
```

**コード構造:**

```python
"""...(ヘッダー)..."""

# ── 標準ライブラリ ──────────────────────────────────────────
import argparse
from pathlib import Path
from typing import Optional

# ── サードパーティ ───────────────────────────────────────────
import some_lib  # pip install some_lib

# ── 定数 ────────────────────────────────────────────────────
SOME_CONSTANT: str = "value"

# ── プライベートヘルパー ──────────────────────────────────────
def _helper(value: str) -> str:
    return value.strip()

# ── メイン ──────────────────────────────────────────────────
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

`logger.py`・`config.py`・テスト・bat ファイル・setup スクリプト・`pyproject.toml` は作らない。必要なパッケージは `# pip install {package}` でインラインドキュメント化する。

---

## bat ランチャーテンプレート

> **Windows のみ。** bat ファイルに関するルールは Linux / macOS 環境には適用しない。
> Linux/macOS では代わりにシェルスクリプトや `Makefile` ターゲットを使う。

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

**ルール:**
- タイムスタンプ付きログファイル名は必須 — 固定名を使わない
- bat ファイルの内容は ASCII のみ — 日本語は cmd.exe の CP932 パースエラーを引き起こす
- タイムスタンプには PowerShell `Get-Date` を使う — `wmic` は Windows 11 24H2 以降で削除済み

コンソールとログへの同時出力（長時間実行コマンド）:

```bat
long_command.exe 2>&1 | powershell -NoProfile -Command "[Console]::InputEncoding=[System.Text.Encoding]::UTF8; $input | ForEach-Object { Write-Host $_; Add-Content -LiteralPath '%BAT_LOG%' -Value $_ -Encoding utf8 }"
```

---

## FastAPI run.bat テンプレート

> **Windows のみ。** 上記の bat ランチャーの注記を参照。

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

ポート規約：メインリポジトリには固定ポートを割り当て、ワークツリーのテストサーバーには固定ポート+1以上を使う。

---

## GUI（tkinter）

- アクションボタン：青色
- 設定ボタン → モーダル設定ダイアログを開く
- 設定ダイアログ：全設定項目を GUI から編集可能。`.env` に保存する
- 再起動が必要な設定：赤色で「再起動後に適用されます」と表示
- レイアウト：3案を生成してユーザーが選択する
