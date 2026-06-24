#!/usr/bin/env python3
"""issue-review-daemon.py

「確認:issue-reviewer」ラベル付き Issue を claude -p で直列処理するデーモン。

使い方:
    GH_KIT_PLUGIN_DIR=/path/to/gh-kit \\
    MCP_CONFIG_PATH=/path/to/mcp-config.json \\
    ./issue-review-daemon.py

環境変数:
    GH_KIT_PLUGIN_DIR   gh-kit プラグインのディレクトリパス（必須）
    MCP_CONFIG_PATH     MCP 設定ファイルパス（必須）
    AI_TOOL             使用する AI CLI ツール (claude / codex) [デフォルト: claude]
    POLL_INTERVAL       ポーリング間隔（秒）[デフォルト: 30]
    MAX_BUDGET_USD      claude -p の最大予算（USD）[デフォルト: 2.00]
    LOCK_FILE           flock に使うロックファイルパス [デフォルト: /tmp/gh-kit-issue-review.lock]
"""

from __future__ import annotations

import fcntl
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

GH_KIT_PLUGIN_DIR = os.environ.get("GH_KIT_PLUGIN_DIR", "")
MCP_CONFIG_PATH = os.environ.get("MCP_CONFIG_PATH", "")
AI_TOOL = os.environ.get("AI_TOOL", "claude")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "30"))
MAX_BUDGET_USD = os.environ.get("MAX_BUDGET_USD", "2.00")
LOCK_FILE = os.environ.get(
    "LOCK_FILE",
    str(Path(os.environ.get("TMPDIR", tempfile.gettempdir())) / "gh-kit-issue-review.lock"),
)

LABEL_CONFIRM = os.environ.get("GH_KIT_LABEL_CONFIRM_ISSUE_REVIEW", "確認:issue-reviewer")
LABEL_PROCESSING = os.environ.get("GH_KIT_LABEL_PROCESSING_ISSUE_REVIEWER", "処理中:issue-reviewer")
LABEL_PRIORITY_URGENT = os.environ.get("GH_KIT_LABEL_PRIORITY_URGENT", "優先度:急ぎ")
LABEL_PRIORITY_LOW = os.environ.get("GH_KIT_LABEL_PRIORITY_LOW", "優先度:いつでも")

EXIT_LOCK_BUSY = 200


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr, flush=True)


def die(msg: str) -> None:
    log(f"ERROR: {msg}")
    sys.exit(1)


def preflight() -> None:
    if not GH_KIT_PLUGIN_DIR:
        die("GH_KIT_PLUGIN_DIR が未設定です。gh-kit プラグインのディレクトリパスを指定してください。")
    if not Path(GH_KIT_PLUGIN_DIR).is_dir():
        die(f"GH_KIT_PLUGIN_DIR='{GH_KIT_PLUGIN_DIR}' が存在しません。")
    if not MCP_CONFIG_PATH:
        die("MCP_CONFIG_PATH が未設定です。MCP 設定ファイルのパスを指定してください。")
    if not Path(MCP_CONFIG_PATH).is_file():
        die(f"MCP_CONFIG_PATH='{MCP_CONFIG_PATH}' が存在しません。")
    for tool in (AI_TOOL, "gh"):
        if shutil.which(tool) is None:
            die(f"{tool!r} が見つかりません。インストールされているか確認してください。")


def get_next_issue() -> Optional[int]:
    try:
        result = subprocess.run(
            [
                "gh", "issue", "list",
                "--state", "open",
                "--label", LABEL_CONFIRM,
                "--json", "number,labels",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return None

    try:
        issues = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None

    def is_not_processing(issue: dict) -> bool:
        return not any(lbl["name"].startswith("処理中:") for lbl in issue.get("labels", []))

    def priority_key(issue: dict) -> tuple[int, int]:
        names = [lbl["name"] for lbl in issue.get("labels", [])]
        if LABEL_PRIORITY_URGENT in names:
            p = 0
        elif LABEL_PRIORITY_LOW in names:
            p = 1
        else:
            p = 2
        return (p, issue["number"])

    candidates = [i for i in issues if is_not_processing(i)]
    if not candidates:
        return None
    candidates.sort(key=priority_key)
    return candidates[0]["number"]


def add_label(issue_number: int, label: str) -> bool:
    return subprocess.run(
        ["gh", "issue", "edit", str(issue_number), "--add-label", label],
        capture_output=True,
    ).returncode == 0


def remove_label(issue_number: int, label: str) -> None:
    subprocess.run(
        ["gh", "issue", "edit", str(issue_number), "--remove-label", label],
        capture_output=True,
    )


def run_ai_review(issue_number: int) -> int:
    cmd = [
        AI_TOOL, "-p", f"/gh-kit:issue-review {issue_number}",
        "--plugin-dir", GH_KIT_PLUGIN_DIR,
        "--mcp-config", MCP_CONFIG_PATH,
        "--strict-mcp-config",
        "--permission-mode", "dontAsk",
        "--allowedTools", "Bash,Read,Edit,Write,WebFetch",
        "--max-budget-usd", MAX_BUDGET_USD,
        "--output-format", "json",
        "--no-session-persistence",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    assert proc.stdout is not None
    for line in proc.stdout:
        sys.stderr.write(line)
        sys.stderr.flush()
    return proc.wait()


def review_issue(issue_number: int) -> None:
    log(f"Issue #{issue_number} のレビューを開始します")

    if not add_label(issue_number, LABEL_PROCESSING):
        log(f"WARN: 処理中ラベルの付与に失敗しました（Issue #{issue_number}）")

    try:
        lock_fd = os.open(LOCK_FILE, os.O_CREAT | os.O_WRONLY, 0o644)
        try:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                log(f"SKIP: ロック取得失敗 — 別インスタンスが実行中です（Issue #{issue_number}）")
                return

            exit_code = run_ai_review(issue_number)

            if exit_code != 0:
                log(f"ERROR: {AI_TOOL} -p が異常終了しました（Issue #{issue_number}, exit_code={exit_code}）")
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
        remove_label(issue_number, LABEL_PROCESSING)


def main() -> None:
    preflight()

    log("issue-review-daemon 起動")
    log(f"  AI_TOOL={AI_TOOL}")
    log(f"  GH_KIT_PLUGIN_DIR={GH_KIT_PLUGIN_DIR}")
    log(f"  MCP_CONFIG_PATH={MCP_CONFIG_PATH}")
    log(f"  POLL_INTERVAL={POLL_INTERVAL}s")
    log(f"  MAX_BUDGET_USD={MAX_BUDGET_USD}")
    log(f"  LOCK_FILE={LOCK_FILE}")
    log(f"ポーリング開始（間隔: {POLL_INTERVAL}s）")

    while True:
        issue_number = get_next_issue()
        if issue_number is not None:
            review_issue(issue_number)
        else:
            log(f"対象 Issue なし — {POLL_INTERVAL}s 待機")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("SIGINT を受信しました。終了します。")
        sys.exit(130)
