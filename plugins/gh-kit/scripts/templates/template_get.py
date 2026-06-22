"""template_get.py — GitHub Wiki からテンプレートを取得して stdout に出力する CLI。

使い方:
  python template_get.py <template_name>

template_name はテンプレートファイル名（拡張子込み）。
拡張子を除いた名前で Wiki ページを検索する（例: PRドキュメント.j2 → PRドキュメント）。

Wiki はリモート GitHub Wiki から curl で直接取得する。
GH_KIT_OWNER / GH_KIT_REPO 環境変数が未設定の場合は gh CLI から自動取得する。
取得できない場合は終了コード 2 でエラー終了する。
"""
from __future__ import annotations

import os
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path


def _get_repo_info() -> tuple[str, str]:
    """リポジトリのオーナーとリポジトリ名を取得する。

    優先順位:
    1. GH_KIT_OWNER / GH_KIT_REPO 環境変数
    2. gh CLI で現在のリポジトリ情報を取得
    """
    owner = os.environ.get("GH_KIT_OWNER", "").strip()
    repo = os.environ.get("GH_KIT_REPO", "").strip()

    if owner and repo:
        return owner, repo

    # gh CLI からリポジトリ情報を取得
    try:
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "owner,name", "--jq", ".owner.login + \"/\" + .name"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split("/", 1)
            if len(parts) == 2:
                return parts[0], parts[1]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return "", ""


def _fetch_wiki_page(owner: str, repo: str, page_name: str) -> str | None:
    """GitHub Wiki からページ内容を curl 相当で取得する。

    URL: https://raw.githubusercontent.com/wiki/{owner}/{repo}/{page_name}.md
    """
    url = f"https://raw.githubusercontent.com/wiki/{owner}/{repo}/{page_name}.md"

    # まず GITHUB_TOKEN / GH_TOKEN を使って認証付きで試みる
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or _get_gh_token()

    try:
        req = urllib.request.Request(url)
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    except urllib.error.URLError:
        return None


def _get_gh_token() -> str:
    """gh CLI から認証トークンを取得する。"""
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return ""


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("ERROR: 引数は template_name の 1 つだけ", file=sys.stderr)
        return 1

    name = argv[1]
    if "/" in name or ".." in name:
        print(f"ERROR: 不正なテンプレート名: {name}", file=sys.stderr)
        return 1

    # 拡張子を除いた Wiki ページ名を導出
    page_name = Path(name).stem  # 例: "PRドキュメント.j2" -> "PRドキュメント"

    # リポジトリ情報を取得
    owner, repo = _get_repo_info()
    if not owner or not repo:
        print(
            "ERROR: リポジトリ情報を取得できません。\n"
            "  GH_KIT_OWNER / GH_KIT_REPO 環境変数を設定するか、\n"
            "  gh CLI でリポジトリにアクセスできる状態にしてください。",
            file=sys.stderr,
        )
        return 2

    # リモート Wiki からページを取得
    content = _fetch_wiki_page(owner, repo, page_name)
    if content is None:
        print(
            f"ERROR: Wiki ページが見つかりません: {page_name}.md\n"
            f"  URL: https://raw.githubusercontent.com/wiki/{owner}/{repo}/{page_name}.md\n"
            f"  Wiki ページが存在するか確認してください。",
            file=sys.stderr,
        )
        return 2

    sys.stdout.write(content)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
