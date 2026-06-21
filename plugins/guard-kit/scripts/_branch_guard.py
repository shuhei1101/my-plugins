"""guard-kit プラグイン scripts 共通: 保護ブランチ実行ガード。

cwd が master / main / develop のときに stderr へ日本語メッセージを出して exit 1 する。
状態書き換え系スクリプト (`index-tool.py` / `issue-tool.py` / `trim-index.py`) の
`main()` 先頭から `assert_not_protected_branch()` を呼ぶ前提。

判定は cwd で `git branch --show-current` を実行するため、MCP server 経由
(`cwd=CLAUDE_PROJECT_DIR`) でも CLI 直叩きでも同じ結果になる。
"""

from __future__ import annotations

import subprocess
import sys

PROTECTED_BRANCHES = frozenset({"master", "main", "develop"})


def _current_branch() -> str | None:
    """cwd の git ブランチ名を返す。git 不在やリポジトリ外なら None。"""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def assert_not_protected_branch(script_label: str | None = None) -> None:
    """保護ブランチ上なら exit 1 で停止する。それ以外（git 外含む）は何もしない。"""
    branch = _current_branch()
    if branch is None or branch not in PROTECTED_BRANCHES:
        return

    label = f"`{script_label}` " if script_label else ""
    print(
        f"ERROR: 保護ブランチ '{branch}' 上では {label}を実行できません。\n"
        "`worktree_create` MCP（gh-kit-tools）でブランチとワークツリーを作成し、そこから実行してください。",
        file=sys.stderr,
    )
    sys.exit(1)
