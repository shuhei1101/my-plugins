"""`integrations/http/fetcher.py` の単体テスト。"""
from __future__ import annotations

import email.message
import urllib.error

import pytest

from inject_rules.integrations.http.fetcher import _html_to_text, _normalize_url, fetch_text

URLOPEN_PATH = "inject_rules.integrations.http.fetcher.urlopen"
PLAIN_URL = "https://example.com/rules.yaml"
RAW_URL = "https://raw.githubusercontent.com/owner/repo/master/docs/a.md"


class _StubResponse:
    """urlopen の戻り値を模した応答。"""

    def __init__(self, body: str, *, content_type: str):
        self._body = body.encode("utf-8")
        self.headers = email.message.Message()
        self.headers["Content-Type"] = f"{content_type}; charset=utf-8"

    def __enter__(self) -> _StubResponse:
        return self

    def __exit__(self, *args: object) -> bool:
        return False

    def read(self) -> bytes:
        return self._body


def _make_urlopen(body: str = "", *, content_type: str = "text/plain", error: Exception | None = None):
    """要求 URL を記録する urlopen スタブを作る。"""
    calls: list[str] = []

    def _urlopen(url: str, timeout: int | None = None) -> _StubResponse:
        calls.append(url)
        if error is not None:
            raise error
        return _StubResponse(body, content_type=content_type)

    _urlopen.calls = calls  # type: ignore[attr-defined]
    return _urlopen


# =========================
# fetch_text
# =========================


def test_fetch_text(monkeypatch):
    """プレーンテキストの取得（正常系）。"""
    # 準備
    monkeypatch.setattr(URLOPEN_PATH, _make_urlopen("rules:\n  - url: https://example.com/a.md\n"))
    # 実行
    text = fetch_text(PLAIN_URL)
    # 検証
    assert text == "rules:\n  - url: https://example.com/a.md"


def test_fetch_text_when_raw_github(monkeypatch):
    """フロントマターの除去（正常系）。"""
    # 準備: 先頭にフロントマターを持つ本文
    body = "---\ntemplate_version: 1.0.0\n---\n\n# 命名規約\n本文\n"
    monkeypatch.setattr(URLOPEN_PATH, _make_urlopen(body))
    # 実行
    text = fetch_text(RAW_URL)
    # 検証
    assert text.startswith("# 命名規約")
    assert "template_version" not in text


def test_fetch_text_when_html(monkeypatch):
    """HTML のテキスト抽出（正常系）。"""
    # 準備
    body = "<html><body><p>本文</p></body></html>"
    monkeypatch.setattr(URLOPEN_PATH, _make_urlopen(body, content_type="text/html"))
    # 実行
    text = fetch_text("https://example.com/page")
    # 検証: タグが除かれる
    assert text == "本文"


def test_fetch_text_when_non_ascii_url(monkeypatch):
    """日本語 URL の取得（正常系）。"""
    # 準備
    urlopen = _make_urlopen("本文")
    monkeypatch.setattr(URLOPEN_PATH, urlopen)
    # 実行
    fetch_text("https://example.com/規約/コメント.md")
    # 検証: エンコード済み URL で要求される
    requested = urlopen.calls[0]
    assert requested.isascii()
    assert "%E8%A6%8F%E7%B4%84" in requested


def test_fetch_text_when_local_path(tmp_path, monkeypatch):
    """ローカルファイルの読み込み（正常系）。"""
    # 準備
    urlopen = _make_urlopen("")
    monkeypatch.setattr(URLOPEN_PATH, urlopen)
    path = tmp_path / "命名規則.md"
    path.write_text("# 命名規約\n本文\n", encoding="utf-8")
    # 実行
    text = fetch_text(str(path))
    # 検証: ファイルの本文が返り、HTTP 取得が発生しない
    assert text == "# 命名規約\n本文"
    assert urlopen.calls == []


def test_fetch_text_when_local_front_matter(tmp_path, monkeypatch):
    """ローカルのフロントマター除去（正常系）。"""
    # 準備
    monkeypatch.setattr(URLOPEN_PATH, _make_urlopen(""))
    path = tmp_path / "a.md"
    path.write_text("---\ntemplate_version: 1.0.0\n---\n\n# 命名規約\n本文\n", encoding="utf-8")
    # 実行
    text = fetch_text(str(path))
    # 検証: raw 配信と同じ扱いになる
    assert text.startswith("# 命名規約")
    assert "template_version" not in text


def test_fetch_text_when_unreachable(monkeypatch):
    """取得失敗（異常系）。"""
    # 準備
    monkeypatch.setattr(URLOPEN_PATH, _make_urlopen(error=urllib.error.URLError("接続できません")))
    # 実行・検証
    with pytest.raises(urllib.error.URLError):
        fetch_text(PLAIN_URL)


def test_fetch_text_when_local_missing(tmp_path, monkeypatch):
    """ローカルファイル不在（異常系）。"""
    # 準備
    monkeypatch.setattr(URLOPEN_PATH, _make_urlopen(""))
    # 実行・検証
    with pytest.raises(OSError):
        fetch_text(str(tmp_path / "存在しない.md"))


# =========================
# _normalize_url
# =========================


def test_normalize_url_when_blob():
    """blob URL の変換（正常系）。"""
    # 実行
    url = _normalize_url("https://github.com/owner/repo/blob/master/docs/a.md")
    # 検証
    assert url == "https://raw.githubusercontent.com/owner/repo/master/docs/a.md"


def test_normalize_url_when_wiki():
    """Wiki URL の変換（正常系）。"""
    # 実行
    url = _normalize_url("https://github.com/owner/repo/wiki/Page")
    # 検証: raw URL に .md が補完される
    assert url == "https://raw.githubusercontent.com/wiki/owner/repo/Page.md"


def test_normalize_url_when_raw():
    """raw URL の素通し（正常系）。"""
    # 実行・検証
    assert _normalize_url(RAW_URL) == RAW_URL


def test_normalize_url_when_other_host():
    """他ホストの素通し（正常系）。"""
    # 実行・検証
    assert _normalize_url(PLAIN_URL) == PLAIN_URL


# =========================
# _html_to_text
# =========================


def test_html_to_text():
    """テキストの抽出（正常系）。"""
    # 実行
    text = _html_to_text("<html><body><p>1 段落目</p><p>2 段落目</p></body></html>")
    # 検証
    assert "1 段落目" in text
    assert "2 段落目" in text
    assert "<p>" not in text


def test_html_to_text_when_script():
    """script の除外（正常系）。"""
    # 実行
    text = _html_to_text("<html><body><script>alert('除外対象')</script><p>本文</p></body></html>")
    # 検証
    assert "本文" in text
    assert "除外対象" not in text


def test_html_to_text_when_broken():
    """壊れた HTML（正常系）。"""
    # 実行・検証: 閉じタグが欠けていても例外を投げずテキストが返る
    assert "本文" in _html_to_text("<html><body><p>本文")
