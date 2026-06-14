"""workspace / post-commit-deletion-check — Stop hook.

レスポンス終了時に「直近 5 コミットで削除されたファイル数」をチェックし、
閾値（デフォルト 30）を超えていたら警告コンテキストを注入する。

警告のみで block はしない。マージ事故で大量ファイルが消えたときに
気付くきっかけを作るのが目的。

env:
    WORK_DELETION_THRESHOLD: 削除件数の警告閾値（デフォルト 30）
    WORK_DELETION_LOOKBACK: 何コミット遡るか（デフォルト 5）
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

DEFAULT_THRESHOLD = 30
DEFAULT_LOOKBACK = 5


def _count_deletions(lookback: int) -> tuple[int, list[str]]:
    """直近 lookback コミットでの削除ファイル数と代表サンプルを返す。"""
    rev_range = f"HEAD~{lookback}..HEAD"
    result = subprocess.run(
        ["git", "log", "--diff-filter=D", "--name-only", "--pretty=format:", rev_range],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        # 履歴が浅くて HEAD~N が無い場合などは黙ってスキップ
        return 0, []

    files = [line for line in result.stdout.splitlines() if line.strip()]
    return len(files), files[:10]


def main() -> None:
    """削除件数を計測して閾値超なら警告を出す。"""
    # stdin はあるけど内容は使わない
    sys.stdin.read()

    threshold = int(os.environ.get("WORK_DELETION_THRESHOLD", DEFAULT_THRESHOLD))
    lookback = int(os.environ.get("WORK_DELETION_LOOKBACK", DEFAULT_LOOKBACK))

    count, samples = _count_deletions(lookback)
    if count < threshold:
        return

    sample_block = "\n".join(f"- `{f}`" for f in samples)
    message = (
        f"⚠️ 直近 {lookback} コミットで {count} 件のファイル削除を検出しました（閾値 {threshold}）。\n\n"
        f"代表サンプル（最大 10 件）:\n{sample_block}\n\n"
        "意図した削除でなければ `git log --diff-filter=D --name-only` で全体を確認し、\n"
        "誤削除が混じっていないか調べてください。"
    )
    sys.stdout.buffer.write(
        json.dumps({"additionalContext": message}, ensure_ascii=False).encode("utf-8")
    )


if __name__ == "__main__":
    main()
