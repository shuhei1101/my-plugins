"""
user-prompt-submit.py — UserPromptSubmit hook for work-kit

Injects the current PR's task status into Claude's context on every prompt.
- In a PR worktree (branch matches PR{N}/...): injects task checklist from the PR doc.
- On main branch: reminds to create a worktree for new work.

Usage:
  Installed and invoked automatically by Claude Code hooks. Do not run manually.

  Input  (stdin): JSON object sent by Claude Code (UserPromptSubmit event)
  Output (stdout): JSON with hookSpecificOutput.additionalContext
"""

# ── stdlib ──────────────────────────────────────────────────
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ── private helpers ─────────────────────────────────────────
def _get_git_branch() -> Optional[str]:
    """
    カレントディレクトリの Git ブランチ名を返す。

    :return: ブランチ名。取得失敗時は None
    """
    try:
        return subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=5,
        ).strip()
    except Exception:
        return None


def _find_pr_doc(pr_num: str) -> Optional[Path]:
    """
    PR 番号に対応する PR ドキュメントのパスを返す。

    :param pr_num: PR 番号（文字列）
    :return: PR ドキュメントのパス。見つからない場合は None
    """
    matches = list(Path.cwd().glob(f"docs/tasks/**/PR{pr_num}.md"))
    return matches[0] if matches else None


def _extract_task_section(pr_doc: str) -> str:
    """
    PR ドキュメントから「作業内容」セクションを抽出する。

    :param pr_doc: PR ドキュメントの全文
    :return: 作業内容セクション。見つからない場合は全文
    """
    m = re.search(
        r"(## 作業内容\n(?:(?!^## ).)*)",
        pr_doc,
        re.MULTILINE | re.DOTALL,
    )
    return m.group(1).strip() if m else pr_doc.strip()


def _emit(context: str) -> None:
    """
    additionalContext を含む JSON を stdout に出力する。

    :param context: Claude に注入するコンテキスト文字列
    """
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))

# ── main ────────────────────────────────────────────────────
def main() -> None:
    """メイン処理。stdin の JSON を読み、PR タスク状況を context に注入する。"""
    try:
        json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    branch = _get_git_branch()
    if branch is None:
        sys.exit(0)

    m = re.match(r"PR(\d+)/", branch)
    if not m:
        _emit("[work-kit] On main branch. If starting new work, create a worktree with /wt:wt.")
        sys.exit(0)

    pr_num = m.group(1)
    pr_doc_path = _find_pr_doc(pr_num)
    if pr_doc_path is None:
        sys.exit(0)

    pr_doc = pr_doc_path.read_text(encoding="utf-8")
    tasks = _extract_task_section(pr_doc)
    _emit(f"[PR{pr_num} task status]\n{tasks}")


if __name__ == "__main__":
    main()
