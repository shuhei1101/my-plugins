#!/usr/bin/env python3
"""monitor/main.py

gh-kit モニターデーモン。各モニターの poll() を順番に呼び出し続ける。

使い方:
    python main.py

新しいモニターの追加方法:
    1. {name}.py を作成し poll() 関数を実装する
    2. main() 内の while ループに {name}.poll() を追記する

    constants.sh から動的注入される定数: utils.load_constants_sh() 参照
"""

from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

# 同パッケージ内モジュールを解決できるようにパスを通す
sys.path.insert(0, str(Path(__file__).resolve().parent))

import settings
from features.monitors import issue_triage_monitor
from shared.logger import logger


def preflight() -> None:
    """起動前に外部コマンド（claude / gh）の存在を検証する。"""
    for tool in ("claude", "gh"):
        if shutil.which(tool) is None:
            logger.error(f"{tool!r} が見つかりません。インストールされているか確認してください。")
            sys.exit(1)


def main() -> int:
    """デーモン本体: 各モニターの poll() を順番に呼び出し続ける。"""
    preflight()

    logger.info("gh-kit monitor 起動")
    logger.info(f"POLL_INTERVAL={settings.POLL_INTERVAL}s")
    logger.info("ポーリング開始")

    while True:
        try:
            issue_triage_monitor.poll()
            # 将来追加例: issue_spec_monitor.poll()
        except Exception:
            logger.exception("ポーリング中に例外が発生しました")
        time.sleep(settings.POLL_INTERVAL)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("SIGINT を受信しました。終了します。")
        sys.exit(130)
