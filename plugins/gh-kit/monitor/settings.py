from __future__ import annotations

import os
import tempfile
from pathlib import Path

from utils import _load_env_file

# カレントディレクトリの gh_monitor.env を優先して読み込む（外部 export 済みを優先）
_load_env_file(Path.cwd() / "gh_monitor.env")

POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "30"))
LOCK_FILE = os.environ.get(
    "LOCK_FILE",
    str(Path(os.environ.get("TMPDIR", tempfile.gettempdir())) / "gh-kit-issue-review.lock"),
)
