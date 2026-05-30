<!-- This file is a Japanese mirror. When updating the English original, update this file too. -->
# python-script — 単一ファイルスクリプト

> このファイルは `python-script.md` の日本語ミラーです。

`pyproject.toml` を作らない簡易スクリプトの構造。
1 ファイル〜数ファイルで完結する自動化、コンバート、レポート生成等で使う。

---

## ファイル構成

```
project/
├── script.py             # メイン
├── log/                  # 実行ログ（実行時に自動作成）
├── run.bat               # Windows ランチャー（任意）
├── run.sh                # UNIX ランチャー（任意）
└── README.md             # 使い方（推奨）
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

## 必須要素

1. **モジュール docstring**: 1 行目で何をするか、続けて詳細
2. **`from __future__ import annotations`**: 全ファイル冒頭
3. **`argparse`**: 引数は必ず argparse でパース（即値ハードコード禁止）
4. **`main() -> int`**: メイン処理は関数化、終了コードを返す
5. **`if __name__ == "__main__": sys.exit(main())`**: 直接実行可能に
6. **logger 使用**: `print` でなく `logger`
7. **例外処理**: 想定例外を捕まえ、未捕捉例外は `logger.exception` で traceback ごと残す
8. **コメント・ログは日本語で書く**: インラインコメントおよび `logger.*` のメッセージ文字列は英語でなく日本語で書く

---

## ログ出力先

簡易スクリプトでも開発時はファイル出力したいことが多い。
**Python 側で書かず**、bat / sh ランチャーで `tee` する方式が楽（後で grep しやすい）:

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

詳細は `scripts/launchers-windows.md` / `scripts/launchers-unix.md`。

---

## 複数ファイル化が必要になったら

スクリプトが大きくなって `script.py` 1 つに収まらなくなったら:

```
project/
├── script.py             # entry point
├── _processing.py        # 処理本体
├── _formatting.py        # 出力整形
└── log/
```

`_` プレフィックスで「内部」を示す。さらに大きくなる兆しが見えたら `py-project` に昇格。

---

## 依存ライブラリ

サードパーティ依存が要るなら `requirements.txt` を置いて `pip install` できるようにする:

```
# requirements.txt
httpx>=0.27
pydantic>=2.0
```

これも増えてきたら（5 個以上 / venv が要る規模）`py-project` に昇格する目安。

---

## やってはいけないこと

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

## 関連ファイル

- `scripts/launchers-windows.md` — bat ランチャー
- `scripts/launchers-unix.md` — sh ランチャー
- `scripts/tkinter.md` — GUI スクリプトの場合
- `core/comments.md` — docstring の書き方
