"""PreToolUse フックの入口。編集対象にマッチする規約ドキュメントをコンテキストへ注入する。

Usage:
python plugins/inject-rules/hooks/pre_tool_use.py < payload.json
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inject_rules.main import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
