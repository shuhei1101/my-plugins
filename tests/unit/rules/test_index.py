"""`features/rules/index.py` の単体テスト。"""
from __future__ import annotations

import urllib.error

from inject_rules.features.rules.index import load_rules, parse_index
from inject_rules.features.rules.types import RuleDefinition
from inject_rules.features.session.types import SessionState

A = "https://example.com/a.md"
B = "https://example.com/b.md"


# =========================
# parse_index
# =========================


def test_parse_index(rule_index):
    """標準的な索引の解析（正常系）。"""
    # 準備
    text = rule_index([(A, ["**/*.py", "**/*.pyi"])])
    # 実行
    rules = parse_index(text)
    # 検証
    assert rules == [RuleDefinition(url=A, patterns=("**/*.py", "**/*.pyi"))]


def test_parse_index_when_unquoted_pattern():
    """クォートなし glob の無視（正常系）。"""
    # 準備: 1 件はクォートあり、1 件はなし
    text = f'rules:\n  - url: {A}\n    paths:\n      - "**/*.py"\n      - **/*.md\n'
    # 実行
    rules = parse_index(text)
    # 検証: クォートなしの値は取り込まれない
    assert rules == [RuleDefinition(url=A, patterns=("**/*.py",))]


def test_parse_index_when_comment_and_blank(rule_index):
    """コメント・空行の無視（正常系）。"""
    # 準備
    text = "# 索引のコメント\n\n" + rule_index([(A, ["**/*.py"])])
    # 実行
    rules = parse_index(text)
    # 検証
    assert rules == [RuleDefinition(url=A, patterns=("**/*.py",))]


def test_parse_index_when_patterns_missing():
    """`paths` 欠落エントリの除外（正常系）。"""
    # 準備: paths を持たないエントリ
    text = f"rules:\n  - url: {A}\n"
    # 実行
    rules = parse_index(text)
    # 検証
    assert rules == []


def test_parse_index_when_empty():
    """空本文（正常系）。"""
    # 実行・検証
    assert parse_index("") == []


# =========================
# load_rules
# =========================


def test_load_rules(rule_index, fetch_stub):
    """単一索引の読み込み（正常系）。"""
    # 準備
    index_url = "https://example.com/rules.yaml"
    fetch = fetch_stub({index_url: rule_index([(A, ["**/*.py"]), (B, ["**/*.md"])])})
    # 実行
    rules = load_rules([index_url], fetch=fetch, state=SessionState())
    # 検証
    assert [r.url for r in rules] == [A, B]


def test_load_rules_when_multiple_indexes(rule_index, fetch_stub):
    """複数索引のマージ（正常系）。"""
    # 準備: 索引 2 件がそれぞれ別のルールを持つ
    first, second = "https://example.com/1.yaml", "https://example.com/2.yaml"
    fetch = fetch_stub(
        {first: rule_index([(A, ["**/*.py"])]), second: rule_index([(B, ["**/*.md"])])}
    )
    # 実行
    rules = load_rules([first, second], fetch=fetch, state=SessionState())
    # 検証: 設定順に連結される
    assert [r.url for r in rules] == [A, B]


def test_load_rules_when_duplicated_url(rule_index, fetch_stub):
    """重複 URL の先勝ち（正常系）。"""
    # 準備: 同じ url を持つ索引 2 件（パターンは異なる）
    first, second = "https://example.com/1.yaml", "https://example.com/2.yaml"
    fetch = fetch_stub(
        {first: rule_index([(A, ["**/*.py"])]), second: rule_index([(A, ["**/*.md"])])}
    )
    # 実行
    rules = load_rules([first, second], fetch=fetch, state=SessionState())
    # 検証: 1 件に畳まれ、先頭索引のパターンが残る
    assert rules == [RuleDefinition(url=A, patterns=("**/*.py",))]


def test_load_rules_when_fetch_failed(rule_index, fetch_stub):
    """取得失敗索引のスキップ（正常系）。"""
    # 準備: 1 件目が取得失敗、2 件目は成功
    first, second = "https://example.com/1.yaml", "https://example.com/2.yaml"
    fetch = fetch_stub(
        {second: rule_index([(B, ["**/*.md"])])},
        errors={first: urllib.error.URLError("接続できません")},
    )
    # 実行
    rules = load_rules([first, second], fetch=fetch, state=SessionState())
    # 検証: 成功した索引のエントリだけ返る
    assert [r.url for r in rules] == [B]


def test_load_rules_when_fetch_failed_twice(fetch_stub, monkeypatch):
    """取得失敗ログの抑制（正常系）。"""
    # 準備: 取得に失敗する索引と、送出を記録するログ
    index_url = "https://example.com/rules.yaml"
    fetch = fetch_stub({}, errors={index_url: urllib.error.URLError("接続できません")})
    logs: list[tuple] = []
    monkeypatch.setattr(
        "inject_rules.features.rules.index.emit_log", lambda *a, **kw: logs.append((a, kw))
    )
    state = SessionState()
    # 実行: 同じ状態で 2 回呼ぶ
    load_rules([index_url], fetch=fetch, state=state)
    load_rules([index_url], fetch=fetch, state=state)
    # 検証: ツール呼び出しごとに出さない
    assert len(logs) == 1
