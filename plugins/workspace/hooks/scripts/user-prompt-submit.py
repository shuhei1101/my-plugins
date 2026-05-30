"""workspace / user-prompt-submit — UserPromptSubmit hook.

ユーザープロンプトが送信されるたびに、PR 在中チェックや QA/TODO 確認手順を
プロンプト本体の前に注入する。
内容は完全にプロンプト Markdown ファイルに委ねており、このスクリプトは
ファイル中身を標準出力にそのまま流し込むだけ。

Args:
    sys.argv[1]: 注入する Markdown ファイルパス
                 （hooks.json から `${CLAUDE_PLUGIN_ROOT}/hooks/prompts/user-prompt-submit.md` を渡す）
"""

from __future__ import annotations

import os
import pathlib
import sys


def main() -> None:
    if os.environ.get("WORKSPACE_PR_ENFORCEMENT", "true").lower() in ("false", "0", "no", "off"):
        return
    prompt_path = pathlib.Path(sys.argv[1])
    if not prompt_path.exists():
        return
    sys.stdout.buffer.write(prompt_path.read_bytes())


if __name__ == "__main__":
    main()
