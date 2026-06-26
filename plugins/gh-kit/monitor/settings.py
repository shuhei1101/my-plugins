from __future__ import annotations

import os

# 全モニターの poll() を一巡したあとに待機する秒数（次の周回までのインターバル）
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "30"))
