"""注入ドメインのデータモデル。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class InjectionBlock:
    """1 ルール分の注入内容。"""

    url: str
    patterns: tuple[str, ...]
    body: str
    offset: int = 0  # body が元の本文のどこから始まっているか


@dataclass(frozen=True, slots=True, kw_only=True)
class PackResult:
    """上限に収める処理の結果。"""

    blocks: list[InjectionBlock]
    completed: list[str]  # 今回で全量を送り終えた URL
    partial: dict[str, int]  # 続き位置を持ち越す URL と位置
    remaining: int  # 次回に持ち越す件数
