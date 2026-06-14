"""workspace / delete-guard — PreToolUse(Bash) hook.

`rm` または `rmdir` で `.git` または `.claude` ディレクトリを削除しようとしたとき、
永久にブロックする（再実行しても通らない）。

Args:
    sys.argv[1]: ブロックメッセージの Markdown ファイルパス
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

# rm / rmdir コマンドの検出
_RM_PATTERN = re.compile(r"\b(?:rm|rmdir)\b")

# .git または .claude がパスコンポーネントとして登場するパターン
# .gitignore 等は除外（.git の直後が英数字なら非対象）
_PROTECTED_PATH = re.compile(r"(?:^|[\s/\"\'\\])\.(?:git|claude)(?:[/\s\"\'\\]|$)")


def main() -> None:
    """削除ガードのメイン処理。"""
    payload = json.loads(sys.stdin.read())
    command = payload.get("tool_input", {}).get("command", "")

    # rm / rmdir を含まないコマンドはスキップ
    if not _RM_PATTERN.search(command):
        return

    # 保護対象パスが含まれていなければスキップ
    if not _PROTECTED_PATH.search(command):
        return

    prompt_path = pathlib.Path(sys.argv[1])
    context = (
        prompt_path.read_text("utf-8")
        if prompt_path.exists()
        else ".git または .claude ディレクトリの削除はブロックされています。"
    )

    sys.stdout.buffer.write(
        json.dumps({"decision": "block", "additionalContext": context}, ensure_ascii=False).encode("utf-8")
    )


if __name__ == "__main__":
    main()
