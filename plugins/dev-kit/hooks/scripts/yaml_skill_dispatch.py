# dev-kit yaml-skill-dispatch hook — remind the user to invoke `dev-kit:yaml`
# the first time a YAML file is edited or written in a session.

from __future__ import annotations

import pathlib
import sys

from _common import already_dispatched_this_session, emit_block_reason, read_hook_input


def main() -> None:
    data = read_hook_input()
    file_path = (data.get("tool_input") or {}).get("file_path", "") or ""
    if not (file_path.endswith(".yaml") or file_path.endswith(".yml")):
        return

    session_id = data.get("session_id", "default")
    if already_dispatched_this_session("dev-kit-yaml-skill", session_id):
        return

    emit_block_reason(pathlib.Path(sys.argv[1]))


if __name__ == "__main__":
    main()
