"""単一UC「作業規約注入」の E2E テスト。"""
from __future__ import annotations

TARGET = "docs/新規.md"
CONTENT = "# 新規ページ"
CONVENTIONS_MARK = "新規ファイルの作成手順"


def _index_of(calls: list[tuple[str, dict]], name: str, path: str, **conditions: str) -> int:
    """指定ツール・指定パスの呼び出しが何番目に現れるかを返す（無ければ -1）。"""
    for index, (tool_name, tool_input) in enumerate(calls):
        if tool_name != name or tool_input.get("file_path") != path:
            continue
        if all(tool_input.get(key) == value for key, value in conditions.items()):
            return index
    return -1


def test_normal(claude_project, run_claude):
    """作業規約が取り込まれ、新規ファイルが空作成から始まる（正常系）。"""
    # 準備: 未作成のファイルパスを新規作成の依頼先にする
    target = claude_project / TARGET
    prompt = (
        f"`{TARGET}` を新規作成し、`{CONTENT}` という 1 行を書き込んでください。"
        "確認や質問はせずに実行し、終わったら「完了」とだけ答えてください。"
    )
    # 実行
    result = run_claude(prompt, indexes=None)
    # 検証: 作業規約が取り込まれている
    assert CONVENTIONS_MARK in result.transcript
    # 検証: 空ファイルの作成が内容の書き込みより先に行われている
    created = _index_of(result.tool_calls, "Write", str(target), content="")
    edited = _index_of(result.tool_calls, "Edit", str(target))
    assert created >= 0
    assert edited > created
    # 検証: 依頼した内容がファイルに書かれている
    assert CONTENT in target.read_text(encoding="utf-8")
