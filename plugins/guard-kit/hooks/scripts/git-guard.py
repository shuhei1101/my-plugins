"""guard-kit / git-guard — PreToolUse(Bash) hook.

`git push` または `git merge` を含む Bash コマンドを検出したとき、
プロンプト注入 (`decision: block`) で必ずユーザー確認を挟む。

ループ防止のため、セッションごとに一時トークンファイルを使い、
1 回ブロックしたら 2 回目以降は素通りさせる
(= 同一セッションで同じコマンドを再実行できる)。

Args:
    sys.argv[1]: プロンプト本文の Markdown ファイルパス
                 （hooks.json から `${CLAUDE_PLUGIN_ROOT}/hooks/prompts/git-guard.md` を渡す）
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import tempfile


def main() -> None:
    payload = json.loads(sys.stdin.read())
    command = payload.get("tool_input", {}).get("command", "")

    if not re.search(r"\bgit\s+(push|merge)\b", command):
        return

    session_id = payload.get("session_id", "default")
    token = pathlib.Path(tempfile.gettempdir()) / f"workspace-git-guard-{session_id}"

    if token.exists():
        token.unlink()
        return

    token.touch()

    prompt_path = pathlib.Path(sys.argv[1])
    if not prompt_path.exists():
        return

    response = {"decision": "block", "reason": prompt_path.read_text("utf-8")}
    sys.stdout.buffer.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    main()
