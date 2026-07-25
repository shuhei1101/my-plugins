"""作業規約注入ユースケースの結合テスト。"""
from __future__ import annotations

import json

SESSION = "9f2c1b"


def _payload() -> dict:
    """セッション開始フックのペイロードを組み立てる。"""
    return {"session_id": SESSION, "hook_event_name": "SessionStart", "source": "startup"}


def _response(capsys) -> dict:
    """標準出力の応答 JSON を返す。"""
    return json.loads(capsys.readouterr().out.strip())


def test_normal(capsys, run_session_start):
    """作業規約をコンテキストへ追加する（正常系）。"""
    # 実行
    code = run_session_start(_payload())
    # 検証
    assert code == 0
    output = _response(capsys)["hookSpecificOutput"]
    assert output["hookEventName"] == "SessionStart"
    assert "新規ファイルの作成手順" in output["additionalContext"]
