"""work プラグイン SessionStart フック: 作業フロー + タスクツール使い方を注入する。"""
from __future__ import annotations

import json
import pathlib
import sys


def main() -> None:
    """注入する Markdown を additionalContext として返す。"""
    if len(sys.argv) < 2:
        return
    msg_path = pathlib.Path(sys.argv[1])
    if not msg_path.exists():
        return

    body = msg_path.read_text("utf-8")
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": body,
        }
    }
    sys.stdout.buffer.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    main()
