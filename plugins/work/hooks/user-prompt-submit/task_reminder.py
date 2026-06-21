"""work プラグイン UserPromptSubmit フック: Claude Code タスク登録を促す。"""
from __future__ import annotations

import json
import os
import pathlib
import sys


def main() -> None:
    """タスク登録リマインダーを additionalContext として注入する。"""
    if os.environ.get("WORK_TASK_REMINDER", "true").lower() in ("false", "0", "no", "off"):
        return

    if len(sys.argv) < 2:
        return

    prompt_path = pathlib.Path(sys.argv[1])
    if not prompt_path.exists():
        return

    body = prompt_path.read_text("utf-8")
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": body,
        }
    }
    sys.stdout.buffer.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    main()
