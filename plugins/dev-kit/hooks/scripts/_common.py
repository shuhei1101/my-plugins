# dev-kit フックスクリプト共通ヘルパー。
#
# このファイルは `/ref-inject:apply` によってインストールされるスターターテンプレート。
# `decision: block` の reason を出力するフックスクリプトや、フック stdin のパース、
# セッション単位の重複実行防止フラグなどの汎用ヘルパーを含む。プラグイン固有のヘルパーは
# 新しいフックを追加する際にこのファイルに追記する。クロスプラグイン共有禁止
# （インシデント `premature-cross-plugin-centralization` 参照）。

from __future__ import annotations

import json
import os
import pathlib
import sys
import tempfile

ENV_PREFIX = "DEV_KIT"

FALSY = {"false", "0", "no", "off"}
TRUTHY = {"true", "1", "yes", "on"}


def read_hook_input() -> dict:
    """フック入力 JSON を標準入力から読み込む。"""
    return json.loads(sys.stdin.read())


def env_truthy(name: str, default: bool = True) -> bool:
    """環境変数が truthy かどうかを返す。

    default=True（デフォルト）の場合、falsy な値以外を truthy として扱う（オプトアウト方式）。
    default=False の場合、truthy な値のみを truthy として扱う（オプトイン方式）。
    """
    raw = os.environ.get(name)
    if raw is None:
        return default
    val = raw.strip().lower()
    if default:
        return val not in FALSY
    return val in TRUTHY


def exit_if_stop_loop(input_data: dict) -> None:
    """Stop フックが再発火（stop_hook_active）のとき、静かに終了する。"""
    if input_data.get("stop_hook_active"):
        sys.exit(0)


def already_dispatched_this_session(tag: str, session_id: str) -> bool:
    """一時ファイルを使ったセッション単位の重複実行ガード。

    フラグが既に存在する場合は True を返す。存在しない場合はフラグを作成して False を返す。
    呼び出し元が早期リターンするかどうかを決定する。
    """
    flag = pathlib.Path(tempfile.gettempdir()) / f"{tag}-{session_id}"
    if flag.exists():
        return True
    flag.touch()
    return False


def emit_block_reason(prompt_path: pathlib.Path) -> None:
    """`{decision: block, reason: <プロンプト本文>}` JSON を標準出力に書き出す。"""
    if not prompt_path.exists():
        return
    body = prompt_path.read_text("utf-8")
    payload = {"decision": "block", "reason": body}
    sys.stdout.buffer.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
