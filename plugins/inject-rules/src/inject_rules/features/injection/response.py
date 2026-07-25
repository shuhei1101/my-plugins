"""フックの応答 JSON の組み立て。"""
from __future__ import annotations

from typing import Any

from inject_rules.features.injection.types import PackResult

HOOK_EVENT_NAME = "PreToolUse"
SYSTEM_MESSAGE_HEADER = "[rules-injection]"


def build_response(result: PackResult, message: str, *, loaded: int, total: int) -> dict[str, Any]:
    """詰め込み結果と注入テキストからフックの応答を作る。"""
    # 未送信が残っているときだけ差し戻し、次の呼び出しで続きを送る
    if result.remaining:
        decision = "deny"
        progress = f"  Loading: {loaded}/{total} ファイル — 残り {result.remaining} 未完了"
    else:
        decision = "allow"
        progress = f"  Loaded: {loaded}/{total} ファイル"
    lines = [SYSTEM_MESSAGE_HEADER, progress, *(f"  · {block.url}" for block in result.blocks)]
    return {
        "hookSpecificOutput": {
            "hookEventName": HOOK_EVENT_NAME,
            "permissionDecision": decision,
            "additionalContext": message,
        },
        "systemMessage": "\n".join(lines) + "\n",
    }
