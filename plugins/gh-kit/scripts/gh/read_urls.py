"""指定 URL のコンテンツを取得して標準出力に返す。

GitHub blob URL は raw.githubusercontent.com に変換してから取得する。
複数 URL を指定した場合は順番に取得して出力する。

# 使い方
python read_urls.py <URL> [<URL> ...]
"""
from __future__ import annotations

import sys
import urllib.request

from utils import normalize_github_url


def main() -> int:
    if len(sys.argv) < 2:
        print("使い方: python read_urls.py <URL> [<URL> ...]", file=sys.stderr)
        return 1

    exit_code = 0
    for raw_url in sys.argv[1:]:
        url = normalize_github_url(raw_url)
        try:
            with urllib.request.urlopen(url) as resp:
                print(resp.read().decode("utf-8"))
        except Exception:
            import traceback
            traceback.print_exc()
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
