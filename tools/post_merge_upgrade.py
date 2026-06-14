"""push + marketplace upgrade + reload-plugins を実行するコアスクリプト。

フック（.claude/hooks/post-merge-upgrade.py）およびMCPツール（push）から呼ばれる。
各サブステップは silent fail させず、結果を stdout にまとめて出す（フックがそれを会話に注入する）。

# 直接実行
python tools/post_merge_upgrade.py
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


# 各サブプロセスのタイムアウト（秒）。ハング検知用なので長すぎず短すぎず。
_STEP_TIMEOUT = 30


def _run_step(label: str, cmd: list[str], cwd: str) -> tuple[bool, str]:
    """サブステップを 1 個実行し、(ok, 表示用テキスト) を返す。

    ハング検知のため `_STEP_TIMEOUT` 秒で打ち切る。
    """
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, check=False,
            timeout=_STEP_TIMEOUT,
        )
    except FileNotFoundError as e:
        return False, f"### {label}: 実行ファイルなし\n\n```\n{e}\n```"
    except subprocess.TimeoutExpired:
        return False, f"### {label}: TIMEOUT ({_STEP_TIMEOUT}s)\n\nハングしている可能性があります。"

    ok = result.returncode == 0
    head = f"### {label}: {'OK' if ok else f'FAIL (rc={result.returncode})'}"
    body_parts: list[str] = []
    if result.stdout.strip():
        body_parts.append(f"stdout:\n```\n{result.stdout.strip()}\n```")
    if result.stderr.strip():
        body_parts.append(f"stderr:\n```\n{result.stderr.strip()}\n```")
    body = "\n\n".join(body_parts) if body_parts else "(no output)"
    return ok, f"{head}\n\n{body}"


def run() -> str:
    """push + marketplace upgrade + reload-plugins を順に実行し、レポート文字列を返す。"""
    reports: list[str] = []

    # push: WSL からは Windows 側の git.exe を使う（HTTPS 認証が WSL の git に通らないため）
    # cwd は WSL パスのまま渡す — Python の chdir は WSL 側で行われるため Windows パスにすると失敗する。
    # git.exe は WSL interop で WSL パスを解釈できる。
    git_cmd = (
        ["git.exe", "push", "origin", "master"]
        if sys.platform != "win32"
        else ["git", "push", "origin", "master"]
    )
    push_ok, push_report = _run_step("push", git_cmd, str(REPO_ROOT))
    reports.append(push_report)

    # push が GitHub に反映されるまで待機（push 失敗時は意味ないのでスキップ）
    if push_ok:
        time.sleep(2)

    # marketplace upgrade
    _, mp_report = _run_step(
        "marketplace upgrade",
        [sys.executable, str(REPO_ROOT / "tools" / "marketplace.py"), "upgrade"],
        str(REPO_ROOT),
    )
    reports.append(mp_report)

    # 起動中の tmux セッションに /reload-plugins を送信
    _, rl_report = _run_step(
        "reload-plugins",
        [sys.executable, str(REPO_ROOT / "tools" / "reload_plugins.py")],
        str(REPO_ROOT),
    )
    reports.append(rl_report)

    return "## post-merge-upgrade\n\n" + "\n\n".join(reports)


def main() -> int:
    """エントリポイント。レポートを stdout に出す。"""
    print(run())
    return 0


if __name__ == "__main__":
    sys.exit(main())
