"""`features/rules/index.py` の単体テスト。"""
from __future__ import annotations

import urllib.error

from inject_rules.features.rules.index import _resolve_base, load_rules, parse_index
from inject_rules.features.rules.types import RuleDefinition
from inject_rules.features.session.types import SessionState

BASE = "https://example.com/docs/"
INDEX = "https://example.com/docs/rules.yaml"
A_REL, B_REL = "a.md", "b.md"
A, B = BASE + A_REL, BASE + B_REL


# =========================
# parse_index
# =========================


def test_parse_index(rule_index):
    """標準的な索引の解析（正常系）。"""
    # 準備
    text = rule_index([(A_REL, ["**/*.py", "**/*.pyi"])])
    # 実行
    rules = parse_index(text, base=BASE)
    # 検証: ベースと相対パスが結合される
    assert rules == [RuleDefinition(location=A, patterns=("**/*.py", "**/*.pyi"))]


def test_parse_index_when_local_base(rule_index):
    """ローカルベースの結合（正常系）。"""
    # 準備
    text = rule_index([("rules/python/core/命名規則.md", ["**/*.py"])])
    # 実行
    rules = parse_index(text, base="/home/user/repo/my-plugins/docs/")
    # 検証: ローカル絶対パスとして解決される
    assert rules[0].location == "/home/user/repo/my-plugins/docs/rules/python/core/命名規則.md"


def test_parse_index_when_unquoted_pattern():
    """クォートなし glob の無視（正常系）。"""
    # 準備: 1 件はクォートあり、1 件はなし
    text = f'rules:\n  - rule: {A_REL}\n    paths:\n      - "**/*.py"\n      - **/*.md\n'
    # 実行
    rules = parse_index(text, base=BASE)
    # 検証: クォートなしの値は取り込まれない
    assert rules == [RuleDefinition(location=A, patterns=("**/*.py",))]


def test_parse_index_when_comment_and_blank(rule_index):
    """コメント・空行の無視（正常系）。"""
    # 準備
    text = "# 索引のコメント\n\n" + rule_index([(A_REL, ["**/*.py"])])
    # 実行
    rules = parse_index(text, base=BASE)
    # 検証
    assert rules == [RuleDefinition(location=A, patterns=("**/*.py",))]


def test_parse_index_when_patterns_missing():
    """`paths` 欠落エントリの除外（正常系）。"""
    # 準備: paths を持たないエントリ
    text = f"rules:\n  - rule: {A_REL}\n"
    # 実行
    rules = parse_index(text, base=BASE)
    # 検証
    assert rules == []


def test_parse_index_when_empty():
    """空本文（正常系）。"""
    # 実行・検証
    assert parse_index("", base=BASE) == []


# =========================
# _resolve_base
# =========================


def test_resolve_base_when_remote():
    """raw URL の親（正常系）。"""
    # 実行・検証
    assert _resolve_base(INDEX) == BASE


def test_resolve_base_when_local():
    """ローカル絶対パスの親（正常系）。"""
    # 実行・検証
    assert _resolve_base("/home/user/repo/docs/rules.yaml") == "/home/user/repo/docs/"


def test_resolve_base_when_backslash():
    """区切りの正規化（正常系）。"""
    # 実行・検証
    assert _resolve_base(r"C:\repo\docs\rules.yaml") == "C:/repo/docs/"


# =========================
# load_rules
# =========================


def test_load_rules(rule_index, fetch_stub):
    """単一索引の読み込み（正常系）。"""
    # 準備
    fetch = fetch_stub({INDEX: rule_index([(A_REL, ["**/*.py"]), (B_REL, ["**/*.md"])])})
    # 実行
    rules = load_rules([INDEX], fetch=fetch, state=SessionState())
    # 検証: 索引のベースと結合された場所になる
    assert [r.location for r in rules] == [A, B]


def test_load_rules_when_local_index(rule_index, fetch_stub):
    """ローカル索引の読み込み（正常系）。"""
    # 準備
    index = "/home/user/repo/my-plugins/docs/rules.yaml"
    fetch = fetch_stub({index: rule_index([("rules/python/core/命名規則.md", ["**/*.py"])])})
    # 実行
    rules = load_rules([index], fetch=fetch, state=SessionState())
    # 検証
    assert [r.location for r in rules] == [
        "/home/user/repo/my-plugins/docs/rules/python/core/命名規則.md"
    ]


def test_load_rules_when_multiple_indexes(rule_index, fetch_stub):
    """複数索引のマージ（正常系）。"""
    # 準備: ベースの異なる索引 2 件がそれぞれ別のルールを持つ
    first, second = "https://example.com/1/rules.yaml", "https://example.com/2/rules.yaml"
    fetch = fetch_stub(
        {first: rule_index([(A_REL, ["**/*.py"])]), second: rule_index([(B_REL, ["**/*.md"])])}
    )
    # 実行
    rules = load_rules([first, second], fetch=fetch, state=SessionState())
    # 検証: 設定順に連結され、各件が自分の索引のベースで解決される
    assert [r.location for r in rules] == [
        "https://example.com/1/a.md",
        "https://example.com/2/b.md",
    ]


def test_load_rules_when_duplicated_location(rule_index, fetch_stub):
    """重複の先勝ち（正常系）。"""
    # 準備: 同じベースで同じ相対パスを指す索引 2 件（パターンは異なる）
    first, second = "https://example.com/docs/1.yaml", "https://example.com/docs/2.yaml"
    fetch = fetch_stub(
        {first: rule_index([(A_REL, ["**/*.py"])]), second: rule_index([(A_REL, ["**/*.md"])])}
    )
    # 実行
    rules = load_rules([first, second], fetch=fetch, state=SessionState())
    # 検証: 1 件に畳まれ、先頭索引のパターンが残る
    assert rules == [RuleDefinition(location=A, patterns=("**/*.py",))]


def test_load_rules_when_fetch_failed(rule_index, fetch_stub):
    """取得失敗索引のスキップ（正常系）。"""
    # 準備: 1 件目が取得失敗、2 件目は成功
    first, second = "https://example.com/docs/1.yaml", "https://example.com/docs/2.yaml"
    fetch = fetch_stub(
        {second: rule_index([(B_REL, ["**/*.md"])])},
        errors={first: urllib.error.URLError("接続できません")},
    )
    # 実行
    rules = load_rules([first, second], fetch=fetch, state=SessionState())
    # 検証: 成功した索引のエントリだけ返る
    assert [r.location for r in rules] == [B]


def test_load_rules_when_fetch_failed_twice(fetch_stub, monkeypatch):
    """取得失敗ログの抑制（正常系）。"""
    # 準備: 取得に失敗する索引と、送出を記録するログ
    fetch = fetch_stub({}, errors={INDEX: urllib.error.URLError("接続できません")})
    logs: list[tuple] = []
    monkeypatch.setattr(
        "inject_rules.features.rules.index.emit_log", lambda *a, **kw: logs.append((a, kw))
    )
    state = SessionState()
    # 実行: 同じ状態で 2 回呼ぶ
    load_rules([INDEX], fetch=fetch, state=state)
    load_rules([INDEX], fetch=fetch, state=state)
    # 検証: ツール呼び出しごとに出さない
    assert len(logs) == 1
