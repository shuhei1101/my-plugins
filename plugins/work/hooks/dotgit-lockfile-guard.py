"""workspace / dotgit-lockfile-guard — PreToolUse(Edit|Write) hook.

`.git/**` 配下、主要パッケージマネージャの lock ファイル、および
`.gitignore` / `.gitattributes` への Edit / Write を永久ブロックする
（再実行しても通らない）。Read はガードしない。

Args:
    sys.argv[1]: ブロックメッセージの Markdown ファイルパス
"""

from __future__ import annotations

import json
import os
import pathlib
import sys

# ブロック対象のロックファイル名（basename 完全一致）
# パッケージマネージャ CLI が自動更新する前提のため、Claude による直接編集を恒久禁止する
_LOCK_FILENAMES = frozenset(
    {
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "npm-shrinkwrap.json",
        "Cargo.lock",
        "Gemfile.lock",
        "Pipfile.lock",
        "poetry.lock",
        "uv.lock",
        "composer.lock",
        "go.sum",
    }
)

# Claude 由来の削除/上書き事故を恒久ブロックしたい dotfile（basename 完全一致）
# .gitignore を失うと tracked 不要なファイルが一気に working tree に湧くため
_PROTECTED_DOTFILES = frozenset({".gitignore", ".gitattributes"})


def _is_dotgit_path(file_path: str) -> bool:
    """パスに `.git` 成分が含まれるかを判定する。"""
    # Windows / POSIX どちらの区切りでもパス成分単位で判定するため正規化する
    normalized = file_path.replace("\\", "/")
    return ".git" in normalized.split("/")


def _is_lockfile_path(file_path: str) -> bool:
    """パスの basename がロックファイル一覧に該当するかを判定する。"""
    basename = os.path.basename(file_path.replace("\\", "/"))
    return basename in _LOCK_FILENAMES


def _is_protected_dotfile_path(file_path: str) -> bool:
    """パスの basename が保護対象 dotfile (`.gitignore` 等) と完全一致するかを判定する。"""
    basename = os.path.basename(file_path.replace("\\", "/"))
    return basename in _PROTECTED_DOTFILES


def _build_block_output(reason: str, context: str) -> dict:
    """PreToolUse の deny 出力を構築する。"""
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
            "additionalContext": context,
        }
    }


def main() -> int:
    """フックのエントリーポイント。.git / lock ファイル / 保護 dotfile への Edit/Write をブロックする。"""
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    # 対象パスがなければスルー
    if not file_path:
        return 0

    # .git 配下、ロックファイル、保護 dotfile (.gitignore/.gitattributes) のいずれかにマッチしたら永久ブロック
    if _is_dotgit_path(file_path):
        target_label = ".git/** 配下のファイル"
    elif _is_lockfile_path(file_path):
        target_label = f"ロックファイル ({os.path.basename(file_path)})"
    elif _is_protected_dotfile_path(file_path):
        target_label = f"保護 dotfile ({os.path.basename(file_path)})"
    else:
        # 対象外パスは通過
        return 0

    prompt_path = pathlib.Path(sys.argv[1])
    context = (
        prompt_path.read_text("utf-8")
        if prompt_path.exists()
        else f"{target_label} への Edit/Write はブロックされています。"
    )

    reason = (
        f"{target_label} への Edit/Write はブロックされました。\n"
        ".git は Git CLI 経由でのみ、lock ファイルはパッケージマネージャ CLI 経由でのみ、"
        ".gitignore / .gitattributes はユーザー手動でのみ更新してください。"
    )

    print(json.dumps(_build_block_output(reason, context), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
