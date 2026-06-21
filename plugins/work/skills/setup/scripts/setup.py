"""setup.py — workspace セットアップスクリプト

カレントディレクトリに .work/ ドキュメント構造をブートストラップする。
notes/ のみを生成する（空ディレクトリ）。タスク・イシュー管理は廃止された
（GitHub Issues/PR を使う gh プラグインへ移管）。

使い方:
  python setup.py
"""

from __future__ import annotations

import sys
from pathlib import Path

TARGET_DIR = Path.cwd() / ".work"


def main() -> int:
    """メイン処理。.work/ をカレントディレクトリにブートストラップする。"""
    TARGET_DIR.mkdir(exist_ok=True)
    print(f"セットアップ中: {TARGET_DIR}")

    (TARGET_DIR / "notes").mkdir(exist_ok=True)
    print("  作成:       notes/")

    print(f"\nセットアップ完了: {TARGET_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
