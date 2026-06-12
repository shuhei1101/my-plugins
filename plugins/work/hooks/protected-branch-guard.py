"""保護ブランチへの直接ファイル編集を検出してブロックするフック。

PreToolUse フックとして動作し、main/master/develop ブランチへの
Edit・Write ツール呼び出しを阻止して /work:start の使用を促す。

Usage:
python protected_branch_guard.py
# stdin に PreToolUse フックの JSON を渡す
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

PROTECTED_BRANCHES = {"main", "master", "develop"}


def get_git_branch(path: str) -> str:
    """指定パスが属する git リポジトリの現在ブランチ名を返す。"""
    result = subprocess.run(
        ["git", "-C", path, "branch", "--show-current"],
        capture_output=True,
        text=True,
        timeout=5,
    )
    return result.stdout.strip()


def resolve_check_dir(data: dict) -> str:
    """ブランチチェック対象ディレクトリを決定する。"""
    file_path = data.get("tool_input", {}).get("file_path", "")
    if file_path:
        # ファイルパスの親ディレクトリを優先（存在しない場合は cwd にフォールバック）
        parent = os.path.dirname(os.path.abspath(file_path))
        if os.path.exists(parent):
            return parent
    return data.get("cwd", ".")


def build_deny_output(branch: str) -> dict:
    """ブロック用の JSON 出力を構築する。"""
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"保護ブランチ '{branch}' への直接ファイル編集はブロックされました。\n\n"
                "このワークキットでは main/master/develop ブランチへの直接編集は禁止されています。\n"
                "必ず /work:start スキルを使用してワークツリーを作成し、そこで作業を行ってください。\n\n"
                "ユーザーに以下を日本語で伝えてください：\n"
                f"「{branch} ブランチへの直接編集はできません。"
                "/work:start を実行してワークツリーを作成してから作業を開始してください。」"
            ),
            "additionalContext": (
                f"保護ブランチ '{branch}' への直接編集がブロックされました。\n"
                "- 禁止理由: このプロジェクトはワークツリーを使った分離作業を必須としています\n"
                "- 対処法: `/work:start` スキルを実行してブランチとワークツリーを作成する\n"
                "- ワークツリー作成後は、そのパスで自由にファイルを編集できます"
            ),
        }
    }


def main() -> int:
    """フックのエントリーポイント。ブランチを確認し必要に応じてブロックする。"""
    data = json.load(sys.stdin)

    check_dir = resolve_check_dir(data)

    try:
        branch = get_git_branch(check_dir)
    except Exception:
        # git コマンド失敗時はスルー（git 未インストール、git リポジトリ外など）
        return 0

    # 保護ブランチ以外はそのまま通過
    if branch not in PROTECTED_BRANCHES:
        return 0

    # 保護ブランチへの編集をブロック
    print(json.dumps(build_deny_output(branch), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
