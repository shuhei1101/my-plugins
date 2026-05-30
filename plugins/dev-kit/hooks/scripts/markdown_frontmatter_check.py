"""dev-kit Markdown frontmatter placement check.

PreToolUse(Edit | Write | MultiEdit) で発火し、*.md ファイルへの書き込み内容に
「YAML フロントマター開き --- より前に非空行がある」パターンを検出して警告する。

- block はしない (decision: block は出力しない) — 注意喚起のみ (advisory)
- 違反がなければ無出力で終了
- env トグル: DEV_KIT_MARKDOWN_CHECK=false/0/no/off で無効化（デフォルト有効）
"""
from __future__ import annotations

import json
import os
import sys


def _eprint(msg: str) -> None:
    sys.stderr.write(f"[dev-kit-markdown-check] {msg}\n")


def _has_content_before_frontmatter(content: str) -> bool:
    """Return True if non-empty lines appear before the opening ---."""
    lines = content.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            return False  # reached opening --- without finding non-empty content
        if stripped:
            return True   # non-empty line before ---
    return False  # no --- found at all → no frontmatter, not our concern


def main() -> int:
    if os.environ.get("DEV_KIT_MARKDOWN_CHECK", "true").lower() in ("false", "0", "no", "off"):
        return 0

    try:
        data = json.loads(sys.stdin.read())
    except Exception as e:
        _eprint(f"stdin parse error: {e}")
        return 0

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}

    if tool_name == "MultiEdit":
        file_path = tool_input.get("file_path", "")
        edits = tool_input.get("edits") or []
        content = "\n".join(e.get("new_string", "") for e in edits)
    elif tool_name in ("Edit", "Write"):
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("new_string") or tool_input.get("content") or ""
    else:
        return 0

    if not file_path.endswith(".md"):
        return 0

    if not _has_content_before_frontmatter(content):
        return 0

    reason = (
        "[dev-kit] Advisory: content found before the opening `---` frontmatter.\n\n"
        "Most Markdown renderers only recognize the YAML block when `---` is on the very "
        "first line. Anything above it will be rendered as body text.\n\n"
        "Fix: move HTML comments and other content to immediately after the closing `---`.\n\n"
        "This is advisory — you may proceed if the placement is intentional."
    )
    sys.stdout.buffer.write(
        json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False).encode("utf-8")
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
