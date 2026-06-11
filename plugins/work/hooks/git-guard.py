"""workspace / git-guard — PreToolUse(Bash) hook.

`git push` または `git merge` を含む Bash コマンドを検出したとき、
プロンプト注入 (`decision: block`) で必ずユーザー確認を挟む。

ただし `git merge master` / `git merge main` など、上流ブランチを現在のブランチへ
取り込む操作は安全なのでブロックしない。
ブロック対象は master/main 以外のブランチへの merge（例: feature ブランチ上で
`git merge master` は OK、master ブランチ上で `git merge feature` はブロック）。

ループ防止のため、セッションごとに一時トークンファイルを使い、
1 回ブロックしたら 2 回目以降は素通りさせる
(= 同一セッションで同じコマンドを再実行できる)。

env トグル:
    WORK_GUARD: `false` / `0` / `no` / `off` で無効化（デフォルト有効）

Args:
    sys.argv[1]: プロンプト本文の Markdown ファイルパス
                 （hooks.json から `${CLAUDE_PLUGIN_ROOT}/hooks/prompts/git-guard.md` を渡す）
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import sys
import tempfile

# origin/ プレフィックスあり/なし両方に対応した安全マージの判定パターン
_SAFE_MERGE = re.compile(
    r"\bgit\s+merge\s+(origin/)?(master|main)\b"
)


def main() -> None:
    # env で無効化されていれば何もしない
    if os.environ.get("WORK_GUARD", "true").lower() in ("false", "0", "no", "off"):
        return

    payload = json.loads(sys.stdin.read())
    command = payload.get("tool_input", {}).get("command", "")

    # push / merge どちらも含まないコマンドはスキップ
    if not re.search(r"\bgit\s+(push|merge)\b", command):
        return

    # master/main を現在ブランチへ取り込む操作（上流取り込み）はブロック不要
    if _SAFE_MERGE.search(command):
        return

    # セッション単位のワンタイムトークンで「確認 → 通過 → 確認 → 通過」を交互に実現
    session_id = payload.get("session_id", "default")
    token = pathlib.Path(tempfile.gettempdir()) / f"workspace-git-guard-{session_id}"

    if token.exists():
        # 2 回目以降：トークンを消費して素通り（再実行を許可）
        token.unlink()
        return

    # 1 回目：トークンを作成してブロック（ユーザー確認を促す）
    token.touch()

    prompt_path = pathlib.Path(sys.argv[1])
    if not prompt_path.exists():
        return

    response = {"decision": "block", "reason": prompt_path.read_text("utf-8")}
    sys.stdout.buffer.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    main()
