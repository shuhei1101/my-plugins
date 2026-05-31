"""claude-kit setup_check — SessionStart フック: setup_done フラグを確認する。

setup_done が false / 未設定の場合、/claude-kit:setup-wizard を実行するよう
Claude に指示するブロック理由を出力する。
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

PLUGIN_NAME = "claude-kit"


def read_setup_done(plugin_name: str) -> bool:
    local_md = pathlib.Path.home() / ".claude" / f"{plugin_name}.local.md"
    if not local_md.exists():
        return False
    content = local_md.read_text("utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False
    for line in match.group(1).splitlines():
        if re.match(r"^\s*setup_done\s*:\s*true\s*$", line, re.IGNORECASE):
            return True
    return False


def main() -> None:
    if read_setup_done(PLUGIN_NAME):
        sys.exit(0)

    reason = (
        "**claude-kit プラグインの初回セットアップが完了していません。**\n\n"
        "`/claude-kit:setup-wizard` を実行してセットアップを完了してください。\n\n"
        "セットアップが完了したら通常どおり作業を続けることができます。"
    )
    payload = {"decision": "block", "reason": reason}
    sys.stdout.buffer.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    main()
