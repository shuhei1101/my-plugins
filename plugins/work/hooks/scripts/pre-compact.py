# work PreCompact フック — コンテキスト圧縮（/compact）の直前に
# conversation-to-claude スキルを実行させ、セッションの知識をアーティファクト化する。
#
# 仕組み:
#   1回目の発火 → `decision: block` でスキル実行を促す（圧縮を一旦止める）
#   2回目以降（スキル実行後の再 /compact）→ セッションフラグで素通りさせ圧縮を進める
#
# env トグル:
#   WORK_PRECOMPACT_CONV2CLAUDE（デフォルト truthy）— falsy で無効化する

from __future__ import annotations

import pathlib
import sys

from _common import (
    already_dispatched_this_session,
    emit_block_reason,
    env_truthy,
    read_hook_input,
)


def main() -> None:
    if not env_truthy("WORK_PRECOMPACT_CONV2CLAUDE", default=True):
        return

    data = read_hook_input()
    session_id = data.get("session_id", "default")

    # 2回目以降（スキル完了後に再実行された /compact）は素通りさせて圧縮を進める。
    if already_dispatched_this_session("work-pre-compact", session_id):
        return

    emit_block_reason(pathlib.Path(sys.argv[1]))


if __name__ == "__main__":
    main()
