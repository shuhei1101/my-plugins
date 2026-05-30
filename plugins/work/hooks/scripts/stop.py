# workspace Stop hook — emit a TODO/QA reminder when a response ends.
#
# Env toggles:
#   WORK_STOP_REMINDER (default truthy) — set falsy to disable entirely
#   WORK_MERGE_PROPOSAL (default truthy) — set falsy to drop the merge
#     suggestion (uses stop-no-merge.md instead of stop.md)

from __future__ import annotations

import pathlib
import sys

from _common import (
    emit_block_reason,
    env_truthy,
    exit_if_stop_loop,
    read_hook_input,
)


def main() -> None:
    if not env_truthy("WORK_STOP_REMINDER", default=True):
        return

    data = read_hook_input()
    exit_if_stop_loop(data)

    prompts_dir = pathlib.Path(sys.argv[1]).parent
    fname = (
        "stop.md"
        if env_truthy("WORK_MERGE_PROPOSAL", default=True)
        else "stop-no-merge.md"
    )
    emit_block_reason(prompts_dir / fname)


if __name__ == "__main__":
    main()
