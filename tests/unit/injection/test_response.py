"""`features/injection/response.py` の単体テスト。"""
from __future__ import annotations

from inject_rules.features.injection.response import build_response
from inject_rules.features.injection.types import InjectionBlock, PackResult

A = "https://example.com/a.md"


def _result(*, remaining: int) -> PackResult:
    """テスト用の詰め込み結果を組み立てる。"""
    block = InjectionBlock(url=A, patterns=("**/*.py",), body="本文")
    return PackResult(blocks=[block], completed=[A], partial={}, remaining=remaining)


def test_build_response():
    """完了時の応答（正常系）。"""
    # 準備
    result = _result(remaining=0)
    # 実行
    response = build_response(result, "注入テキスト", loaded=1, total=1)
    # 検証
    output = response["hookSpecificOutput"]
    assert output["hookEventName"] == "PreToolUse"
    assert output["permissionDecision"] == "allow"
    assert output["additionalContext"] == "注入テキスト"


def test_build_response_when_remaining():
    """未完了時の応答（正常系）。"""
    # 準備
    result = _result(remaining=1)
    # 実行
    response = build_response(result, "注入テキスト", loaded=1, total=2)
    # 検証
    assert response["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert "残り 1" in response["systemMessage"]
