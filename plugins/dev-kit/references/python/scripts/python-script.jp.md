<!-- This file is a Japanese mirror of python-script.md. When updating the English original, update this file too. -->
# python-script — 単一ファイルスクリプト

> このファイルは `python-script.md` の日本語ミラーです。

`pyproject.toml` を作らない簡易スクリプトの構造。
1 ファイル〜数ファイルで完結する自動化、コンバート、レポート生成等で使う。

---

## ファイル構成

スクリプトはプロジェクトルート直下ではなく、`scripts/`（または `tools/`）サブフォルダに置く。

```
project/
└── scripts/              # or tools/
    ├── my-script.py      # メイン
    └── _common.py        # 共通ヘルパー（任意）
```

`pyproject.toml` は不要。プロジェクト全体のパッケージ化が必要になったら **`py-project`** に昇格させる。

---

## script.py の標準テンプレート

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

docstring の使い方（Usage）は、**インデントを付けず**にコマンドを書いてそのままコピペ実行できるようにし、
コマンドの**上**に `#` コメントで何をするかの説明を書く。任意引数は `[角括弧]` で示す
（例: `python my-script.py --input data.csv [--verbose]`）。

---

## 必須要素

1. **モジュール docstring**: 1 行目で何をするか、続けて詳細と使い方の例
   （インデントなしのコマンド＋その上に `#` で説明。任意引数は `[角括弧]`）
2. **`from __future__ import annotations`**: 全ファイル冒頭
3. **`argparse`**: 引数は必ず argparse でパース（即値ハードコード禁止）
4. **`main() -> int`**: メイン処理は関数化、終了コードを返す
5. **`if __name__ == "__main__": sys.exit(main())`**: 直接実行可能に
6. **`print` を使う**: 通常の出力は stdout へ、エラーは `print(..., file=sys.stderr)` — logging モジュール不要
7. **例外処理**: 想定例外を捕まえ、未捕捉例外は `traceback.print_exc()` で traceback ごと残す
8. **コメント・print メッセージは日本語で書く**: インラインコメントおよび `print` のメッセージ文字列は英語でなく日本語で書く

---

## やってはいけないこと

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

## 関連ファイル

- `scripts/tkinter.md` — GUI スクリプトの場合
- `core/comments.md` — docstring の書き方
