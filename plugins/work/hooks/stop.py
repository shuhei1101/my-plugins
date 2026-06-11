# workspace Stop フック — レスポンス終了時に TODO/QA リマインダーを出力する。
#
# env トグル:
#   WORK_STOP_REMINDER（デフォルト truthy）— falsy で全体を無効化する
#   WORK_MERGE_PROPOSAL（デフォルト truthy）— falsy でマージ提案を省略する
#     （stop.md の代わりに stop-no-merge.md を使用）

from __future__ import annotations

import json
import os
import pathlib
import sys

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


def exit_if_stop_loop(input_data: dict) -> None:
    """Stop フックが再発火（stop_hook_active）のとき、静かに終了する。"""
    if input_data.get("stop_hook_active"):
        sys.exit(0)


def emit_block_reason(prompt_path: pathlib.Path) -> None:
    """`{decision: block, additionalContext: <プロンプト本文>}` JSON を標準出力に書き出す。"""
    if not prompt_path.exists():
        return
    body = prompt_path.read_text("utf-8")
    payload = {"decision": "block", "additionalContext": body}
    sys.stdout.buffer.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


def main() -> None:
    if not env_truthy("WORK_STOP_REMINDER", default=True):
        return

    data = read_hook_input()
    exit_if_stop_loop(data)

    if len(sys.argv) < 2:
        return  # 引数なし: fail-open で静かに終了
    prompts_dir = pathlib.Path(sys.argv[1]).parent
    fname = (
        "stop.md"
        if env_truthy("WORK_MERGE_PROPOSAL", default=True)
        else "stop-no-merge.md"
    )
    emit_block_reason(prompts_dir / fname)


if __name__ == "__main__":
    main()
