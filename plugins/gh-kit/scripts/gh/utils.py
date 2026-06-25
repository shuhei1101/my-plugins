from __future__ import annotations

import re


def normalize_github_url(url: str) -> str:
    """github.com/{owner}/{repo}/blob/{rest} を raw.githubusercontent.com の URL に変換する。

    マッチしなければ url をそのまま返す。
    """
    m = re.match(
        r"^https?://(?:www\.)?github\.com/([^/]+)/([^/]+)/blob/(.+)$",
        url,
    )
    if not m:
        return url
    owner, repo, rest = m.group(1), m.group(2), m.group(3)
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{rest}"
