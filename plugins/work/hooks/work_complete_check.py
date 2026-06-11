"""workspace / work-complete-check — Stop フック。

レスポンス終了時に QA・マージ提案リマインダーを additionalContext として注入し、
Claude に処理を継続させる（decision: block で継続）。

env トグル:
    WORK_STOP_REMINDER（デフォルト truthy）— falsy で全体を無効化する
    WORK_MERGE_PROPOSAL（デフォルト truthy）— falsy でマージ提案を省略する
"""

from __future__ import annotations

import json
import os
import pathlib
import sys

_FALSY = {"false", "0", "no", "off"}


def env_truthy(name: str, default: bool = True) -> bool:
    """環境変数が truthy かどうかを返す。"""
    raw = os.environ.get(name)
    if raw is None:
        return default
    val = raw.strip().lower()
    # default=True の場合: _FALSY に含まれなければ truthy
    if default:
        return val not in _FALSY
    # default=False の場合: _TRUTHY に含まれれば truthy
    return val in {"true", "1", "yes", "on"}


def main() -> None:
    """Stop フック: リマインダーを additionalContext として注入して処理を継続させる。"""
    if not env_truthy("WORK_STOP_REMINDER", default=True):
        return

    # stop_hook_active は Stop フックが再発火していることを示す — 無限ループ防止
    data = json.loads(sys.stdin.read())
    if data.get("stop_hook_active"):
        sys.exit(0)

    if len(sys.argv) < 2:
        return

    prompts_dir = pathlib.Path(sys.argv[1]).parent
    # WORK_MERGE_PROPOSAL が falsy の場合はマージ提案なしのプロンプトを使用
    fname = (
        "work_complete_check.md"
        if env_truthy("WORK_MERGE_PROPOSAL", default=True)
        else "work_complete_no_merge.md"
    )
    prompt_path = prompts_dir / fname
    if not prompt_path.exists():
        return

    body = prompt_path.read_text("utf-8")
    # decision: block + hookSpecificOutput で継続（additionalContext を Claude が受け取る）
    payload = {
        "decision": "block",
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "additionalContext": body,
        },
    }
    sys.stdout.buffer.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    main()
