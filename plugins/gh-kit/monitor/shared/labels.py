"""GitHub ラベル関連のユーティリティ。

scripts/constants.sh の export 行を Python 名前空間に注入する load_constants_sh と、
優先度ランクや prefix 一致判定など、各モニターから使い回す関数を提供する。
"""

from __future__ import annotations

import os

from shared.constants import CONSTANTS_SH_PATH

# 優先度ランク（数値が小さいほど先に処理される）
PRIORITY_RANK_URGENT = 0
PRIORITY_RANK_LOW = 1
PRIORITY_RANK_NORMAL = 2


def load_constants_sh(target: dict[str, object]) -> None:
    """scripts/constants.sh の export 行を target 名前空間に注入する。

    target には通常 globals() を渡し、constants.sh の定数名（GH_KIT_LABEL_*）
    がそのままモジュールトップレベル変数として参照可能になる。
    定数の再定義（Python 側で名前を付け直す）を不要にし、constants.sh を SoT に統一する。
    既に os.environ に値があれば（外部 export 済み）そちらを優先。
    """
    if not CONSTANTS_SH_PATH.is_file():
        # フォールバックは設けない: 必須ファイルが無ければ起動を中止
        raise FileNotFoundError(f"constants.sh が見つかりません: {CONSTANTS_SH_PATH}")
    for raw in CONSTANTS_SH_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        # export VAR=VALUE 形式のみ取り込む（コメント・空行・shebang・その他は無視）
        if not line.startswith("export "):
            continue
        body = line[len("export "):]
        if "=" not in body:
            continue
        key, value = body.split("=", 1)
        # bash の `"..."` / `'...'` クォートを剥がす（同じ記号で囲まれている場合のみ）
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        # 外部 env を優先し、無ければ constants.sh の値を採用
        target[key] = os.environ.get(key, value)


def priority_rank(label_names: list[str], urgent_label: str, low_label: str) -> int:
    """ラベル名リストから優先度ランクを返す。

    引数:
        label_names: Issue/PR に付いているラベル名のリスト
        urgent_label: 急ぎラベル名（例: ``GH_KIT_LABEL_PRIORITY_URGENT``）
        low_label: 後回しラベル名（例: ``GH_KIT_LABEL_PRIORITY_LOW``）

    戻り値:
        ``PRIORITY_RANK_URGENT`` / ``PRIORITY_RANK_LOW`` / ``PRIORITY_RANK_NORMAL``
        のいずれか。数値が小さいほど先に処理されるべき。
    """
    if urgent_label in label_names:
        return PRIORITY_RANK_URGENT
    if low_label in label_names:
        return PRIORITY_RANK_LOW
    return PRIORITY_RANK_NORMAL


def has_label_prefix(label_names: list[str], prefix: str) -> bool:
    """ラベル名リストに、指定 prefix で始まるラベルが含まれているか判定する。"""
    return any(name.startswith(prefix) for name in label_names)
