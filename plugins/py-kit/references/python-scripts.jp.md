<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# Python スクリプト規約 — py-kit（日本語ミラー）

> このファイルは `python-scripts.md` の日本語ミラーです。Claude Code には読み込まれません。
> 変更する場合は JP ミラーを先に更新し、その後 `python-scripts.md` にも反映してください。

スタンドアロンスクリプト・bat ランチャー・簡易自動化の規約。`python-core.md` と
合わせて読む。以下に適用：

- 単一 `.py` ファイルの Python スクリプト（`pyproject.toml`・パッケージディレクトリなし）
- Windows `.bat` ランチャー（どのプロジェクトでも）
- FastAPI `run.bat` ショートカットランチャー
- tkinter GUI クイックプロトタイプ

本格プロジェクトには**適用しない** — それらは `python-architecture.md` に従う。

---

## 1. 簡易スクリプト構造

簡易スクリプト = 1ファイル・1仕事・終了するもの。例：「この CSV を変換」「このページを1回スクレイプ」「このレポートを再生成」。

### 1.1 必須ファイルヘッダー

すべてのスクリプトは最低3行の docstring で始める：

```python
"""
{script_name} — {1行の目的}

Usage:
  python {script_name}.py [options] {positional_args}
"""
```

`argparse.ArgumentParser` がこれを `description=__doc__` で再利用するので、`--help` 出力がファイルヘッダーと一貫する。

### 1.2 セクションマーカー

水平線コメントで4つの論理領域を区切る。書式：

```python
"""...(ヘッダー)..."""

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
    """終了コードを返す；0が成功・非0がエラー。"""
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

### 1.3 セクション順は固定

| 領域 | 内容 | 順序の理由 |
|---|---|---|
| ヘッダー docstring | name・purpose・usage | `argparse` が読む |
| stdlib import | stdlib のみ | 最初に解決・サードパーティ要件なし |
| third-party import | サードパーティ・`# pip install` コメント付き | 実行前に何をインストールすべきかが見える |
| constants | 型アノテーション付きの `UPPER_SNAKE_CASE` 定数 | 関数が読む前に見える |
| private helpers | 先頭 `_` の `_helper()` 関数 | `main()` が使う |
| main + parse_args | エントリポイント | 一番下 — 見つけやすい |

順序を変えない。

### 1.4 `# pip install` コメント必須

すべてのサードパーティ import に `# pip install {package}` インラインコメントを付ける。これにより新しいインタプリタからでもドキュメントなしで実行可能になる。

```python
# ✅ 良い
import httpx       # pip install httpx
from pydantic import BaseModel  # pip install pydantic

# ❌ 悪い — 呼び出し元が推測する必要あり
import httpx
from pydantic import BaseModel
```

stdlib モジュール（`json`・`pathlib`・`typing`）にはコメント不要。

### 1.5 `main()` は終了コードを返す

`main()` は `int` を返す。`sys.exit(main(parse_args()))` で終了コードをシェルに伝え、bat ランチャーが `%ERRORLEVEL%` で分岐できるようにする。

```python
# ✅ 良い
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
# ❌ 悪い — 終了コードが伝播しない
def main(args):
    process(...)

if __name__ == "__main__":
    main(parse_args())
```

### 1.6 簡易スクリプトに含めてはいけないもの

スクリプトが「簡易」なのは、以下を持たないから。これらが必要になったら、それはプロジェクトに昇格 — `pyproject.toml` を作り `python-architecture.md` に従う。

| 簡易スクリプトで禁止 | 理由 |
|---|---|
| `pyproject.toml` | それはプロジェクト |
| `logger.py` | 1ファイルが同フォルダの別 `.py` を import すべきでない；stdlib `logging.basicConfig()` をインラインで使う |
| 別ファイル `config.py` | 定数と CLI 引数で済ます |
| bat ランチャー | `python script.py` で直接実行 |
| `setup/setup_venv.bat` | コメントに書かれたモジュールを `pip install` するようユーザーに伝える |
| `tests/` フォルダ | テストが必要なら、それはプロジェクト |
| 複数ファイル | 「簡易スクリプト」は1ファイル |

これらに手を伸ばしているなら一度立ち止まる：「これは本当にスクリプトか？」最初からプロジェクトであるべきだった可能性が高い。

### 1.7 argparse パターン

#### 1.7.1 標準パターン

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

#### 1.7.2 サブコマンド

スクリプトが複数モードを持つようになったら、subparser を使う — `--mode` 文字列は渡さない。

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

#### 1.7.3 verbosity フラグ → ロギングレベル

```python
def main(args: argparse.Namespace) -> int:
    level = logging.WARNING - 10 * args.verbose  # -v=INFO・-vv=DEBUG
    logging.basicConfig(level=max(level, logging.DEBUG), format="[%(levelname)s] %(message)s")
    ...
```

### 1.8 簡易スクリプトのロギング

`logging.basicConfig()` をインラインで使う — `logger.py` ファイルは作らない。

```python
import logging

def main(args: argparse.Namespace) -> int:
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
    logger = logging.getLogger(__name__)
    logger.info("Starting %s", args.input)
    ...
```

ログファイルが必要な長時間スクリプトはプロジェクトの領域 — `python-testing.md` のロガー仕様を参照。

### 1.9 簡易スクリプトのエラー処理

終了コード：

| コード | 意味 |
|---|---|
| 0 | 成功 |
| 1 | 運用エラー（入力ファイルなし・ネットワークエラー等） |
| 2 | ユーザーエラー（CLI 引数間違い — argparse が自動で 2 を返す） |
| 130 | ユーザー中断（Ctrl+C） — クリーンアップが必要なら明示的に `KeyboardInterrupt` を処理 |

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

### 1.10 出力規約

| 出力 | 行き先 |
|---|---|
| 通常ステータス（`Starting...`・進捗） | `logger.info` 経由で `stdout` |
| エラー・警告 | `print(..., file=sys.stderr)` または `logger.error` |
| マシン可読の結果（JSON・CSV） | パイプ用なら `stdout`・そうでなければ `--out` ファイル |

スクリプトがパイプされる可能性があるなら、ステータスは `stderr` に出して `stdout` を consumer のためにクリーンに保つ。

---

## 2. bat ランチャーテンプレート — Windows のみ

> **Windows のみ。** bat ファイルと本セクションのルールは Linux / macOS には適用しない。それらでは shell スクリプトや `Makefile` ターゲットを使う。

### 2.1 なぜ bat ランチャーが必要か

Windows ユーザーは `run.bat` をダブルクリックでプログラム起動 — venv シェルを開けるとは期待しない。bat ランチャーが以下を処理：

1. 作業ディレクトリ設定（`%~dp0`）
2. virtualenv 有効化
3. stdout / stderr をタイムスタンプ付きファイルにログ
4. エラー時に pause してユーザーがメッセージを読める

### 2.2 標準テンプレート

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

### 2.3 bat ルール（硬性）

| ルール | 理由 |
|---|---|
| `chcp 65001 > nul` を最上部 | UTF-8 コンソール強制；CP932 が日本語パスを壊す |
| bat 内容は ASCII のみ — 日本語禁止 | `cmd.exe` が CP932 で bat をパース；日本語があると「コマンドではない」エラー |
| タイムスタンプは PowerShell `Get-Date` | `wmic` は Windows 11 24H2+ で削除済み — PowerShell のみ信頼できる |
| ログファイル名：`YYYYMMDDHHMMSS_{purpose}.log` | ソート可・上書きされない |
| `%cd%` ではなく `%~dp0` をパスに使う | `%cd%` はユーザーの起動方法に依存 |
| `setlocal` / `endlocal` で env var を分離 | 親シェルに漏れるのを防ぐ |
| `pause` は失敗時のみ・成功時禁止 | 正常実行はクリーンに終了 |
| `exit /b` で `%ERRORLEVEL%` を伝播 | CI・連鎖 bat が成功/失敗で分岐できる |
| `> "%BAT_LOG%" 2>&1` | stdout・stderr 両方をキャプチャ |

### 2.4 bat 禁止パターン

```bat
:: ❌ 悪い — bat 内日本語
echo 開始しました

:: ❌ 悪い — wmic（Win11 24H2+ で削除）
for /f %%I in ('wmic os get LocalDateTime ^| find "."') do set TS=%%I

:: ❌ 悪い — chcp なし・CP932 で動く
@echo off
:: (続き)

:: ❌ 悪い — 成功時 pause
python -m mypkg
pause

:: ❌ 悪い — 終了コード非伝播
python -m mypkg
exit /b 0
```

### 2.5 コンソール + ログ同時出力

リアルタイム進捗 + ログ両方が必要な長時間コマンド向け：

```bat
long_command.exe 2>&1 | powershell -NoProfile -Command "[Console]::InputEncoding=[System.Text.Encoding]::UTF8; $input | ForEach-Object { Write-Host $_; Add-Content -LiteralPath '%BAT_LOG%' -Value $_ -Encoding utf8 }"
```

リダイレクトのみより遅い（全行が PowerShell を通る）ので、本当に両方必要なときだけ使う。

---

## 3. FastAPI run.bat テンプレート — Windows のみ

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

### 3.1 ポート規約

| 環境 | ポート |
|---|---|
| メインリポジトリ・dev モード | このプロジェクト用に予約された固定ポート（例 `8000`） |
| ワークツリーテストサーバ（PR レビューなど） | メインポート + 1, + 2 ...（例 `8001`・`8002`） |
| テスト（実サーバ使用の e2e） | 各テスト実行ごとに選ばれる高い乱数ポート（`>30000`） |

プロジェクト固定ポートはプロジェクトの `CLAUDE.md` に明記する。

### 3.2 `python -m` で起動（`uvicorn` 直接ではなく）

`__main__.py` を正規エントリにし、`uvicorn` は内部から呼ぶ：

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
        log_config=None,  # 自前の logger.py を使う
        access_log=False, # ミドルウェアでリクエストロギング
    )

if __name__ == "__main__":
    run()
```

これにより起動方法が2系統に分かれず、bat ランチャーは `python -m {package_name}` を統一的に呼べる。

---

## 4. tkinter GUI クイックプロトタイプ

フルプロジェクトレイアウトを正当化しない小 GUI ツール向け：

### 4.1 スタイルルール

| 要素 | 規約 |
|---|---|
| アクションボタン | 青色 |
| 設定ボタン | モーダル設定ダイアログを開く |
| 設定ダイアログ | 全設定項目を GUI から編集可能・`.env` に保存 |
| 再起動が必要な設定 | 赤色で「再起動後に適用されます」ラベル |
| レイアウト | 3案生成 → ユーザーが選ぶ |

### 4.2 最小 tkinter スケルトン

```python
"""
{tool_name} — {1行の目的}

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
    action.configure(style="Accent.TButton")  # 青
    action.pack(pady=20)

    settings = ttk.Button(root, text="設定", command=lambda: _open_settings(root))
    settings.pack()

    root.mainloop()
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

クイックプロトタイプを超える規模になったらプロジェクト化し、GUI コードは `interface/gui/` に置く。

---

## 5. Linux / macOS 等価

bat が適用されない環境（Linux・macOS・CI）では shell スクリプトラッパー：

```bash
#!/usr/bin/env bash
# run.sh — {1行の目的}
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

| ルール | 理由 |
|---|---|
| 最上部 `set -euo pipefail` | エラー / 未定義変数 / パイプ失敗で即失敗 |
| `SCRIPT_DIR` に `"$(cd ... && pwd)"` | シンボリックリンク解決・呼び出し方法に依存しない |
| `tee` でコンソール + ログ | PowerShell トリックの Linux 版 |

---

## 6. Definition of Done — スクリプトチェックリスト

「簡易スクリプト」向け：

- [ ] 3行のヘッダー docstring（name・purpose・usage）
- [ ] セクションマーカーが正しい順序（stdlib / third-party / constants / helpers / main）
- [ ] すべてのサードパーティ import に `# pip install {package}` コメント
- [ ] `main()` が `int` 終了コードを返す
- [ ] 末尾に `sys.exit(main(parse_args()))`
- [ ] `logger.py`・`config.py`・追加ファイルなし
- [ ] すべての `print()` / ロガー出力が英語（`python-core.md` § 6.1）
- [ ] すべてのシグネチャに型ヒント（`python-core.md` § 3.1）
- [ ] エラーがドキュメント化された終了コードにマップ（§ 1.9）

bat ランチャー向け：

- [ ] 最上部 `chcp 65001 > nul`
- [ ] ファイル内に日本語なし
- [ ] PowerShell ベースのタイムスタンプ（`wmic` なし）
- [ ] ログが `log/YYYYMMDDHHMMSS_*.log` に書かれる
- [ ] `setlocal` / `endlocal` で env var を分離
- [ ] `pause` は失敗時のみ
- [ ] `exit /b %EXITCODE%` でコードを伝播
