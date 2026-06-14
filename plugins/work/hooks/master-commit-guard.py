"""workspace / master-commit-guard — PreToolUse(Bash) hook.

`git commit` / `git add` を `master` / `main` / `develop` ブランチ上で実行しようとしたとき、
完全にブロックする（再実行しても通らない）。

検出ロジック:
- `git commit` / `git add`、または `git -C <path> commit/add` を検出
- 対応する作業ディレクトリの `branch --show-current` を取得し、
  保護ブランチ (`master` / `main` / `develop`) のときだけ発火
- マージ中 (`MERGE_HEAD` 存在) は通過 — マージコミット完成・コンフリクト解消ステージングを阻まないため
- staged ファイルが全て `.gitignore` 対象の場合は通過 — gitignore ファイルのみのコミットは許可
- env `WORK_ALLOW_MASTER_COMMIT` が truthy なら通過 — 例外作業用の明示的な解除手段
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

# env `WORK_PROTECTED_BRANCHES` でカンマ区切り上書き可（空要素は除外）。
# 未設定時はデフォルト `master,main,develop` で完全な後方互換。
PROTECTED_BRANCHES = tuple(
    b.strip()
    for b in os.environ.get("WORK_PROTECTED_BRANCHES", "master,main,develop").split(",")
    if b.strip()
)


def _all_staged_files_are_gitignored(git_args: list[str]) -> bool:
    """staged されている全ファイルが gitignore 対象かどうかを返す。"""
    # staged ファイルの一覧を取得
    staged_proc = subprocess.run(
        git_args + ["diff", "--name-only", "--cached"],
        capture_output=True,
        text=True,
    )
    if staged_proc.returncode != 0:
        return False

    staged_files = [f for f in staged_proc.stdout.strip().splitlines() if f]

    # staged ファイルが空なら git commit 自体が失敗するのでガード不要
    if not staged_files:
        return False

    # 全ファイルが gitignore 対象か確認（1 つでも対象外があればガードする）
    for file in staged_files:
        check_proc = subprocess.run(
            git_args + ["check-ignore", "-q", file],
            capture_output=True,
        )
        # returncode が 0 以外 = gitignore 対象外ファイルが存在する
        if check_proc.returncode != 0:
            return False

    return True


def _git_dir_from_command(command: str) -> str | None:
    """コマンド文字列から git の対象作業ディレクトリを抜き出す。

    優先順位:
        1. `git -C <path> <commit|add> ...`
        2. `cd <path>; git <commit|add> ...` / `cd <path> && git <commit|add> ...`
        3. なし (= 現在の cwd)
    """
    # パターン1: `git -C <path> <commit|add>` 形式
    m = re.search(r"\bgit\s+-C\s+(\S+)\s+(?:commit|add)\b", command)
    if m:
        return m.group(1)
    # パターン2: セミコロン / && / | の前後にある `cd <path>` 形式
    m = re.search(r"(?:^|[;&|])\s*cd\s+(\S+)", command)
    if m:
        return m.group(1)
    return None


def main() -> None:
    payload = json.loads(sys.stdin.read())
    command = payload.get("tool_input", {}).get("command", "")

    # git commit / git add を含まないコマンドはスキップ
    is_commit = bool(re.search(r"\bgit(\s+-C\s+\S+)?\s+commit\b", command))
    is_add = bool(re.search(r"\bgit(\s+-C\s+\S+)?\s+add\b", command))
    if not (is_commit or is_add):
        return

    # コマンド文字列から作業ディレクトリを特定して git コマンドを組み立て
    git_dir = _git_dir_from_command(command)
    git_args = (
        ["git", "-C", os.path.normpath(os.path.join(os.getcwd(), git_dir))]
        if git_dir
        else ["git"]
    )

    # 現在のブランチを取得し、保護対象でなければスキップ
    branch_proc = subprocess.run(
        git_args + ["branch", "--show-current"],
        capture_output=True,
        text=True,
    )
    if branch_proc.returncode != 0 or branch_proc.stdout.strip() not in PROTECTED_BRANCHES:
        return

    # マージコミット完成中はブロックしない（コンフリクト解消ステージングとコミットを阻害しないため）
    merge_proc = subprocess.run(
        git_args + ["rev-parse", "--verify", "MERGE_HEAD"],
        capture_output=True,
    )
    if merge_proc.returncode == 0:
        return

    # staged ファイルが全て gitignore 対象なら通過（gitignore 済みファイルのみのコミットは許可）
    if _all_staged_files_are_gitignored(git_args):
        return

    # 明示的な解除手段: 例外的に保護ブランチへ直接操作したいときだけ env で許可する
    if os.environ.get("WORK_ALLOW_MASTER_COMMIT", "").strip().lower() in {"true", "1", "yes", "on"}:
        return

    # プロンプト本文を読み込み、git status を末尾に追記してブロック理由とする
    prompt_path = pathlib.Path(sys.argv[1])
    base = prompt_path.read_text("utf-8") if prompt_path.exists() else ""

    status_proc = subprocess.run(git_args + ["status"], capture_output=True, text=True)
    status_out = (
        status_proc.stdout.strip() if status_proc.returncode == 0 else "(git status failed)"
    )

    reason = base + "\n\n---\n\ngit status:\n\n```\n" + status_out + "\n```"
    sys.stdout.buffer.write(
        json.dumps({"decision": "block", "additionalContext": reason}, ensure_ascii=False).encode("utf-8")
    )


if __name__ == "__main__":
    main()
