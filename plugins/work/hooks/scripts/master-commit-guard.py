"""workspace / master-commit-guard — PreToolUse(Bash) hook.

`git commit` を `master` / `main` / `develop` ブランチ上で実行しようとしたとき、
プロンプト注入 (`decision: block`) でユーザーに確認を求める。

検出ロジック:
- `git commit` または `git -C <path> commit` を検出
- 対応する作業ディレクトリの `branch --show-current` を取得し、
  保護ブランチ (`master` / `main` / `develop`) のときだけ発火
- マージ中 (`MERGE_HEAD` 存在) は通過 — マージコミットの完成を阻まないため
- ループ防止: 一時トークンファイルで 1 回ブロックしたら 2 回目以降は素通り
- block 時の `reason` には `git status` の出力を追記し、何が staged/unstaged かを
  そのまま Claude に見せる

Args:
    sys.argv[1]: プロンプト本文の Markdown ファイルパス
                 （hooks.json から `${CLAUDE_PLUGIN_ROOT}/hooks/prompts/master-commit-guard.md` を渡す）
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

# env `WORK_PROTECTED_BRANCHES` でカンマ区切り上書き可（空要素は除外）。
# 未設定時はデフォルト `master,main,develop` で完全な後方互換。
PROTECTED_BRANCHES = tuple(
    b.strip()
    for b in os.environ.get("WORK_PROTECTED_BRANCHES", "master,main,develop").split(",")
    if b.strip()
)


def _git_dir_from_command(command: str) -> str | None:
    """コマンド文字列から git の対象作業ディレクトリを抜き出す。

    優先順位:
        1. `git -C <path> commit ...`
        2. `cd <path>; git commit ...` / `cd <path> && git commit ...`
        3. なし (= 現在の cwd)
    """
    m = re.search(r"\bgit\s+-C\s+(\S+)\s+commit\b", command)
    if m:
        return m.group(1)
    m = re.search(r"(?:^|[;&|])\s*cd\s+(\S+)", command)
    if m:
        return m.group(1)
    return None


def main() -> None:
    payload = json.loads(sys.stdin.read())
    command = payload.get("tool_input", {}).get("command", "")

    if not re.search(r"\bgit(\s+-C\s+\S+)?\s+commit\b", command):
        return

    git_dir = _git_dir_from_command(command)
    git_args = (
        ["git", "-C", os.path.normpath(os.path.join(os.getcwd(), git_dir))]
        if git_dir
        else ["git"]
    )

    branch_proc = subprocess.run(
        git_args + ["branch", "--show-current"],
        capture_output=True,
        text=True,
    )
    if branch_proc.returncode != 0 or branch_proc.stdout.strip() not in PROTECTED_BRANCHES:
        return

    merge_proc = subprocess.run(
        git_args + ["rev-parse", "--verify", "MERGE_HEAD"],
        capture_output=True,
    )
    if merge_proc.returncode == 0:
        return

    session_id = payload.get("session_id", "default")
    token = pathlib.Path(tempfile.gettempdir()) / f"workspace-master-commit-guard-{session_id}"
    if token.exists():
        token.unlink()
        return
    token.touch()

    prompt_path = pathlib.Path(sys.argv[1])
    base = prompt_path.read_text("utf-8") if prompt_path.exists() else ""

    status_proc = subprocess.run(git_args + ["status"], capture_output=True, text=True)
    status_out = (
        status_proc.stdout.strip() if status_proc.returncode == 0 else "(git status failed)"
    )

    reason = base + "\n\n---\n\n**git status:**\n\n```\n" + status_out + "\n```"
    sys.stdout.buffer.write(
        json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False).encode("utf-8")
    )


if __name__ == "__main__":
    main()
