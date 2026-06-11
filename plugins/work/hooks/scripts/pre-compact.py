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

import json
import os
import pathlib
import sys
import tempfile

_FALSY = {"false", "0", "no", "off"}
_TRUTHY = {"true", "1", "yes", "on"}


def read_hook_input() -> dict:
    """フック入力 JSON を標準入力から読み込む。"""
    return json.loads(sys.stdin.read())


def env_truthy(name: str, default: bool = True) -> bool:
    """環境変数が truthy かどうかを返す。"""
    raw = os.environ.get(name)
    if raw is None:
        return default
    val = raw.strip().lower()
    if default:
        return val not in _FALSY
    return val in _TRUTHY


def already_dispatched_this_session(tag: str, session_id: str) -> bool:
    """セッション単位の重複実行ガード。

    フラグが既に存在する場合は True を返す。存在しない場合はフラグを作成して False を返す。
    `open("x")` による排他的生成で TOCTOU 競合を防ぐ。
    """
    flag = pathlib.Path(tempfile.gettempdir()) / f"{tag}-{session_id}"
    try:
        flag.open("x").close()
        return False
    except FileExistsError:
        return True


def emit_block_reason(prompt_path: pathlib.Path) -> None:
    """`{decision: block, reason: <プロンプト本文>}` JSON を標準出力に書き出す。"""
    if not prompt_path.exists():
        return
    body = prompt_path.read_text("utf-8")
    payload = {"decision": "block", "reason": body}
    sys.stdout.buffer.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


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
