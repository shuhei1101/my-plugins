"""
stop.py — work-kit の Stop フック

応答完了時に未完了タスクの更新を Claude に促す。
現在の PR に未チェックのタスクがあれば context にリマインドを注入する。
部分的な作業中の無限ループを避けるため decision: block は使用しない。

使い方:
  Claude Code フックから自動で呼び出される。直接実行しない。

  入力  (stdin): Claude Code が送る JSON（Stop イベント）
  出力 (stdout): hookSpecificOutput.additionalContext を含む JSON、またはなし
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

# ── main ────────────────────────────────────────────────────
def main() -> None:
    """メイン処理。未完了タスクがあれば context にリマインドを注入する。"""
    try:
        json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    branch = _get_git_branch()
    if branch is None:
        sys.exit(0)

    m = re.match(r"PR(\d+)/", branch)
    if not m:
        sys.exit(0)

    pr_num = m.group(1)
    pr_doc_path = _find_pr_doc(pr_num)
    if pr_doc_path is None:
        sys.exit(0)

    pr_doc = pr_doc_path.read_text(encoding="utf-8")
    unchecked = re.findall(r"^- \[ \] .+", pr_doc, re.MULTILINE)
    if not unchecked:
        sys.exit(0)

    items = "\n".join(unchecked)
    context = (
        f"[work-kit] PR{pr_num} has {len(unchecked)} unchecked task(s). "
        f"Mark completed ones as `- [x]` in the PR doc before finishing.\n{items}"
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "additionalContext": context,
        }
    }))


if __name__ == "__main__":
    main()
