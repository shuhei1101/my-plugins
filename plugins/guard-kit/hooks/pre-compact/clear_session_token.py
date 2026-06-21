"""PreCompact フック: コンパクション前にセッショントークンを削除する。

コンテキストがリセットされるため、削除することでルールが再注入されるようにする。
"""
import json
import pathlib
import sys

TOKEN_DIRS = [
    pathlib.Path.home() / ".claude" / "tokens" / "dev-kit" / "rules",
    pathlib.Path.home() / ".claude" / "tokens" / "guard-kit" / "rules",
]

data = json.loads(sys.stdin.read())
session_id = data.get("session_id", "")
if session_id:
    for token_dir in TOKEN_DIRS:
        token_file = token_dir / f"{session_id}.json"
        token_file.unlink(missing_ok=True)  # なければ無視
