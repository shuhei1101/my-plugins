# python-script — Single-file scripts

Structure for simple scripts that don't need a `pyproject.toml`.
Used for automation, conversion, report generation, etc. that fit in one or a few files.

---

## File layout

Scripts live in a `scripts/` (or `tools/`) subfolder under the project root — not at the root itself.

```
project/
└── scripts/              # or tools/
    ├── my-script.py      # main script
    └── _common.py        # shared helpers (optional)
```

No `pyproject.toml` needed. Promote to **`py-project`** once the whole project needs packaging.

---

## Standard template for my-script.py

```python
#!/usr/bin/env python3
"""一行でこのスクリプトが何をするか書く。

もう少し詳細な説明があるならここに。例:
- 入力: CSV ファイル（path で指定）
- 出力: 集計済み JSON を stdout へ

# 入力 CSV を集計して JSON に出力する
python my-script.py --input data.csv --output result.json
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path


# ================================================================
# 定数
# ================================================================

SCRIPT_DIR = Path(__file__).resolve().parent


# ================================================================
# 引数
# ================================================================

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, required=True, help="input CSV file")
    parser.add_argument("--output", type=Path, required=True, help="output JSON file")
    return parser.parse_args()


# ================================================================
# 処理本体
# ================================================================

def process(input_path: Path, output_path: Path) -> None:
    """入力 CSV を読んで集計結果を JSON に書く。"""
    print(f"{input_path} を読み込み中")
    # ... 実処理
    print(f"{output_path} に書き込み完了")


# ================================================================
# Entry point
# ================================================================

def main() -> int:
    args = _parse_args()

    try:
        process(args.input, args.output)
        return 0
    except FileNotFoundError as e:
        print(f"ファイルが見つかりません: {e}", file=sys.stderr)
        return 2
    except Exception:
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

The usage in the docstring: write the command **without indentation** so it can be copy-pasted
and run directly, with a `#` comment line **above** the command describing what it does. Show
optional arguments in `[brackets]` (e.g. `python my-script.py --input data.csv [--verbose]`).

---

## Required elements

1. **Module docstring**: first line states what it does, followed by details and a usage example
   (un-indented command with a `#` description above it; optional args in `[brackets]`)
2. **`from __future__ import annotations`**: at the top of every file
3. **`argparse`**: always parse arguments via argparse (no hardcoded literals)
4. **`main() -> int`**: main processing is a function that returns an exit code
5. **`if __name__ == "__main__": sys.exit(main())`**: makes the file directly runnable
6. **Use `print`**: stdout for normal output, `print(..., file=sys.stderr)` for errors — no logging module needed
7. **Exception handling**: catch expected exceptions; use `traceback.print_exc()` for unexpected ones to preserve the traceback
8. **Japanese for comments and print messages**: write all inline comments and `print` message strings in Japanese — not English

---

## Things you must not do

```python
# ❌ argparse なし、即値
INPUT_PATH = Path("/some/hardcoded/path/data.csv")   # コマンドライン引数にする

# ❌ main がない、トップレベルに処理を書く
data = pd.read_csv(...)   # ← 即実行されてしまう
# main() に閉じる

# ❌ sys.exit を main の外でやる
sys.exit(0)   # main の return で表現する

# ❌ logging モジュールを使う（スクリプトには不要）
import logging
logger = logging.getLogger("script")
logger.info("processing...")   # print を使う
```

---

## Related files

- `scripts/tkinter.md` — when it's a GUI script
- `core/comments.md` — how to write docstrings
