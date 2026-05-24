"""work-kit / stop — Stop hook.

Claude Code がレスポンスを完了する直前に発火し、進行中の PR について
TODO / QA の更新が漏れていないかを確認させるプロンプトを注入する。

reason にはファイルパスの参照1行だけを出力する。
全文埋め込みは会話セッションを汚染するため、Claude 自身がファイルを読む方式にしている。

ループ防止:
- `stop_hook_active` が True で呼ばれた場合（= フック自身が連鎖発火した状態）は
  何もせず終了。これがないと Stop hook → block → 再開 → Stop hook ... を繰り返す。

Args:
    sys.argv[1]: 指示ファイルのパス
                 （hooks.json から `${CLAUDE_PLUGIN_ROOT}/hooks/prompts/stop.md` を渡す）
"""

from __future__ import annotations

import json
import pathlib
import sys


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read())
    except Exception:
        return

    if payload.get("stop_hook_active"):
        return

    prompt_path = pathlib.Path(sys.argv[1])
    if not prompt_path.exists():
        return

    reason = f"Read and follow: {prompt_path}"
    response = {"decision": "block", "reason": reason}
    sys.stdout.buffer.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    main()
