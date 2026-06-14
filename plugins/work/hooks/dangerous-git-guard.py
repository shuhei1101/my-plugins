"""workspace / dangerous-git-guard — PreToolUse(Bash) hook.

危険な git コマンドを永久ブロックする（再実行しても通らない）。

検出対象:
    1. `git worktree remove --force` / `-f` — 強制削除で in-progress 作業が消える
    2. `git rm` で重要ファイルを対象にしたコマンド
       （.gitignore / .gitattributes / .claude/** が引数に含まれる）
    3. `git checkout -- <path>` / `git restore --worktree <path>` で
       重要ファイル（.gitignore / .gitattributes / .claude/**）を対象にしたコマンド
    4. `git merge -X ours` / `git merge -X theirs` / `--strategy-option=ours` 等の
       自動コンフリクト解消オプション（事故の元）

Args:
    sys.argv[1]: ブロックメッセージの Markdown ファイルパス
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

# 危険コマンドのパターンと、それぞれの理由
_DANGEROUS_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"\bgit\s+worktree\s+remove\b[^\n]*\s(?:--force|-f)\b"),
        "git worktree remove --force",
    ),
    (
        re.compile(
            r"\bgit\s+rm\b[^\n]*(?:\s|/|^)(?:\.gitignore|\.gitattributes|\.claude/)"
        ),
        "git rm で重要ファイル（.gitignore / .gitattributes / .claude/）を削除",
    ),
    (
        re.compile(
            r"\bgit\s+(?:checkout|restore)\b[^\n]*(?:\s|/|^)(?:\.gitignore|\.gitattributes|\.claude/)"
        ),
        "git checkout/restore で重要ファイル（.gitignore / .gitattributes / .claude/）を上書き",
    ),
    (
        re.compile(
            r"\bgit\s+merge\b[^\n]*\s(?:-X\s*(?:ours|theirs)|--strategy-option[= ](?:ours|theirs))\b"
        ),
        "git merge -X ours/theirs（自動コンフリクト解消は事故の元）",
    ),
    (
        re.compile(r"\bgit\s+(?:checkout|merge)\b[^\n]*\s--(?:ours|theirs)\b"),
        "git checkout/merge --ours/--theirs（自動コンフリクト解消は事故の元）",
    ),
]


def main() -> None:
    """危険 git コマンドのブロック処理。"""
    payload = json.loads(sys.stdin.read())
    command = payload.get("tool_input", {}).get("command", "")

    for pattern, reason in _DANGEROUS_PATTERNS:
        if pattern.search(command):
            prompt_path = pathlib.Path(sys.argv[1])
            base = prompt_path.read_text("utf-8") if prompt_path.exists() else ""
            context = base + f"\n\n検出: {reason}"
            sys.stdout.buffer.write(
                json.dumps(
                    {"decision": "block", "additionalContext": context},
                    ensure_ascii=False,
                ).encode("utf-8")
            )
            return


if __name__ == "__main__":
    main()
