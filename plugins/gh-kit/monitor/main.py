#!/usr/bin/env python3
"""monitor/main.py

gh-kit モニターデーモン。各モニターの poll() を順番に呼び出し続ける。

使い方:
    python main.py

新しいモニターの追加方法:
    1. {name}.py を作成し poll() 関数を実装する
    2. main() 内の while ループに {name}.poll() を追記する

    constants.sh から動的注入される定数: utils._load_constants_sh() 参照
"""

from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

# 同パッケージ内モジュールを解決できるようにパスを通す
sys.path.insert(0, str(Path(__file__).resolve().parent))

import issue_review
import settings
from utils import GH_KIT_PLUGIN_DIR, die, log


def preflight() -> None:
    """起動前に外部コマンド（claude / gh）の存在を検証する。"""
    for tool in ("claude", "gh"):
        if shutil.which(tool) is None:
            die(f"{tool!r} が見つかりません。インストールされているか確認してください。")


def main() -> int:
    """デーモン本体: 各モニターの poll() を順番に呼び出し続ける。"""
    preflight()

    log("gh-kit monitor 起動")
    log(f"  GH_KIT_PLUGIN_DIR={GH_KIT_PLUGIN_DIR}")
    log(f"  POLL_INTERVAL={settings.POLL_INTERVAL}s")
    log("ポーリング開始")

    while True:
        try:
            issue_review.poll()
            # 将来追加例: pr_plan.poll()
        except Exception as exc:
            log(f"ERROR: ポーリング中に例外が発生しました: {exc}")
        time.sleep(settings.POLL_INTERVAL)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("SIGINT を受信しました。終了します。")
        sys.exit(130)
