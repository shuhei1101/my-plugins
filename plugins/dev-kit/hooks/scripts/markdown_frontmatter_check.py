"""dev-kit Markdown frontmatter placement check.

PreToolUse(Write) で発火し、*.md ファイルへの書き込み内容に
「YAML フロントマター開き --- より前に非空行がある」パターンを検出して警告する。

- Edit / MultiEdit は対象外（new_string はファイル断片であり全体ではないため誤検知する）
- .jp.md ファイルは対象外（JP ミラーは仕様上 HTML コメントがフロントマター前に来る）
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

    # Edit / MultiEdit の new_string はファイル断片のため誤検知が多い — Write のみ対象
    if tool_name != "Write":
        return 0

    file_path = tool_input.get("file_path", "")
    content = tool_input.get("content") or ""

    if not file_path.endswith(".md"):
        return 0

    # JP ミラーファイルは仕様上 HTML コメントがフロントマター前に来るため除外
    if file_path.endswith(".jp.md"):
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
