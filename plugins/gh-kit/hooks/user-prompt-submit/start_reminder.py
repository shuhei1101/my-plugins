"""gh-kit / start-reminder — UserPromptSubmit フック。

ユーザープロンプトが送信されるたびに、/gh-kit:start スキル実行指示を
additionalContext として注入する。
ブロックせずコンテキスト注入のみなので、ユーザーのプロンプトはそのまま処理される。

Args:
    sys.argv[1]: 注入する Markdown ファイルパス
"""

from __future__ import annotations

import json
import os
import pathlib
import sys


def main() -> None:
    """gh-kit:start リマインダーを additionalContext として注入する。"""
    # 環境変数で無効化されている場合はスキップ
    if os.environ.get("GH_KIT_BRANCH_ENFORCEMENT", "true").lower() in ("false", "0", "no", "off"):
        return

    if len(sys.argv) < 2:
        return

    prompt_path = pathlib.Path(sys.argv[1])
    if not prompt_path.exists():
        return

    # decision を入れるとブロックになるため、additionalContext のみ注入する
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
