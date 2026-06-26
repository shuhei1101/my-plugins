"""アプリ全体のロガー。

各モジュールから ``from shared.logger import logger`` でそのまま使う。
import された時点で root logger のハンドラが 1 度だけ設定される。
"""

from __future__ import annotations

import logging
import sys

# root logger に handler を一度だけ設定（再 import でも重複登録しない）
_root = logging.getLogger()
if not _root.handlers:
    _handler = logging.StreamHandler(stream=sys.stdout)
    _handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    _root.addHandler(_handler)
    _root.setLevel(logging.INFO)

# アプリ共通の logger インスタンス
logger = logging.getLogger("gh-kit-monitor")
