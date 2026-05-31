# workspace Stop フック — レスポンス終了時に TODO/QA リマインダーを出力する。
#
# env トグル:
#   WORK_STOP_REMINDER（デフォルト truthy）— falsy で全体を無効化する
#   WORK_MERGE_PROPOSAL（デフォルト truthy）— falsy でマージ提案を省略する
#     （stop.md の代わりに stop-no-merge.md を使用）

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
