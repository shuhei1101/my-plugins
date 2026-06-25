from __future__ import annotations

import fcntl
import os
import subprocess
import sys

import github
import settings
from utils import GH_KIT_PLUGIN_DIR, _load_constants_sh, log

# constants.sh の定数をこのモジュールのトップレベルに注入
# （GH_KIT_LABEL_CONFIRM_ISSUE_REVIEW 等が定数名そのままで使える）
_load_constants_sh(globals())

# 優先度ソート時のランク（数値が小さいほど先に処理）
PRIORITY_RANK_URGENT = 0
PRIORITY_RANK_LOW = 1
PRIORITY_RANK_NORMAL = 2


def find_next_issue() -> int | None:
    """確認:issue-reviewer ラベル付きで処理中ではない次の Issue 番号を返す（なければ None）。"""
    issues = github.list_issues(GH_KIT_LABEL_CONFIRM_ISSUE_REVIEW)  # noqa: F821 — constants.sh から動的注入
    if not issues:
        return None

    def is_not_processing(issue: dict) -> bool:
        """Issue に 処理中:* ラベルが付いていないかを判定する。"""
        return not any(
            lbl["name"].startswith(GH_KIT_LABEL_PROCESSING_PREFIX) for lbl in issue.get("labels", [])  # noqa: F821
        )

    def priority_key(issue: dict) -> tuple[int, int]:
        """ソート用キー（優先度ランク, Issue 番号）を返す。同ランクは古い番号順。"""
        names = [lbl["name"] for lbl in issue.get("labels", [])]
        # 急ぎラベルあり: 最優先で処理
        if GH_KIT_LABEL_PRIORITY_URGENT in names:  # noqa: F821 — constants.sh から動的注入
            rank = PRIORITY_RANK_URGENT
        # いつでもラベルあり: 最劣後（他にネタが無いときだけ処理）
        elif GH_KIT_LABEL_PRIORITY_LOW in names:  # noqa: F821 — constants.sh から動的注入
            rank = PRIORITY_RANK_LOW
        # 優先度ラベルなし: 通常扱い
        else:
            rank = PRIORITY_RANK_NORMAL
        return (rank, issue["number"])

    candidates = [i for i in issues if is_not_processing(i)]
    if not candidates:
        return None
    candidates.sort(key=priority_key)
    return candidates[0]["number"]


def run_ai_review(issue_number: int) -> int:
    """claude -p に /gh-kit:issue-review を投げ、出力を stderr にミラーして exit code を返す。"""
    cmd = [
        "claude",
        "-p", f"/gh-kit:issue-review {issue_number}",  # プリント（非インタラクティブ）モードでスキルを実行
        "--plugin-dir", GH_KIT_PLUGIN_DIR,             # gh-kit プラグインディレクトリを指定
        "--permission-mode", "dontAsk",                 # 許可プロンプトをスキップ（デーモン用）
        "--allowedTools", "Bash,Read,Edit,Write,WebFetch",  # スキルに必要なツールのみ許可
        "--output-format", "json",                      # 結果を JSON で受け取り行単位でパース可能にする
        "--no-session-persistence",                     # セッション履歴を残さない（独立実行）
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    assert proc.stdout is not None
    for line in proc.stdout:
        sys.stderr.write(line)
        sys.stderr.flush()
    return proc.wait()


def review_issue(issue_number: int) -> None:
    """1 件の Issue に対し、処理中ラベル付与・flock 取得・AI レビューを実行する。"""
    log(f"Issue #{issue_number} のレビューを開始します")

    # noqa: F821 — GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER は constants.sh から動的注入
    if not github.add_label(issue_number, GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER):  # noqa: F821
        log(f"WARN: 処理中ラベルの付与に失敗しました（Issue #{issue_number}）")

    try:
        lock_fd = os.open(settings.LOCK_FILE, os.O_CREAT | os.O_WRONLY, 0o644)
        try:
            # 別インスタンスの並走を防ぐため非ブロッキングで排他ロックを取る
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                # 別インスタンスがロックを保持中: 今回はスキップして次回ポーリングに任せる
                log(f"SKIP: ロック取得失敗 — 別インスタンスが実行中です（Issue #{issue_number}）")
                return

            exit_code = run_ai_review(issue_number)

            if exit_code != 0:
                # claude -p が異常終了: ラベルを戻してキュー再投入させる
                log(
                    f"ERROR: claude -p が異常終了しました"
                    f"（Issue #{issue_number}, exit_code={exit_code}）"
                )
                log("  処理中ラベルを除去してキューに戻します")
                return

            log(f"Issue #{issue_number} のレビューが完了しました（exit_code={exit_code}）")
        finally:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            except OSError:
                pass
            os.close(lock_fd)
    finally:
        github.remove_label(issue_number, GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER)  # noqa: F821


def poll() -> None:
    """1 回のポーリングで呼ばれるエントリーポイント。"""
    issue_number = find_next_issue()
    if issue_number is not None:
        review_issue(issue_number)
    else:
        log(f"[issue-review] 対象 Issue なし — {settings.POLL_INTERVAL}s 待機")
