"""workspace / delete-guard — PreToolUse(Bash) hook.

`rm` または `rmdir` で重要ファイル/ディレクトリ（`.git` `.claude` `.gitignore`
`.gitattributes`、主要パッケージマネージャの lock ファイル）を削除しようとしたとき、
永久にブロックする（再実行しても通らない）。

ただし `.claude/worktrees/<branch>` 配下はワークツリー後片付けのため許可する。

Args:
    sys.argv[1]: ブロックメッセージの Markdown ファイルパス
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

# rm / rmdir コマンドの検出
_RM_PATTERN = re.compile(r"\b(?:rm|rmdir)\b")

# 削除を恒久ブロックするロックファイル名（basename 完全一致）
_LOCK_FILENAMES = (
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
)
_LOCKFILE_ALT = "|".join(re.escape(n) for n in _LOCK_FILENAMES)

# .claude/worktrees/<branch> パスを除去するパターン（worktree 後片付けを許可するため）
# \S* で前置パス（/abs/path/ や引用符など）も吸収し、\S+ で branch 名部分を要求する
_WORKTREE_PATH = re.compile(r"\S*\.claude/worktrees/\S+")

# 保護対象パターン:
#   .git / .claude — ディレクトリ（後ろに / か区切りが続く、または末尾）
#   .gitignore / .gitattributes — ファイル名そのもの（後ろに英数字が続かない＝完全一致）
#   lock ファイル — ファイル名完全一致（前後がパス区切り/空白/クォート）
_PROTECTED_PATH = re.compile(
    r"(?:^|[\s/\"\'\\])"
    r"\.(?:git|claude)(?:[/\s\"\'\\]|$)"
    r"|"
    r"(?:^|[\s/\"\'\\])"
    r"\.gitignore(?:[\s\"\'\\]|$)"
    r"|"
    r"(?:^|[\s/\"\'\\])"
    r"\.gitattributes(?:[\s\"\'\\]|$)"
    r"|"
    rf"(?:^|[\s/\"\'\\])(?:{_LOCKFILE_ALT})(?:[\s\"\'\\]|$)"
)


def main() -> None:
    """削除ガードのメイン処理。"""
    payload = json.loads(sys.stdin.read())
    command = payload.get("tool_input", {}).get("command", "")

    # rm / rmdir を含まないコマンドはスキップ
    if not _RM_PATTERN.search(command):
        return

    # .claude/worktrees/<branch> 部分を除去してからチェック
    # → worktrees 配下のみへの削除は保護対象から外れてスキップされる
    sanitized = _WORKTREE_PATH.sub("", command)

    # 保護対象パスが含まれていなければスキップ
    if not _PROTECTED_PATH.search(sanitized):
        return

    prompt_path = pathlib.Path(sys.argv[1])
    context = (
        prompt_path.read_text("utf-8")
        if prompt_path.exists()
        else ".git または .claude ディレクトリの削除はブロックされています。"
    )

    sys.stdout.buffer.write(
        json.dumps({"decision": "block", "additionalContext": context}, ensure_ascii=False).encode("utf-8")
    )


if __name__ == "__main__":
    main()
