"""SessionStart フックの入口。ファイル操作の作業規約をコンテキストへ注入する。

Usage:
python plugins/inject-rules/hooks/session_start.py < payload.json
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inject_rules.main import inject_conventions  # noqa: E402

if __name__ == "__main__":
    sys.exit(inject_conventions())
