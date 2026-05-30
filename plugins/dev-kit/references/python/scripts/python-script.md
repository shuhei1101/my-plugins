# python-script — Single-file scripts

Structure for simple scripts that don't need a `pyproject.toml`.
Used for automation, conversion, report generation, etc. that fit in one or a few files.

---

## File layout

```
project/
├── script.py             # main
├── log/                  # runtime logs (auto-created at runtime)
├── run.bat               # Windows launcher (optional)
├── run.sh                # UNIX launcher (optional)
└── README.md             # usage (recommended)
```

No `pyproject.toml` needed. Promote to **`py-project`** once the whole project needs packaging.

---

## Standard template for script.py

```python
#!/usr/bin/env python3
"""一行でこのスクリプトが何をするか書く。

もう少し詳細な説明があるならここに。例:
- 入力: CSV ファイル（path で指定）
- 出力: 集計済み JSON を stdout へ
- 副作用: log/ にログ出力

Usage:
    python script.py --input data.csv --output result.json
"""
from __future__ import annotations
import argparse
import logging
import sys
from pathlib import Path


# ================================================================
# 定数
# ================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
LOG_DIR = SCRIPT_DIR / "log"


# ================================================================
# Logger
# ================================================================

def _setup_logger() -> logging.Logger:
    logger = logging.getLogger("script")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(message)s"))
    logger.addHandler(handler)
    return logger


logger = _setup_logger()


# ================================================================
# 引数
# ================================================================

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, required=True, help="input CSV file")
    parser.add_argument("--output", type=Path, required=True, help="output JSON file")
    parser.add_argument("--verbose", "-v", action="store_true", help="verbose log")
    return parser.parse_args()


# ================================================================
# 処理本体
# ================================================================

def process(input_path: Path, output_path: Path) -> None:
    """入力 CSV を読んで集計結果を JSON に書く。"""
    logger.info(f"{input_path} を読み込み中")
    # ... 実処理
    logger.info(f"{output_path} に書き込み完了")


# ================================================================
# Entry point
# ================================================================

def main() -> int:
    args = _parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    try:
        process(args.input, args.output)
        return 0
    except FileNotFoundError as e:
        logger.error(f"ファイルが見つかりません: {e}")
        return 2
    except Exception:
        logger.exception("予期しないエラーが発生しました")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## Required elements

1. **Module docstring**: first line states what it does, followed by details
2. **`from __future__ import annotations`**: at the top of every file
3. **`argparse`**: always parse arguments via argparse (no hardcoded literals)
4. **`main() -> int`**: main processing is a function that returns an exit code
5. **`if __name__ == "__main__": sys.exit(main())`**: makes the file directly runnable
6. **Use logger**: not `print`, use `logger`
7. **Exception handling**: catch expected exceptions; log uncaught ones with `logger.exception` to preserve the traceback
8. **Japanese for comments and logs**: write all inline comments and `logger.*` message strings in Japanese — not English

---

## Log output destination

Even for simple scripts, you often want file output during development.
Rather than **writing it in Python**, it's easier to `tee` in a bat/sh launcher (easier to grep later):

```bat
:: run.bat
@echo off
chcp 65001 > nul
setlocal
set TS=%date:~0,4%%date:~5,2%%date:~8,2%-%time:~0,2%%time:~3,2%%time:~6,2%
set LOG=log\script-%TS%.log
if not exist log mkdir log
python script.py %* > "%LOG%" 2>&1
type "%LOG%"
```

```bash
# run.sh
#!/usr/bin/env bash
set -euo pipefail
mkdir -p log
TS=$(date +%Y%m%d-%H%M%S)
python script.py "$@" 2>&1 | tee "log/script-$TS.log"
```

See `scripts/launchers-windows.md` / `scripts/launchers-unix.md` for details.

---

## When you need multiple files

When the script grows beyond a single `script.py`:

```
project/
├── script.py             # entry point
├── _processing.py        # core processing
├── _formatting.py        # output formatting
└── log/
```

The `_` prefix indicates "internal". When you see signs of further growth, promote to `py-project`.

---

## Third-party dependencies

If you need third-party dependencies, put a `requirements.txt` so they can be `pip install`ed:

```
# requirements.txt
httpx>=0.27
pydantic>=2.0
```

When this grows (5+ dependencies / large enough to need a venv), it's the threshold to promote to `py-project`.

---

## Things you must not do

```python
# ❌ argparse なし、即値
INPUT_PATH = Path("/some/hardcoded/path/data.csv")   # コマンドライン引数にする

# ❌ print デバッグ
print("processing...")   # logger.info を使う

# ❌ main がない、トップレベルに処理を書く
data = pd.read_csv(...)   # ← 即実行されてしまう
# main() に閉じる

# ❌ sys.exit を main の外でやる
sys.exit(0)   # main の return で表現する
```

---

## Related files

- `scripts/launchers-windows.md` — bat launcher
- `scripts/launchers-unix.md` — sh launcher
- `scripts/tkinter.md` — when it's a GUI script
- `core/comments.md` — how to write docstrings
