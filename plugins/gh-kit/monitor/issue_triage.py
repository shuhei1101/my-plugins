from __future__ import annotations

import github
import settings
from claude_runner import run_claude_prompt
from utils import has_label_prefix, load_constants_sh, log, priority_rank

# constants.sh の定数をこのモジュールのトップレベルに注入
# （GH_KIT_LABEL_CONFIRM_ISSUE_TRIAGE 等が定数名そのままで使える）
load_constants_sh(globals())


def _find_next_issues() -> list[int]:
    """確認ラベル付きで処理中ではない Issue 番号を、優先度順にすべて返す（なければ空リスト）。"""
    issues = github.list_issues(GH_KIT_LABEL_CONFIRM_ISSUE_TRIAGE)  # noqa: F821 — constants.sh から動的注入
    if not issues:
        return []

    def sort_key(issue: dict) -> tuple[int, int]:
        """ソート用キー（優先度ランク, Issue 番号）。同ランクは古い番号順で処理。"""
        names = [lbl["name"] for lbl in issue.get("labels", [])]
        rank = priority_rank(
            names,
            GH_KIT_LABEL_PRIORITY_URGENT,  # noqa: F821
            GH_KIT_LABEL_PRIORITY_LOW,  # noqa: F821
        )
        return (rank, issue["number"])

    # 処理中ラベルが付いていない Issue だけを候補にする
    candidates = [
        i for i in issues
        if not has_label_prefix(
            [lbl["name"] for lbl in i.get("labels", [])],
            GH_KIT_LABEL_PROCESSING_PREFIX,  # noqa: F821
        )
    ]
    candidates.sort(key=sort_key)
    return [c["number"] for c in candidates]


def _run_ai_triage(issue_number: int) -> int:
    """claude -p に /gh-kit:issue-triage を投げて exit code を返す。デフォルト設定で実行。"""
    return run_claude_prompt(f"/gh-kit:issue-triage {issue_number}")


def _triage_issue(issue_number: int) -> None:
    """1 件の Issue に対し、処理中ラベル付与・AI トリアージを実行する。"""
    log(f"Issue #{issue_number} の triage を開始します")

    # noqa: F821 — GH_KIT_LABEL_PROCESSING_ISSUE_TRIAGE は constants.sh から動的注入
    if not github.add_label(issue_number, GH_KIT_LABEL_PROCESSING_ISSUE_TRIAGE):  # noqa: F821
        log(f"WARN: 処理中ラベルの付与に失敗しました（Issue #{issue_number}）")

    try:
        exit_code = _run_ai_triage(issue_number)

        if exit_code != 0:
            # claude -p が異常終了: 処理中ラベルを外してキュー再投入させる
            log(
                f"ERROR: claude -p が異常終了しました"
                f"（Issue #{issue_number}, exit_code={exit_code}）"
            )
            return

        log(f"Issue #{issue_number} の triage が完了しました（exit_code={exit_code}）")
    finally:
        github.remove_label(issue_number, GH_KIT_LABEL_PROCESSING_ISSUE_TRIAGE)  # noqa: F821


def poll() -> None:
    """1 回のポーリングで呼ばれるエントリーポイント。"""
    issue_numbers = _find_next_issues()
    if not issue_numbers:
        log(f"[issue-triage] 対象 Issue なし — {settings.POLL_INTERVAL}s 待機")
        return
    # 候補が複数あるなら優先度順に 1 件ずつ処理する
    for issue_number in issue_numbers:
        _triage_issue(issue_number)
