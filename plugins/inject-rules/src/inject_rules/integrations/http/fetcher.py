"""場所からのテキスト取得。"""
from __future__ import annotations

import re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import quote
from urllib.request import urlopen

FETCH_TIMEOUT_SEC = 10
REMOTE_SCHEMES = ("http://", "https://")
RAW_HOST = "raw.githubusercontent.com"
SAFE_URL_CHARS = ":/?#[]@!$&'()*+,;=%~"
FRONT_MATTER_RE = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)
BLOB_RE = re.compile(r"\Ahttps://github\.com/([^/]+)/([^/]+)/blob/(.+)\Z")
WIKI_RE = re.compile(r"\Ahttps://github\.com/([^/]+)/([^/]+)/wiki/(.+)\Z")
TAG_RE = re.compile(r"<[^>]*>")
SKIP_TAGS = frozenset({"script", "style", "noscript", "head"})
BLANK_LINES_RE = re.compile(r"\n{3,}")


def fetch_text(location: str, *, timeout: int = FETCH_TIMEOUT_SEC) -> str:
    """場所から本文テキストを取得する。"""
    # ローカルの場所はファイルとして読む（raw 配信と同じくフロントマターを落とす）
    if not location.startswith(REMOTE_SCHEMES):
        text = Path(location).read_text(encoding="utf-8")
        return FRONT_MATTER_RE.sub("", text).strip()
    target = _normalize_url(location)
    # 日本語パスをそのまま渡すと urlopen が扱えないためエンコードする
    encoded = quote(target, safe=SAFE_URL_CHARS)
    with urlopen(encoded, timeout=timeout) as response:
        raw = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        content_type = response.headers.get_content_type()
    text = raw.decode(charset, errors="replace")

    # raw 配信のドキュメントは先頭にフロントマターが付く
    if RAW_HOST in target:
        return FRONT_MATTER_RE.sub("", text).strip()
    # HTML で配信されているページはタグを落として本文だけ取り出す
    if content_type == "text/html":
        return _html_to_text(text)
    return text.strip()


def _normalize_url(url: str) -> str:
    """GitHub の閲覧 URL を raw URL に変換する。"""
    blob = BLOB_RE.match(url)
    if blob:
        owner, repo, rest = blob.groups()
        return f"https://{RAW_HOST}/{owner}/{repo}/{rest}"
    wiki = WIKI_RE.match(url)
    if wiki:
        owner, repo, page = wiki.groups()
        return f"https://{RAW_HOST}/wiki/{owner}/{repo}/{page}.md"
    return url


def _html_to_text(html: str) -> str:
    """HTML からテキストノードだけを取り出す。"""

    class _TextExtractor(HTMLParser):
        """テキストノードを集めるパーサ。"""

        def __init__(self) -> None:
            super().__init__(convert_charrefs=True)
            self.chunks: list[str] = []
            self.skip_depth = 0

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            if tag in SKIP_TAGS:
                self.skip_depth += 1

        def handle_endtag(self, tag: str) -> None:
            if tag in SKIP_TAGS and self.skip_depth > 0:
                self.skip_depth -= 1

        def handle_data(self, data: str) -> None:
            # 捨てる要素の中身は本文に混ぜない
            if self.skip_depth == 0:
                self.chunks.append(data)

    parser = _TextExtractor()
    try:
        parser.feed(html)
        parser.close()
        collected = "".join(parser.chunks)
    except Exception:
        # 解析できない HTML はタグを単純に除去して読める形にする
        collected = TAG_RE.sub("", html)

    lines = [line.strip() for line in collected.splitlines()]
    return BLANK_LINES_RE.sub("\n\n", "\n".join(lines)).strip()
