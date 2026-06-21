"""template_get.py — gh-kit/templates/ 配下のテンプレートを stdout に出力する CLI。

使い方:
  python template_get.py <template_name>

template_name は plugins/gh-kit/templates/ 配下のファイル名（拡張子込み）。
存在しないテンプレートは終了コード 2 で停止する。
"""
from __future__ import annotations

import sys
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("ERROR: 引数は template_name の 1 つだけ", file=sys.stderr)
        return 1

    name = argv[1]
    if "/" in name or ".." in name:
        print(f"ERROR: 不正なテンプレート名: {name}", file=sys.stderr)
        return 1

    path = TEMPLATES_DIR / name
    if not path.is_file():
        print(f"ERROR: テンプレートが見つからない: {path}", file=sys.stderr)
        return 2

    sys.stdout.write(path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
