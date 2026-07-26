"""`features/rules/matcher.py` の単体テスト。"""
from __future__ import annotations

from pathlib import Path

from inject_rules.features.rules.matcher import _build_candidates, _glob_to_regex, match_rules
from inject_rules.features.rules.types import RuleDefinition

BASE = Path("/repo")


def _rule(url: str, *patterns: str) -> RuleDefinition:
    return RuleDefinition(location=url, patterns=patterns)


# =========================
# match_rules
# =========================


def test_match_rules():
    """索引順の抽出（正常系）。"""
    # 準備: 3 件中 2 件がマッチする
    rules = [
        _rule("https://example.com/py.md", "**/*.py"),
        _rule("https://example.com/md.md", "**/*.md"),
        _rule("https://example.com/wiki.md", "**/docs/wiki/**"),
    ]
    # 実行
    matched = match_rules(rules, "/repo/docs/wiki/規約.md", base_dir=BASE)
    # 検証: 索引順で 2 件
    assert [r.location for r in matched] == ["https://example.com/md.md", "https://example.com/wiki.md"]


def test_match_rules_when_no_match():
    """マッチなし（正常系）。"""
    # 準備
    rules = [_rule("https://example.com/py.md", "**/*.py")]
    # 実行
    matched = match_rules(rules, "/repo/README.md", base_dir=BASE)
    # 検証
    assert matched == []


def test_match_rules_when_multiple_patterns():
    """複数パターンの片方が一致（正常系）。"""
    # 準備: 2 パターンのうち 1 つだけ当たる
    rules = [_rule("https://example.com/a.md", "**/*.ts", "**/*.py")]
    # 実行
    matched = match_rules(rules, "/repo/src/main.py", base_dir=BASE)
    # 検証: 重複せず 1 件
    assert len(matched) == 1


# =========================
# _glob_to_regex
# =========================


def test_glob_to_regex_when_double_star():
    """区切りをまたぐ（正常系）。"""
    # 実行
    regex = _glob_to_regex("**/foo.py")
    # 検証
    assert regex.match("a/b/foo.py")
    assert regex.match("foo.py")


def test_glob_to_regex_when_single_star():
    """区切りをまたがない（正常系）。"""
    # 実行
    regex = _glob_to_regex("src/*.py")
    # 検証
    assert regex.match("src/main.py")
    assert not regex.match("src/sub/main.py")


def test_glob_to_regex_when_brace():
    """選択の展開（正常系）。"""
    # 実行
    regex = _glob_to_regex("{a,b}.py")
    # 検証
    assert regex.match("a.py")
    assert regex.match("b.py")
    assert not regex.match("c.py")


def test_glob_to_regex_when_dot():
    """メタ文字のエスケープ（正常系）。"""
    # 実行
    regex = _glob_to_regex("a.py")
    # 検証: ドットが任意 1 文字として扱われない
    assert not regex.match("axpy")


# =========================
# _build_candidates
# =========================


def test_build_candidates():
    """絶対と相対の 2 件（正常系）。"""
    # 実行
    candidates = _build_candidates("/repo/docs/wiki/規約.md", BASE)
    # 検証
    assert candidates == ["/repo/docs/wiki/規約.md", "docs/wiki/規約.md"]


def test_build_candidates_when_outside_base():
    """基準外のパス（正常系）。"""
    # 実行
    candidates = _build_candidates("/other/a.md", BASE)
    # 検証: 相対パスが求められないので絶対パスだけ
    assert candidates == ["/other/a.md"]
