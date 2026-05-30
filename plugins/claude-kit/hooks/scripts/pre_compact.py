# claude-kit PreCompact hook — prompt the user to run conversation-to-claude
# before context compaction proceeds.
#
# Token semantics: a tempdir flag (`pre-compact-once-{session_id}`) alternates
# between "fire prompt + touch flag" and "skip + remove flag", so a /compact
# cycle that fires PreCompact twice (before the skill, after the skill) only
# surfaces the prompt once. The next compaction cycle starts fresh.

from __future__ import annotations

import pathlib
import sys
import tempfile

from _common import emit_block_reason, read_hook_input


def main() -> None:
    data = read_hook_input()
    session_id = data.get("session_id", "default")
    token = pathlib.Path(tempfile.gettempdir()) / f"pre-compact-once-{session_id}"

    if token.exists():
        token.unlink()
        return

    token.touch()
    emit_block_reason(pathlib.Path(sys.argv[1]))


if __name__ == "__main__":
    main()
