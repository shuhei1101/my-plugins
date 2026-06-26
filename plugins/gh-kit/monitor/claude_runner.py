from __future__ import annotations

import subprocess
import sys

# 使用するモデル（Opus 4.7 を明示指定。利用不可なら CLI 側でエラー）
MODEL = "claude-opus-4-7"


def run_claude_prompt(prompt: str) -> int:
    """claude -p にプロンプトを投げ、出力を stderr にミラーして exit code を返す。

    引数:
        prompt: claude -p に渡すプロンプト（例: ``"/gh-kit:issue-triage 42"``）

    戻り値:
        claude プロセスの exit code
    """
    cmd = [
        "claude",
        "-p", prompt,
        # 権限チェックを全スキップ（デーモン無人運用なので承認プロンプトが出ると詰まるため）
        "--permission-mode", "bypassPermissions",
        # 出力を JSON で受け取る（モニター側で機械処理しやすいフォーマット）
        "--output-format", "json",
        # 使用モデルを明示（CLI デフォルトに依存せず固定）
        "--model", MODEL,
        # セッション履歴をディスクに残さない（1 回限りの独立実行のため）
        "--no-session-persistence",
    ]
    # claude をサブプロセスとして起動。
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # PIPE を指定しているので stdout は必ず存在するが、型チェッカ向けに表明しておく
    assert proc.stdout is not None

    # 子プロセスが書いた行をリアルタイムに親プロセスの stderr へそのまま流す
    # （バッファに溜め込まずに進捗を即座に見えるようにする）。
    # flush() を毎行呼ぶのは、stderr が tty でない場合に行バッファされないようにするため。
    for line in proc.stdout:
        sys.stderr.write(line)
        sys.stderr.flush()

    # 子プロセスの終了を待ち、その exit code を呼び出し元に返す
    return proc.wait()
