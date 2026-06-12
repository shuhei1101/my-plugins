"""SessionStart フック: work プラグインの概要をコンテキストに注入する。

Args:
    sys.argv[1]: 注入する Markdown ファイルパス（hooks.json から session_start.md を渡す）
"""
from __future__ import annotations

import json
import pathlib
import sys


def main() -> None:
    """セッション開始時にプラグイン概要を additionalContext として注入する。"""
    if len(sys.argv) < 2:
        return

    prompt_path = pathlib.Path(sys.argv[1])
    if not prompt_path.exists():
        return

    payload = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": prompt_path.read_text("utf-8"),
        },
    }
    sys.stdout.buffer.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    main()
