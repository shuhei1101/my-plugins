"""PreCompact フックの入口。圧縮でルールが消えるため注入済み記録を破棄して再注入させる。

Usage:
python plugins/inject-rules/hooks/pre_compact.py < payload.json
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inject_rules.main import clear  # noqa: E402

if __name__ == "__main__":
    sys.exit(clear())
