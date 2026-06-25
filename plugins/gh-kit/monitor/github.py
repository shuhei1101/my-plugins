from __future__ import annotations

import json
import subprocess
from functools import lru_cache

from utils import log


@lru_cache(maxsize=1)
def current_login() -> str | None:
    """ログイン中の GitHub ユーザー名を取得する。失敗時は None。"""
    result = subprocess.run(
        ["gh", "api", "user", "--jq", ".login"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        log(f"WARN: gh api user が失敗しました (exit={result.returncode}): {result.stderr.strip()}")
        return None
    return result.stdout.strip() or None


def list_issues(label: str) -> list[dict]:
    """指定ラベル付きの open Issue を取得する。失敗時は空リストを返す。

    ユーザー自身が assignee に入っている Issue は「ユーザー確認待ち」と見なし除外する。
    """
    result = subprocess.run(
        [
            "gh", "issue", "list",
            "--state", "open",
            "--label", label,
            "--json", "number,labels,assignees",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        log(f"WARN: gh issue list が失敗しました (exit={result.returncode}): {result.stderr.strip()}")
        log("  git リポジトリ内で実行してください")
        return []
    issues = json.loads(result.stdout)
    login = current_login()
    if login is None:
        return issues
    return [
        issue for issue in issues
        if not any(a.get("login") == login for a in issue.get("assignees", []))
    ]


def add_label(issue_number: int, label: str) -> bool:
    """Issue にラベルを付与し、成功なら True を返す。"""
    return subprocess.run(
        ["gh", "issue", "edit", str(issue_number), "--add-label", label],
        capture_output=True,
    ).returncode == 0


def remove_label(issue_number: int, label: str) -> None:
    """Issue からラベルを除去する（失敗は無視）。"""
    subprocess.run(
        ["gh", "issue", "edit", str(issue_number), "--remove-label", label],
        capture_output=True,
    )
