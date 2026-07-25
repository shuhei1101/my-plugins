"""`shared/settings.py` の単体テスト。"""
from __future__ import annotations

from pathlib import Path

from inject_rules.shared.settings import Settings

ENV_NAMES = (
    "INJECT_RULES_INDEXES",
    "INJECT_RULES_OTLP_ENDPOINT",
    "INJECT_RULES_CACHE_DIR",
    "INJECT_RULES_SESSION_DIR",
)


def test_from_env(monkeypatch):
    """環境変数の反映（正常系）。"""
    # 準備
    monkeypatch.setenv("INJECT_RULES_INDEXES", "https://example.com/rules.yaml")
    monkeypatch.setenv("INJECT_RULES_OTLP_ENDPOINT", "http://collector:4317")
    monkeypatch.setenv("INJECT_RULES_CACHE_DIR", "/tmp/cache")
    monkeypatch.setenv("INJECT_RULES_SESSION_DIR", "/tmp/session")
    # 実行
    settings = Settings.from_env()
    # 検証
    assert settings.index_urls == ("https://example.com/rules.yaml",)
    assert settings.otlp_endpoint == "http://collector:4317"
    assert settings.cache_dir == Path("/tmp/cache")
    assert settings.session_dir == Path("/tmp/session")


def test_from_env_when_unset(monkeypatch):
    """未設定時の既定値（正常系）。"""
    # 準備
    for name in ENV_NAMES:
        monkeypatch.delenv(name, raising=False)
    # 実行
    settings = Settings.from_env()
    # 検証
    assert settings.index_urls == ()
    assert settings.otlp_endpoint == "http://localhost:4317"
    assert settings.cache_dir == Path.home() / ".cache" / "inject-rules"
    assert settings.session_dir == Path.home() / ".claude" / "tokens" / "inject-rules"


def test_from_env_when_multiple_indexes(monkeypatch):
    """カンマ区切りの分割（正常系）。"""
    # 準備
    monkeypatch.setenv("INJECT_RULES_INDEXES", "https://example.com/a.yaml,https://example.com/b.yaml")
    # 実行
    settings = Settings.from_env()
    # 検証
    assert settings.index_urls == ("https://example.com/a.yaml", "https://example.com/b.yaml")


def test_from_env_when_spaces(monkeypatch):
    """空白と空要素の除去（正常系）。"""
    # 準備
    monkeypatch.setenv("INJECT_RULES_INDEXES", "https://example.com/a.yaml, ,https://example.com/b.yaml")
    # 実行
    settings = Settings.from_env()
    # 検証: 空要素は落ちる
    assert settings.index_urls == ("https://example.com/a.yaml", "https://example.com/b.yaml")
