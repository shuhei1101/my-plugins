"""PreCompact フック: コンパクション前にセッショントークンを削除する。

コンテキストがリセットされるため、削除することでルールが再注入されるようにする。
"""
import json
import pathlib
import sys

TOKEN_DIR = pathlib.Path.home() / ".claude" / "tokens" / "work" / "rules"

data = json.loads(sys.stdin.read())
session_id = data.get("session_id", "")
if session_id:
    token_file = TOKEN_DIR / f"{session_id}.json"
    token_file.unlink(missing_ok=True)  # なければ無視
